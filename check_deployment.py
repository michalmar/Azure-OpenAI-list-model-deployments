import logging
from azure.cli.core import get_default_cli
import os
from  tqdm import tqdm

def az_cli_run(args_str, verbose=False):
    args = args_str.split()[1:]
    if verbose:
        logging.info(f"az_cli_run: {args}")
    cli = get_default_cli()
    
    # Suppress output
    with open(os.devnull, 'w') as devnull:
        original_stdout = os.dup(1)
        original_stderr = os.dup(2)
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
        
        try:
            cli.invoke(args)
        finally:
            os.dup2(original_stdout, 1)
            os.dup2(original_stderr, 2)
            os.close(original_stdout)
            os.close(original_stderr)
    
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

command = f"az group list --output json"
json_data = az_cli_run(command)

resource_groups = []
for item in tqdm(json_data, desc="Fetching resource groups in subscription:"):
    resource_groups.append( item["name"])

print(f"Found {len(resource_groups)} resource groups")

services = []
for rg in tqdm(resource_groups, desc="Fetching Azure OpenAI services"):
    command = f"az cognitiveservices account list --resource-group {rg} --output json"
    json_data = az_cli_run(command)
    if isinstance(json_data, bool):
        continue
    for item in json_data:
        if item["kind"] == "OpenAI":
            services.append(
                {
                    "name": item["name"],
                    "resource_group": rg,
                },
            )

print(f"Found {len(services)} services")

# for service in services:
for service in tqdm(services, desc="Exploring deployments"):
    
    service["deployments"] = []
    # az cognitiveservices account deployment list --name aoai-swedencentral --resource-group rg-ai-openai --output json | jq '.[] | {deployment: .name, model: .properties.model.name, sku: .sku.name}'
    command = f"az cognitiveservices account deployment list --name {service['name']} --resource-group {service['resource_group']} --output json"
    json_data = az_cli_run(command)

    # service["deployments"] = json_data
    for item in json_data: 
        service["deployments"].append({
            "deployment": item["name"],
            "model": item["properties"]["model"]["name"],
            "sku": item["sku"]["name"]
        })

unusual_deployments = []
for service in services:
    # print(f"Deploying models to {service['name']} in {service['resource_group']} ")
    for deployment in service["deployments"]:
        if deployment["sku"] != "Standard":
            print(f"Unusual deployment {deployment['deployment']} in {service['resource_group']}: model {deployment['model']} sku {deployment['sku']}")
            unusual_deployments.append({
                "service": service["name"],
                "resource_group": service["resource_group"],
                "deployment": deployment["deployment"],
                "model": deployment["model"],
                "sku": deployment["sku"]
            })
        else:
            pass

# sace services to a file as json
import json
from datetime import datetime
from tqdm import tqdm
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
with open(f'services_{current_time}.json', 'w') as json_file:
    json.dump(unusual_deployments, json_file)

