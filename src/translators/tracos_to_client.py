from datetime import datetime
from typing import Dict


class TracOSToClientTranslator:
    """Traduz do formato TracOS → Cliente"""
    
    def translate(self, tracos_data: Dict) -> Dict:
     
        # Calcula booleanos baseado no status
        status_flags = self._calculate_status_flags(tracos_data.get("status", "in_progress"))
        
        # Monta dados no formato Cliente
        client_data = {
            "orderNo": tracos_data["number"],
            "isActive": True,
            "isCanceled": status_flags["isCanceled"],
            "isDeleted": tracos_data.get("deleted", False),
            "isDone": status_flags["isDone"],
            "isOnHold": status_flags["isOnHold"],
            "isPending": status_flags["isPending"],
            "isSynced": True,
            "summary": tracos_data["title"],
            "creationDate": self._format_date(tracos_data["createdAt"]),
            "lastUpdateDate": self._format_date(tracos_data["updatedAt"]),
            "deletedDate": self._format_date(tracos_data.get("deletedAt")) if tracos_data.get("deletedAt") else None,
        }
        
        return client_data
    
    def _calculate_status_flags(self, status: str) -> Dict[str, bool]:
        """Converte status TracOS em booleanos do cliente"""
        flags = {
            "isCanceled": False,
            "isDone": False,
            "isOnHold": False,
            "isPending": False,
        }
        
        if status == "cancelled":
            flags["isCanceled"] = True
        elif status == "completed":
            flags["isDone"] = True
        elif status == "on_hold":
            flags["isOnHold"] = True
        elif status == "pending":
            flags["isPending"] = True
        
        return flags
    
    def _format_date(self, date_value) -> str:
        """Converte datetime para ISO"""
        if date_value is None:
            return None
        if isinstance(date_value, str):
            return date_value
        if isinstance(date_value, datetime):
            # Também converte para ISO no final
            return date_value.isoformat().replace('+00:00', 'Z')
        return None
      
# Definir a classe tradutora, ou seja, que converte do formato TracOS para Cliente e quem usa é o outbound_service.py