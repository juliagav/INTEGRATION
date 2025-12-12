
from pathlib import Path
from typing import Dict

class ClientAdapter:
    """Lê e escreve arquivos JSON do sistema do cliente"""
    
    REQUIRED_FIELDS = ["orderNo", "summary", "creationDate", "lastUpdateDate"]
    
    def __init__(self):
        self.inbound_dir = Path("./data/inbound")
        self.outbound_dir = Path("./data/outbound")
    
    def validate_work_order(self, work_order: dict) -> bool:
        """Valida se a work order tem todos os campos obrigatórios"""
        
        # Para cada campo obrigatório 
        for field in self.REQUIRED_FIELDS:
            
            # VALIDAÇÃO 1: Verifica se o campo existe
            if field not in work_order:
                print(f" Campo obrigatório faltando: {field}")
                return False
            
            # VALIDAÇÃO 2: Verifica se o campo não está vazio
            if work_order[field] is None or work_order[field] == "":
                print(f" Campo obrigatório vazio: {field}")
                return False
        
        # Se passou em todas as validações
        print(f" Validação OK para orderNo #{work_order.get('orderNo')}")
        return True
