import sys
sys.path.insert(0, '.')

from service.inbound_service import InboundService
from service.outbound_service import OutboundService


def run_pipeline():
    
    print("\n" + "="*60)
    print(" TRACTIAN - Sistema de Integração")
    print("="*60)
    
    print("\n" + "="*60)
    print(" ETAPA 1: INBOUND (Cliente > TracOS)")
    print("="*60 + "\n")
    
    try:
        inbound = InboundService()
        inbound.process()
        inbound.close()
    except Exception as e:
        print(f" Erro no fluxo INBOUND: {e}")
    
    print("\n" + "="*60)
    print(" ETAPA 2: OUTBOUND (TracOS > Cliente)")
    print("="*60 + "\n")
    
    try:
        outbound = OutboundService()
        outbound.process()
        outbound.close()
    except Exception as e:
        print(f" Erro no fluxo OUTBOUND: {e}")
    
    print("\n" + "="*60)
    print(" PIPELINE COMPLETO!")
    print("="*60)
<<<<<<< HEAD
=======
    print("""


>>>>>>> 559fbfc373304c439ec0cc12cbc2bb09ec03c2d6

if __name__ == "__main__":
    run_pipeline()
