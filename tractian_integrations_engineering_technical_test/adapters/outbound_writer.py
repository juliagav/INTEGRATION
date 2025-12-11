import json
from pathlib import Path
from typing import List, Dict
from loguru import logger

from .client_adapter import ClientAdapter
from ..translators.tracos_to_client import TracOSToClientTranslator


class OutboundWriter:
    """Escreve work orders não sincronizadas no formato cliente para a pasta outbound"""
    
    def __init__(self, outbound_dir: str = "./data/outbound"):
        self.outbound_dir = Path(outbound_dir)
        self.outbound_dir.mkdir(parents=True, exist_ok=True)
        self.translator = TracOSToClientTranslator()
        self.client_adapter = ClientAdapter()
    
    def write_work_orders(self, tracos_work_orders: List[Dict]) -> None:
        """
        Escreve lista de work orders TracOS no formato Cliente para a pasta outbound
        
        Args:
            tracos_work_orders: Lista de work orders vindas do MongoDB (formato TracOS)
        """
        if not tracos_work_orders:
            logger.warning("Nenhuma work order para sincronizar no outbound")
            return
        
        for tracos_wo in tracos_work_orders:
            try:
                # Traduz de TracOS para Cliente
                client_wo = self.translator.translate(tracos_wo)
                
                # Escreve arquivo
                self._write_file(client_wo)
                
                logger.info(f"✅ Work order #{client_wo['orderNo']} escrita no outbound")
            
            except Exception as e:
                logger.error(f"❌ Erro ao escrever work order #{tracos_wo.get('number')}: {e}")
    
    def _write_file(self, client_work_order: Dict) -> None:
        """Escreve um arquivo JSON na pasta outbound"""
        filename = f"{client_work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(client_work_order, f, indent=2, default=str)
        
        logger.debug(f"📄 Arquivo escrito: {file_path}")