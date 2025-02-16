# Crypto-Wallet-Analysis-Agent

## Overview
The Crypto Wallet Analysis Agent is a tool designed for analyzing cryptocurrency wallet activity, trends, and patterns. It includes agents that assess wallet age, transaction trends, and overall behavior using various data ingestion and processing modules.

## Overview
```
├── data                    # Contains input data files like wallet addresses
├── development             # Development and testing scripts
│   ├── test.ipynb          # Jupyter Notebook for testing
│   └── test.py             # Python script for testing
├── logs                    # Log files for tracking execution
├── output                  # Stores processed results and analysis outputs
├── scripts                 # Utility scripts
├── src                     # Main source code directory
│   ├── config              # Configuration files
│   ├── database            # Database-related scripts
│   ├── modules             # Core modules for agents and ingestion
│   ├── utils               # Utility functions (logging, common operations)
├── LICENSE                 # Project license
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
```

## Overview
### Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Pip and virtual environment tools

### Installation
1. Clone the repository:
```
git clone <repo_url>
cd crypto-wallet-analysis-agent
```

2. Create and activate a virtual environment:
```
conda create -n $NAME_PROJECT -python=3.11 -y
conda activate $NAME_PROJECT
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create .env fille:
```
#Database
DATABASE_USER=USER
DATABASE_PASSWORD=PASSWORD
DATABASE_HOSTNAME=mongodb
DATABASE_PORT=27017
DATABASE_URL=mongodb://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOSTNAME}:${DATABASE_PORT}


#Etherscan
OPENAI_API_KEY=YOUR_OPEN_AI_KEY

#Runpod
RUNPOD_TOKEN=YOUR_RUNPOD_TOKEN
RUNPOD_URL=YOUR_RUNPOD_URL
```

5. Init .env:
```
source .env
export PYTHONPATH="$PYTHONPATH:$PWD"
```

6. Init MONGODB container:
```
docker run -d --name mongodb_container -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=USER -e MONGO_INITDB_ROOT_PASSWORD=PASSWORD mongo:latest
```

## Usage Examples
### Running the Agents
To run the whole pipeline, run the following command:
```
python src/modules/agent_controller.py
```

## Design Decisions

## Modular Architecture

Each component (config, database, modules, utils) is separately organized for maintainability and scalability.

## Agent-Based Analysis

The agent modules (trend_agent.py, wallet_age_agent.py) follow a structured approach to analyze wallet behavior.

## Configurable Parameters

Uses YAML-based configuration files (crypto.yaml, database.yaml) for easy modifications without code changes.

## Logging System

A centralized logging system (utils/logger.py) tracks important runtime information.


## Limitations and Assumptions
1. I have not integrated workflow orchestration
2. I have not finished the whole project in time. Lack of `Transaction Analysis` and `Behavioral Classification` modules