import sys
sys.path.insert(0, '.')

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from src.outbound_query import OutboundQuery
from src.translators.tracos_to_client import TracOSToClientTranslator

load_dotenv()


class OutboundService:
    
    def __init__(self):
        self.query = OutboundQuery()
        self.translator = TracOSToClientTranslator()
        self.outbound_dir = Path(os.getenv("DATA_OUTBOUND_DIR", "./data/outbound"))
        self.outbound_dir.mkdir(parents=True, exist_ok=True)
    
    def write_json(self, work_order: dict) -> bool:
        filename = f"{work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(work_order, f, indent=2)
            
            print(f" Escrito: {filename}")
            return True
        
        except PermissionError:
            print(f" Sem permissão para escrever: {filename}")
            return False
        
        except OSError as e:
            print(f" Erro de I/O ao escrever {filename}: {e}")
            return False
        
        except Exception as e:
            print(f" Erro inesperado ao escrever {filename}: {e}")
            return False
    
    def process(self):
        print(" Iniciando fluxo OUTBOUND\n")
        
        unsynced = self.query.get_unsynced_work_orders()
        
        if not unsynced:
            print("\n Nenhuma work order para sincronizar!")
            return
        
        print(f"\n Processando {len(unsynced)} work orders...\n")
        
        sucesso = 0
        falha = 0
        
        for tracos_wo in unsynced:
            try:
                if '_id' in tracos_wo:
                    del tracos_wo['_id']
                
                client_wo = self.translator.translate(tracos_wo)
                
                if self.write_json(client_wo):
                    self.query.mark_as_synced(tracos_wo['number'])
                    sucesso += 1
                else:
                    falha += 1
                
            except Exception as e:
                print(f" Erro ao processar #{tracos_wo.get('number')}: {e}")
                falha += 1
        
        print(f"\n Fluxo OUTBOUND concluído!")
        print(f" Resultado: {sucesso} sucesso, {falha} falha")
    
    def close(self):
        self.query.close()


if __name__ == "__main__":
    print("="*60)
    print(" TESTE COMPLETO: OUTBOUND SERVICE")
    print("="*60 + "\n")
    
    service = OutboundService()
    service.process()
    service.close()