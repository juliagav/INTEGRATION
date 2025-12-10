# src/translators/client_to_tracos.py
from datetime import datetime
from typing import Dict

class ClientToTracOSTranslator:
    """Traduz do formato Cliente → TracOS"""
    
    def translate(self, client_data: Dict) -> Dict:
        """
        Traduz work order do cliente para TracOS
        
        Args:
            client_data: Dados do cliente
            
        Returns:
            Dados no formato TracOS
        """
        # Calcula status baseado nos booleanos
        status = self._calculate_status(client_data)
        
        # Monta dados TracOS
        tracos_data = {
            "number": client_data["orderNo"],
            "status": status,
            "title": client_data["summary"],
            "description": client_data["summary"],
            "createdAt": self._parse_date(client_data["creationDate"]),
            "updatedAt": self._parse_date(client_data["lastUpdateDate"]),
            "deleted": client_data.get("isDeleted", False),
            "deletedAt": self._parse_date(client_data.get("deletedDate")) if client_data.get("deletedDate") else None
        }
        
        return tracos_data
    
    def _calculate_status(self, data: Dict) -> str:
        """Calcula status TracOS baseado nos booleanos do cliente"""
        if data.get("isCanceled"):
            return "cancelled"
        elif data.get("isDone"):
            return "completed"
        elif data.get("isOnHold"):
            return "on_hold"
        elif data.get("isPending"):
            return "pending"
        else:
            return "in_progress"
    
    def _parse_date(self, date_str: str) -> datetime:
        """Converte string para datetime"""
        if not date_str:
            return datetime.utcnow()
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))


async def main():
    """Teste do tradutor"""
    print("🧪 Testando Tradutor Cliente → TracOS\n")
    
    # Dados do cliente (exemplo)
    client_wo = {
        "orderNo": 1,
        "isCanceled": False,
        "isDeleted": False,
        "isDone": False,
        "isOnHold": True,
        "isPending": False,
        "summary": "Example workorder #1",
        "creationDate": "2025-11-10T22:15:47.144481+00:00",
        "lastUpdateDate": "2025-11-10T23:15:47.144481+00:00",
        "deletedDate": None
    }
    
    # Traduzir
    translator = ClientToTracOSTranslator()
    tracos_wo = translator.translate(client_wo)
    
    # Mostrar resultado
    import json
    print("📥 ENTRADA (Cliente):")
    print(json.dumps(client_wo, indent=2))
    
    print("\n📤 SAÍDA (TracOS):")
    print(json.dumps(tracos_wo, indent=2, default=str))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())