import json
import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class ClientAdapter:
   
    """Lê e escreve arquivos JSON do sistema do cliente"""
    REQUIRED_FIELDS = ["orderNo", "summary", "creationDate", "lastUpdateDate"]
    
    def __init__(self):
        self.inbound_dir = Path(os.getenv("DATA_INBOUND_DIR", "./data/inbound"))
        self.outbound_dir = Path(os.getenv("DATA_OUTBOUND_DIR", "./data/outbound"))
    
    def validate_work_order(self, work_order: Dict) -> bool:
        """Validando se a work order tem todos os campos obrigatórios"""
        for field in self.REQUIRED_FIELDS:
            if field not in work_order:
                print(f" Campo obrigatório faltando: {field}")
                return False
            
            if work_order[field] is None or work_order[field] == "":
                print(f" Campo obrigatório vazio: {field}")
                return False
        
        print(f"✅ Validação OK para orderNo #{work_order.get('orderNo')}")
        return True
    
    def read_inbound_files(self) -> List[Dict]:
        """Lê todos os arquivos JSON da pasta inbound"""
        work_orders = []
        
        if not self.inbound_dir.exists():
            print(f" Diretório não encontrado: {self.inbound_dir}")
            return work_orders
        
        json_files = list(self.inbound_dir.glob("*.json"))
        print(f" Encontrados {len(json_files)} arquivos JSON")
        
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if self.validate_work_order(data):
                    work_orders.append(data)
                    print(f" Lido e validado: {file_path.name}")
                else:
                    print(f" Arquivo ignorado (campos inválidos): {file_path.name}")
            
            except json.JSONDecodeError:
                print(f" Arquivo corrompido (JSON inválido): {file_path.name}")
            
            except PermissionError:
                print(f" Sem permissão para ler: {file_path.name}")
            
            except Exception as e:
                print(f" Erro inesperado ao ler {file_path.name}: {e}")
        
        return work_orders
    
    def write_outbound_file(self, work_order: Dict) -> bool:
        """Escreve uma work order como JSON na pasta outbound"""
        try:
            self.outbound_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{work_order['orderNo']}.json"
            file_path = self.outbound_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(work_order, f, indent=2)
            
            print(f" Escrito: {filename}")
            return True
        
        except PermissionError:
            print(f" Sem permissão para escrever: {filename}")
            return False
        
        except Exception as e:
            print(f" Erro ao escrever: {e}")
            return False