from typing import Protocol, List, Dict, Any

class AgentProtocol(Protocol):
    def get_response(self, message: List[Dict[str, Any]]) -> Dict[str, Any]:
        ...