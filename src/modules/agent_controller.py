from src.modules import (AgentProtocol,
                         HistoricalTrendAnalysisAgent,
                         WalletAgeAgent,
                         DataIngestionAgent)

from src.utils.logger import logging


class AgentController:
    def __init__(self):
        self.data_ingestion_agent = DataIngestionAgent()
        self.wallet_age_agent = WalletAgeAgent()
        self.trend_analysis_agent = HistoricalTrendAnalysisAgent()

    def get_response(self, input):
        logging.info('Start scraping ...')
        self.data_ingestion_agent.run()

        logging.info('Start wage age analysis')
        self.wallet_age_agent.get_response(input)

        logging.info('Start historical trend analysis')
        self.trend_analysis_agent.get_response(input)