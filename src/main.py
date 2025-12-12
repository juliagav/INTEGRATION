import sys
sys.path.insert(0, '.')

from service.inbound_service import InboundService
from service.outbound_service import OutboundService


def run_pipeline():
    """Executa o fluxo completo: Inbound > Outbound"""
    
    print("\n" + "="*60)
    print(" TRACTIAN - Sistema de Integração")
    print("="*60)
    
    # ==INBOUND==
    # Cliente > TracOS (JSON > MongoDB)
    print("\n" + "="*60)
    print(" ETAPA 1: INBOUND (Cliente > TracOS)")
    print("="*60 + "\n")
    
    try:
        inbound = InboundService()
        inbound.process()
        inbound.close()
    except Exception as e:
        print(f" Erro no fluxo INBOUND: {e}")
    
    # ==OUTBOUND==
    # TracOS > Cliente (MongoDB > JSON)
    print("\n" + "="*60)
    print(" ETAPA 2: OUTBOUND (TracOS > Cliente)")
    print("="*60 + "\n")
    
    try:
        outbound = OutboundService()
        outbound.process()
        outbound.close()
    except Exception as e:
        print(f" Erro no fluxo OUTBOUND: {e}")
    
    # ==RESUMO==
    print("\n" + "="*60)
    print(" PIPELINE COMPLETO!")
    print("="*60)
    print("""
 Resumo do que foi executado:
   1. INBOUND:  Leu JSONs de data/inbound/ > Validou > Traduziu > Salvou no MongoDB
   2. OUTBOUND: Buscou do MongoDB (isSynced=false) > Traduziu > Escreveu em data/outbound/
    """)


if __name__ == "__main__":
    run_pipeline()