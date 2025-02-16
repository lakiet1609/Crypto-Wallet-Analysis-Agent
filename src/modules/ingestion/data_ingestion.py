import os
import asyncio
import json

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser

from src.database.db.wallet_db import CryptoDatabase
from src.config.app_config import (Config as cfg,
                                   CryptoConfig as cpt)
from src.utils.logger import logging
from src.utils.common import find_valid_json, post_process_result


class DataIngestionAgent:
    def __init__(self):
        self.cryto_db = CryptoDatabase()
        self.collection = self.cryto_db.get_collection()
        self.llm = ChatOpenAI(model=cpt.model, api_key=cfg.OPENAI_API_KEY)
        self.browser = Browser()
        self.wallet_file = cpt.data_path
        self.rate_limit_delay = cpt.rate_limit_delay
        self.etherscan_base_url = cpt.etherscan_base_url
        self.output = self.output_json()

        logging.info('Init Data Ingestion Agent')
    

    def output_json(self):
        return  """
        ```json
        {
        "wallet_address": "0xABC123...789",
        "tokens_held": [
            {
            "symbol": "USDT",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6
            },
            {
            "symbol": "ETH",
            "contract_address": "native",
            "decimals": 18
            }
        ],
        "token_balances": [
            {
            "symbol": "USDT",
            "balance": 1250.50
            },
            {
            "symbol": "ETH",
            "balance": 3.412
            }
        ],
        "wallet_ages": 
            {
            "latest": "2 days ago",
            "first": "5 days ago",
            }
        ],
        "transaction_history": [
            {
            "timestamp": 1708060800,
            "tx_hash": "0x1234abc567...",
            "token": "ETH",
            "amount": 0.25,
            "type": "send",
            "asset_type": "native",
            "from": "0xABC123...789",
            "to": "0xDEF456...012"
            },
            {
            "timestamp": 1708057200,
            "tx_hash": "0x789xyz123...",
            "token": "USDT",
            "amount": 500,
            "type": "receive",
            "asset_type": "ERC-20",
            "from": "0xGHI789...345",
            "to": "0xABC123...789"
            }
        ]
        }
        """


    async def scrape_wallet_data(self, wallet_address):
        try:
            agent = Agent(
                task=f"""
                    **Objective:**  
                    Visit [Etherscan]({self.etherscan_base_url}/{wallet_address}), navigate to the provided wallet address, and extract the following details:
                    1. Wallet Address
                    2. Token Holdings (Balances & USD Values)
                    3. Transaction History (Timestamps, Amounts, Types)

                    ---

                    ### Step 1: Navigate to the Wallet Address
                    - Open [Etherscan]({self.etherscan_base_url}/{wallet_address}).
                    - Ensure the page loads completely and displays the wallet details.

                    ---

                    ### Step 2: Extract Wallet Address
                    - Locate the wallet address displayed prominently on the page.
                    - Extract and save the wallet address.

                    ---

                    ### Step 3: Extract Token Holdings
                    - Navigate to the "Tokens" or "Token Holdings" section of the wallet.
                    - For each token listed, extract:
                    - **Symbol (e.g., USDT, ETH)**  
                    - **Contract Address (use "native" for ETH)**  
                    - **Decimals (e.g., 6 for USDT, 18 for ETH)**  
                    - **Balance (e.g., 1250.50 USDT, 3.412 ETH)**  

                    ---

                    ### Step 4: Extract Wallet Age
                    - Navigate to the "Transactions Sent", "First", "Latest" sections of the wallet.
                    - **Latest (e.g., 2 days ago)**  
                    - **First (e.g., 5 days ago)**  

                    ---
                    
                    ### Step 5: Extract Transaction History
                    - Navigate to the "Transactions" or "Transaction History" section of the wallet.
                    - Navigate to the "VIEW ALL TRANSACTIONS" section of the wallet.
                    - Must extract all transactions listed on the page.
                    - For each transaction, extract:
                    - **Timestamp (in Unix format)**  
                    - **Token (e.g., ETH, USDT)**  
                    - **Amount (e.g., 0.25 ETH, 500 USDT)**  
                    - **Type (e.g., "send" or "receive")**  
                    - **Asset Type (e.g., "native" for ETH, "ERC-20" for tokens)**  
                    - **From (sender address)**  
                    - **To (receiver address)**  


                    ---

                    ### Step 6: Format Data into JSON
                    - Store the extracted information in the following strictly JSON format. Make sure these details are accurate and well-structured like the example below:
                    {self.output}

                    """,
                llm=self.llm,
                browser=self.browser
            )

            result = await agent.run()
            
            parsed_data = find_valid_json(result)

            final_result = post_process_result(parsed_data) 

            await asyncio.sleep(self.rate_limit_delay)
            
            return final_result
        
        except Exception as e:
            logging.error(f'Error in scraping wallet data: {e}')
            return None
    

    def save_mongodb(self, wallet_data):
        if wallet_data:
            existing_entry = self.collection.find_one({"wallet_address": wallet_data["wallet_address"]})
            if existing_entry:
                self.collection.update_one({"wallet_address": wallet_data["wallet_address"]}, {"$set": wallet_data})
                logging.info(f"Updated wallet data for address: {wallet_data['wallet_address']}")
            else:
                self.collection.insert_one(wallet_data)
                logging.info(f"Saved wallet data for address: {wallet_data['wallet_address']}")

    
    async def process_wallets(self, wallet_file):
        if not os.path.exists(wallet_file):
            logging.info(f"Error: File '{wallet_file} not found.")
            return
        
        with open(wallet_file, 'r') as f:
            wallet_addresses = [line.strip() for line in f if line.strip()]
        
        logging.info(f'Found {len(wallet_addresses)} wallet addresses in the file.')

        tasks = [self.scrape_wallet_data(wallet_address) for wallet_address in wallet_addresses]
        results = await asyncio.gather(*tasks)

        for wallet_data in results:
            if wallet_data:
                self.save_mongodb(wallet_data)
            
    
    def run(self):
        asyncio.run(self.process_wallets(self.wallet_file))
        logging.info('Data Ingestion Agent completed successfully')

