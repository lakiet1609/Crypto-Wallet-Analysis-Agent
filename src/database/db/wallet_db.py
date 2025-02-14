from src.database.base_database import BaseDatabase
from src.config.app_config import DatabaseConfig

class CryptoDatabase(BaseDatabase):
    def __init__(self):
        self.config = DatabaseConfig().init_database()
        super(CryptoDatabase, self).__init__(self.config)

        database_name = self.config['database_name']
        collection_name = self.config['collection_name']
        self.database = self.client[database_name]
        self.base_collection = self.database[collection_name]

    def get_collection(self):
        return self.base_collection
