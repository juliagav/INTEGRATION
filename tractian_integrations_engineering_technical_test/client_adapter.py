# src/adapters/client_adapter.py
import json
from pathlib import Path
from typing import List, Dict
from src.utils.logger import logger
from src.utils.config import DATA_INBOUND_DIR, DATA_OUTBOUND_DIR

class ClientAdapter:
    """Lê e escreve arquivos JSON do sistema do cliente"""
    
    def __init__(self):
        self.inbound_dir = Path(DATA_INBOUND_DIR)
        self.outbound_dir = Path(DATA_OUTBOUND_DIR)
    
    def read_inbound_files(self) -> List[Dict]:
        """
        Lê todos os arquivos JSON da pasta inbound
        
        Returns:
            Lista de work orders (dicionários)
        """
        work_orders = []
        
        # Pega todos os arquivos .json
        json_files = list(self.inbound_dir.glob("*.json"))
        
        logger.info(f"📥 Encontrados {len(json_files)} arquivos JSON")
        
        for file_path in json_files:
            try:
                # Abre e lê o JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    work_orders.append(data)
                    logger.info(f"✅ Lido: {file_path.name}")
            except Exception as e:
                logger.error(f"❌ Erro ao ler {file_path.name}: {e}")
        
        return work_orders
    
    def write_outbound_file(self, work_order: Dict) -> None:
        """
        Escreve uma work order como JSON na pasta outbound
        
        Args:
            work_order: Work order para escrever
        """
        # Usa orderNo como nome do arquivo
        filename = f"{work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        # Escreve o JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(work_order, f, indent=2)
        
        logger.info(f"✅ Escrito: {filename}")


# ====== ADICIONE ESTA PARTE ======
if __name__ == "__main__":
    """Teste rápido do adapter"""
    print("🧪 Testando ClientAdapter...\n")
    
    # Criar adapter
    adapter = ClientAdapter()
    
    # Ler JSONs
    work_orders = adapter.read_inbound_files()
    
    # Mostrar resultado
    print(f"\n📊 Total lido: {len(work_orders)} work orders")
    
    if work_orders:
        print("\n📄 Primeira work order:")
        print(json.dumps(work_orders[0], indent=2))