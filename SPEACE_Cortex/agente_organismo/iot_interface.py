"""
IoT Interface per Agente Organismico
REST API + WebSocket per connessione dispositivi IoT

Versione: 1.0
Data: 2026-04-17
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoT-Interface")


class ConnectionProtocol(Enum):
    """Protocolli di connessione supportati"""
    HTTP_REST = "http_rest"
    WEBSOCKET = "websocket"
    MQTT = "mqtt"
    COAP = "coap"


@dataclass
class IoTDevice:
    """Dispositivo IoT registrato"""
    device_id: str
    device_type: str
    protocol: ConnectionProtocol
    endpoint: str
    status: str = "offline"
    last_seen: str = ""
    capabilities: List[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


class IoTInterface:
    """
    Interfaccia IoT per Agente Organismico.
    Gestisce connessioni REST/WebSocket con dispositivi fisici.
    """

    def __init__(self):
        self.devices: Dict[str, IoTDevice] = {}
        self.subscribers: List[Callable] = []
        self.message_buffer: List[Dict[str, Any]] = []
        self.version = "1.0"
        logger.info("IoT Interface initialized (v1.0)")

    # === Device Management ===

    def register_device(self, device: IoTDevice) -> bool:
        """
        Registra un nuovo dispositivo IoT.
        """
        if device.device_id in self.devices:
            logger.warning(f"Device {device.device_id} already registered")
            return False

        self.devices[device.device_id] = device
        logger.info(f"Device registered: {device.device_id} ({device.device_type})")
        return True

    def unregister_device(self, device_id: str) -> bool:
        """Rimuove un dispositivo"""
        if device_id in self.devices:
            del self.devices[device_id]
            logger.info(f"Device unregistered: {device_id}")
            return True
        return False

    def get_device(self, device_id: str) -> Optional[IoTDevice]:
        """Ottiene info dispositivo"""
        return self.devices.get(device_id)

    def list_devices(self, device_type: Optional[str] = None) -> List[IoTDevice]:
        """Lista dispositivi, opzionalmente filtrati per tipo"""
        devices = list(self.devices.values())
        if device_type:
            devices = [d for d in devices if d.device_type == device_type]
        return devices

    # === Data Fetching ===

    def fetch_sensor_data(self, device_id: str, sensor_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch data da sensore specifico.
        In implementation reale, farà HTTP request al dispositivo.
        """
        device = self.get_device(device_id)
        if not device:
            logger.error(f"Device not found: {device_id}")
            return None

        # Simulation: return dummy data
        # In produzione: HTTP GET {endpoint}/sensors/{sensor_name}
        return {
            "device_id": device_id,
            "sensor": sensor_name,
            "value": 0.0,
            "unit": "unknown",
            "timestamp": datetime.now().isoformat(),
            "status": "simulated"
        }

    def fetch_all_sensors(self, device_id: str) -> List[Dict[str, Any]]:
        """Fetch tutti i sensori di un dispositivo"""
        device = self.get_device(device_id)
        if not device:
            return []

        # Simulation: return list of sensor readings
        return [
            {
                "sensor": f"sensor_{i}",
                "value": 0.0,
                "unit": "unknown",
                "timestamp": datetime.now().isoformat()
            }
            for i in range(3)
        ]

    # === WebSocket Streaming (Stub) ===

    def subscribe(self, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe a streaming data"""
        self.subscribers.append(callback)
        logger.info(f"Subscription added. Total: {len(self.subscribers)}")

    def unsubscribe(self, callback: Callable):
        """Unsubscribe"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def broadcast(self, data: Dict[str, Any]):
        """Broadcast data a tutti i subscribers"""
        for subscriber in self.subscribers:
            try:
                subscriber(data)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")

    # === REST API Endpoints (Stub for Flask/FastAPI) ===

    def get_endpoints(self) -> Dict[str, str]:
        """
        Restituisce schema endpoint REST.
        Da implementare con Flask/FastAPI in production.
        """
        return {
            "/iot/devices": "GET - Lista dispositivi",
            "/iot/devices/<id>": "GET - Info dispositivo",
            "/iot/devices/<id>/sensors": "GET - Lista sensori",
            "/iot/devices/<id>/sensors/<name>": "GET - Lettura sensore",
            "/iot/subscribe": "WebSocket - Streaming data"
        }

    # === Auto-Discovery (Stub) ===

    def discover_devices(self, network_range: str = "192.168.1.0/24") -> List[IoTDevice]:
        """
        Auto-discovery dispositivi nella rete.
        In implementation reale, farà scanning network.
        """
        logger.info(f"Auto-discovery started: {network_range}")

        # Simulation: return empty list
        # In produzione: mDNS, SSDP, or network scan
        discovered = []

        logger.info(f"Auto-discovery complete. Found: {len(discovered)} devices")
        return discovered

    # === Status ===

    def get_status(self) -> Dict[str, Any]:
        """Status dell'interfaccia IoT"""
        return {
            "version": self.version,
            "devices_registered": len(self.devices),
            "devices_online": len([d for d in self.devices.values() if d.status == "online"]),
            "subscribers_count": len(self.subscribers),
            "message_buffer_size": len(self.message_buffer)
        }


# Example device factory
def create_iot_device(
    device_id: str,
    device_type: str,
    protocol: str = "http_rest",
    endpoint: str = "http://localhost:8080"
) -> IoTDevice:
    """Factory per creare dispositivi IoT"""
    return IoTDevice(
        device_id=device_id,
        device_type=device_type,
        protocol=ConnectionProtocol(protocol),
        endpoint=endpoint,
        status="offline"
    )


if __name__ == "__main__":
    # Test IoT Interface
    print("IoT Interface v1.0 - Test")

    iot = IoTInterface()

    # Register dummy devices
    devices = [
        create_iot_device("temp_sensor_01", "thermal", "http_rest", "http://192.168.1.100:8080"),
        create_iot_device("air_sensor_01", "olfactory", "http_rest", "http://192.168.1.101:8080"),
    ]

    for device in devices:
        iot.register_device(device)

    # List devices
    print(f"\nRegistered devices: {len(iot.list_devices())}")

    # Get status
    status = iot.get_status()
    print(json.dumps(status, indent=2))
