# service/outbound_service.py
import sys
sys.path.insert(0, '.')

from outbound_query import OutboundQuery
from src.translators.tracos_to_client import TracOSToClientTranslator
import json
from pathlib import Path


class OutboundService:
    """Processa fluxo outbound: TracOS → Cliente"""
    
    def __init__(self):
        self.query = OutboundQuery()
        self.translator = TracOSToClientTranslator()
        self.outbound_dir = Path("./data/outbound")
        self.outbound_dir.mkdir(parents=True, exist_ok=True)
    
    def write_json(self, work_order: dict) -> bool:
        """Escreve JSON em data/outbound/"""
        filename = f"{work_order['orderNo']}.json"
        file_path = self.outbound_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(work_order, f, indent=2)
            
            print(f"✅ Escrito: {filename}")
            return True
        
        except PermissionError:
            print(f"❌ Sem permissão para escrever: {filename}")
            return False
        
        except OSError as e:
            print(f"❌ Erro de I/O ao escrever {filename}: {e}")
            return False
        
        except Exception as e:
            print(f"❌ Erro inesperado ao escrever {filename}: {e}")
            return False
    
    def process(self):
        """Executa fluxo outbound completo"""
        print("🚀 Iniciando fluxo OUTBOUND\n")
        
        # 1. Buscar não sincronizadas
        unsynced = self.query.get_unsynced_work_orders()
        
        if not unsynced:
            print("\n✅ Nenhuma work order para sincronizar!")
            return
        
        print(f"\n📋 Processando {len(unsynced)} work orders...\n")
        
        sucesso = 0
        falha = 0
        
        # 2. Para cada work order
        for tracos_wo in unsynced:
            try:
                # Remove _id
                if '_id' in tracos_wo:
                    del tracos_wo['_id']
                
                # 3. Traduzir
                client_wo = self.translator.translate(tracos_wo)
                
                # 4. Escrever JSON
                if self.write_json(client_wo):
                    # 5. Marcar como sincronizada (só se escreveu com sucesso)
                    self.query.mark_as_synced(tracos_wo['number'])
                    sucesso += 1
                else:
                    falha += 1
                
            except Exception as e:
                print(f"❌ Erro ao processar #{tracos_wo.get('number')}: {e}")
                falha += 1
        
        print(f"\n✅ Fluxo OUTBOUND concluído!")
        print(f"📊 Resultado: {sucesso} sucesso, {falha} falha")
    
    def close(self):
        """Fecha conexão"""
        self.query.close()


if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTE COMPLETO: OUTBOUND SERVICE")
    print("="*60 + "\n")
    
    service = OutboundService()
    service.process()
    service.close()