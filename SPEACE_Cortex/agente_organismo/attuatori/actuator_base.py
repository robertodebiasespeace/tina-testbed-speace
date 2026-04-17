"""
Actuator Base Class
Classe base per attuatori (motori, valvole, relais)

Versione: 1.0
Data: 2026-04-17
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class ActuatorCommand:
    """Comando per attuatore"""
    command_id: str
    actuator_type: str
    action: str
    parameters: Dict[str, Any]
    timestamp: str
    status: str = "pending"
    executed_by: Optional[str] = None


class ActuatorBase(ABC):
    """
    Base class per tutti gli attuatori.
    Futura implementazione: robot arms, valves, relays, drones.
    """

    def __init__(self, actuator_id: str, actuator_type: str):
        self.actuator_id = actuator_id
        self.actuator_type = actuator_type
        self.status = "idle"
        self.last_command: Optional[ActuatorCommand] = None
        self.position = 0.0
        self.version = "1.0"

    @abstractmethod
    def execute(self, command: ActuatorCommand) -> bool:
        """Esegue comando sull'attuatore"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Restituisce stato attuatore"""
        pass

    def validate_command(self, command: ActuatorCommand) -> bool:
        """Valida comando prima di esecuzione"""
        required_fields = ["command_id", "action", "parameters"]
        return all(field in command.parameters or hasattr(command, field) for field in required_fields)


if __name__ == "__main__":
    # Example of concrete implementation
    print("ActuatorBase is abstract - implement in concrete classes")
