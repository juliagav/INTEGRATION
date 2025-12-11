# src/database/connection.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.collection import Collection
import time
import os


class DatabaseConnection:
    """
    Gerencia conexão com MongoDB (Singleton)
    
    Centraliza:
    - Retry logic
    - Configuração via variáveis de ambiente
    - Conexão única reutilizável
    """
    
    _instance = None
    _client = None
    _db = None
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos
    
    def __new__(cls):
        """Singleton: garante uma única instância"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect_with_retry()
    
    def _connect_with_retry(self):
        """Tenta conectar ao MongoDB com retry"""
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        mongo_database = os.getenv("MONGO_DATABASE", "tractian")
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"🔄 Tentativa {attempt}/{self.MAX_RETRIES} - Conectando ao MongoDB...")
                
                self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                self._client.admin.command('ping')
                self._db = self._client[mongo_database]
                
                print("✅ Conectado ao MongoDB!")
                return
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"❌ Tentativa {attempt}/{self.MAX_RETRIES} falhou: {e}")
                
                if attempt < self.MAX_RETRIES:
                    print(f"⏳ Aguardando {self.RETRY_DELAY}s antes de tentar novamente...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    print("❌ Todas as tentativas falharam. MongoDB indisponível.")
                    self._client = None
                    self._db = None
    
    def get_collection(self, collection_name: str) -> Collection | None:
        """Retorna uma collection do banco"""
        if self._db is None:
            print("❌ Sem conexão com MongoDB")
            return None
        return self._db[collection_name]
    
    def is_connected(self) -> bool:
        """Verifica se está conectado"""
        return self._client is not None and self._db is not None
    
    def close(self):
        """Fecha conexão com MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("✅ Conexão MongoDB fechada")


# Função helper para facilitar o uso
def get_db() -> DatabaseConnection:
    """Retorna instância do banco de dados"""
    return DatabaseConnection()


def get_workorders_collection() -> Collection | None:
    """Retorna a collection de workorders"""
    db = get_db()
    return db.get_collection("workorders")