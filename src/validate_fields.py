
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


async def main():
    print(" Testando Validação...\n")
    
    adapter = ClientAdapter()
    
    # Teste 1: VÁLIDA
    print("Teste 1: Work order VÁLIDA")
    valid_wo = {
        "orderNo": 1,
        "summary": "Test",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    result = adapter.validate_work_order(valid_wo)
    print(f"Resultado: {result}\n")
    
    # Teste 2: INVÁLIDA (falta campo)
    print("Teste 2: Work order INVÁLIDA (falta campo)")
    invalid_wo = {
        "orderNo": 2,
        "summary": "Test"
    }
    result = adapter.validate_work_order(invalid_wo)
    print(f"Resultado: {result}\n")
    
    # Teste 3: INVÁLIDA (campo vazio)
    print("Teste 3: Work order INVÁLIDA (campo vazio)")
    empty_wo = {
        "orderNo": 3,
        "summary": "",
        "creationDate": "2024-12-08T10:00:00Z",
        "lastUpdateDate": "2024-12-08T11:00:00Z"
    }
    result = adapter.validate_work_order(empty_wo)
    print(f"Resultado: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())