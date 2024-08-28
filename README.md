# Azure OpenAI list unexpected model deployments

This repository contains a simple filed-driven script to list all the model deployments of Azure OpenAI service account that are not "Standard" in your subscription. The aim, is to provide a quick overview of unexpected deployments that may be consuming resources.

This scripts uses the combination of Python and Azure CLI.


## Requirements
- Python 3.8 or later
- Azure CLI

## Usage
1. Clone the repository
2. Install the required Python packages
```bash
pip install -r requirements.txt
```
3. Login to Azure CLI
```bash
az login
```
4. Set the subscription
```bash
az account set --subscription <subscription_id>
```
5. Run the script
```bash
python check_deployment.py
```

Example output:
```bash
(.venv) M@X Azure-OpenAI-list-model-deployments % python check_deployment.py
Fetching resource groups in subscription:: 100%|████████████████████████████████████████████████████████████████████████████| 6/6 [00:00<00:00, 101475.10it/s]
Found 6 resource groups
Fetching Azure OpenAI services: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:03<00:00,  1.65it/s]
Found 18 services
Exploring deployments: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████| 18/18 [00:12<00:00,  1.45it/s]
Unusual deployment gpt-4o-mini-prov in rg-ai-openai: model gpt-4o-mini sku Provisioned-Managed
Unusual deployment gpt-4o-global in rg-ai-openai: model gpt-4o sku GlobalStandard
```


## Disclaimer
> This repository is not affiliated with OpenAI or Microsoft. The information provided here is based on publicly available information and is subject to change. Author is not responsible for any misuse of the information provided here. You are solely responsible for any use and results you obtain with this script.