from datetime import datetime
from typing import Dict


class ClientToTracOSTranslator:
    """Traduz do formato Cliente > TracOS"""
    
    def translate(self, client_data: Dict) -> Dict:
        """
        Traduz work order do cliente para TracOS
    
        Args:
            client_data: Dados do cliente (vem do JSON dinamicamente!)
            
        Returns:
            Dados no formato TracOS
        """
        # Calcula status baseado nos booleanos
        status = self._calculate_status(client_data)
        
        # Monta dados TracOS a partir dos dados RECEBIDOS
        tracos_data = {
            "number": client_data["orderNo"],
            "status": status,
            "title": client_data["summary"],
            "description": client_data["summary"],
            "createdAt": self._parse_date(client_data["creationDate"]),
            "updatedAt": self._parse_date(client_data["lastUpdateDate"]),
            "deleted": client_data.get("isDeleted", False),
            "deletedAt": self._parse_date(client_data.get("deletedDate")) if client_data.get("deletedDate") else None,
            "isSynced": False,
            "syncedAt": None
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


# Definir a classe tradutora, ou seja, que converte do formato Cliente para TracOS e quem usa é o inbound_service.py