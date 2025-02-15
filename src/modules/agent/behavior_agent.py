import json

from src.utils.response import get_client, get_chat_response
from src.utils.common import write_json_to_text
from src.database.db.wallet_db import CryptoDatabase
from src.utils.logger import logging
from src.config.app_config import (CryptoConfig as cc,
                                   Config as cfg)


class BehaviorAgent:
    def __init__(self):
        self.cryto_db = CryptoDatabase()
        self.collection = self.cryto_db.get_collection()
        
        self.client = get_client(
            api_key=cfg.RUNPOD_TOKEN,
            url=cfg.RUNPOD_URL
        )

        self.model_name = cc.chatbot_model_name
        self.wallet_age_report_path = cc.wallet_age_report_path

        self.output_format = """
        {
        "First Transaction": "YYYY-MM-DD". The date you calculated in step 1. Only the date in (YYYY-MM-DD) format,
        "Wallet Age": "X years, Y months, Z days". X,Y and Z are the number you calculated in step 2 ,
        "Category": "Veteran" or "Established" or "Intermediate" or "Newcomer". Pick one of those and only write the word. ,
        "Analysis": Leave the analysis in step 4 here. Write the analysis in a clear and concise manner.
        }
        """

        logging.info('Init Wallet Age Agent')
    

    def get_wallet_address(self, wallet_address):
        document = self.collection.find_one({"wallet_address": wallet_address})
        return document


    def get_response(self, wallet_address):        
        document = self.get_wallet_address(wallet_address)

        document = str(document)

        system_prompt = f"""
            You are a helpful AI assistant for extracting information in cryto wallet. The format of the wallet is in JSON format.
            Your task is to wallet age analysis for a given wallet address. These are the information you need to extract:
            1. Extract the first transaction date in (YYYY-MM-DD format). In the data, you will find the "wallet_ages" keys which contains the "first" key. From the value of the "first" key, extract how many days ago then do the convert back to (YYYY-MM-DD format) by subtracting the given number of days from today's date. \\
               Today is: 2025-02-17 \\
               Example: "first": "5 days ago" -> "2025-02-01"
            
            2. Calculate the wallet age into X years, Y months, Z days formats \\
               Instructions:
               - Assume 1 year = 365 days and 1 month = 30 days (for simplicity).
               
               Calculate:
               - The number of full years by dividing the total days by 365.
               - The remaining days after extracting full years.
               - The number of full months by dividing the remaining days by 30.
               - The number of full years by dividing the total days by 365.
               
               Provide the result in the format: "X years, Y months, Z days"
               Example: "1 year, 0 months, 9 days" for 374 days.
               If the number of years, months, or days is zero, still display it explicitly (e.g., "0 years, 3 months, 15 days"). Ensure that the output is structured and easy to understand.

            3. From the "X years, Y months, Z days", you calculated in the previous step, categorize the wallet as:
                - "Veteran" (5+ years)
                - "Established" (2-5 years)
                - "Intermediate" (1-2 years)
                - "Newcomer" (less than 1 year)
            
            4. Provide a brief interpretation of what the wallet's age suggests about the holder's experience.


            Your output must be in structured json format like this below. All of the value of each key is the answer of each task given you when doing extract the wallet. Each key is a string and each value is a string. Make sure to follow the format strictly:
            {self.output_format}

            Here is the provided wallet:
            {document}
            """
        
        input_messages = [{'role': "system", "content": system_prompt}] + [{'role': "user", "content": "Analyze the wallet age for the given wallet address."}]

        output = get_chat_response(self.client, self.model_name, input_messages)

        output = json.loads(output)

        write_json_to_text(data=output, output_text_file=self.wallet_age_report_path)

        logging.info('Finish wallet age analysis process ...')

        return output