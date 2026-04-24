"""
Device Discovery per Agente Organismico
Auto-discovery di sensori e dispositivi IoT

Versione: 1.0
Data: 2026-04-17
"""

import logging
import socket
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Device-Discovery")


@dataclass
class DiscoveredDevice:
    """Dispositivo scoperto tramite auto-discovery"""
    ip_address: str
    port: int
    device_type: str
    manufacturer: Optional[str] = None
    capabilities: List[str] = None
    protocol: str = "http"

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


class DeviceDiscovery:
    """
    Auto-discovery per dispositivi IoT.
    Supporta: mDNS, SSDP, network scan, manual configuration.
    """

    def __init__(self):
        self.discovered_devices: List[DiscoveredDevice] = []
        self.last_scan: str = ""
        self.version = "1.0"
        logger.info("Device Discovery initialized (v1.0)")

    # === Network Scanning (Stub) ===

    def scan_network(self, ip_range: str = "192.168.1.0/24") -> List[DiscoveredDevice]:
        """
        Scansiona la rete per dispositivi IoT.
        In implementation reale: TCP connect scan, mDNS, SSDP.
        """
        logger.info(f"Network scan started: {ip_range}")

        # Simulation: return simulated devices
        # In produzione: scan common ports (80, 8080, 443, 1883 for MQTT)
        discovered = [
            DiscoveredDevice(
                ip_address="192.168.1.100",
                port=8080,
                device_type="thermal_sensor",
                manufacturer="Simulated",
                capabilities=["temperature", "humidity"]
            ),
            DiscoveredDevice(
                ip_address="192.168.1.101",
                port=8080,
                device_type="air_quality_sensor",
                manufacturer="Simulated",
                capabilities=["VOC", "CO2", "particles"]
            )
        ]

        self.discovered_devices = discovered
        self.last_scan = datetime.now().isoformat()

        logger.info(f"Network scan complete. Found: {len(discovered)} devices")
        return discovered

    # === mDNS Discovery (Stub) ===

    def mdns_discover(self, service_type: str = "_iot._tcp") -> List[DiscoveredDevice]:
        """
        Discover devices via mDNS/Bonjour.
        Common service types:
        - _hue._tcp (Philips Hue)
        - _airplay._tcp (Apple TV)
        - _printer._tcp (Printers)
        """
        logger.info(f"mDNS discovery for: {service_type}")

        # Stub: return empty
        # In produzione: python-zeroconf library
        return []

    # === SSDP Discovery (Stub) ===

    def ssdp_discover(self) -> List[DiscoveredDevice]:
        """
        Discover devices via SSDP (Simple Service Discovery Protocol).
        Used by SmartTVs, Xbox, etc.
        """
        logger.info("SSDP discovery started")

        # Stub: return empty
        # In produzione: requests-ssdp or similar
        return []

    # === Manual Configuration ===

    def add_manual_device(self, device: DiscoveredDevice) -> bool:
        """Aggiunge dispositivo manualmente"""
        if device.ip_address in [d.ip_address for d in self.discovered_devices]:
            logger.warning(f"Device already discovered: {device.ip_address}")
            return False

        self.discovered_devices.append(device)
        logger.info(f"Manual device added: {device.ip_address}")
        return True

    # === Device Testing ===

    def test_device_connection(self, device: DiscoveredDevice) -> bool:
        """
        Testa connessione a dispositivo.
        Returns True se il dispositivo risponde.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((device.ip_address, device.port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"Connection test failed for {device.ip_address}: {e}")
            return False

    # === Status ===

    def get_status(self) -> Dict[str, Any]:
        """Status del discovery"""
        return {
            "version": self.version,
            "devices_discovered": len(self.discovered_devices),
            "last_scan": self.last_scan,
            "capabilities": ["network_scan", "mdns", "ssdp", "manual"]
        }


# =============================================================================
# ORGANISM DEVICE DISCOVERY - Enhanced per SPEACE
# =============================================================================
"""
SPEACE Organismica IoT - Device Discovery e Assimilazione Automatica
Versione: 2.0
Data: 24 Aprile 2026
"""

import json
import asyncio
from pathlib import Path


class OrganismDeviceDiscovery:
    """
    Scopre, classifica e assimila dispositivi nell'ambiente informatico di SPEACE.
    Funziona come "sistema immunitario" che integra nuovi dispositivi nel grafo computazionale.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.discovered_devices: Dict[str, Dict] = {}
        self.assimilated_devices: Dict[str, Dict] = {}
        self.max_devices = 100

    async def discover_environment(self) -> Dict[str, Any]:
        """Riconosce il contesto e tenta di scoprire dispositivi nella rete."""
        context = {
            "environment_type": "unknown",
            "devices_found": len(self.discovered_devices),
            "devices_assimilated": len(self.assimilated_devices),
            "capabilities": [],
            "timestamp": datetime.now().isoformat()
        }

        context["environment_type"] = self._classify_environment(list(self.discovered_devices.values()))

        for device in self.assimilated_devices.values():
            if "capabilities" in device:
                context["capabilities"].extend(device["capabilities"])

        context["capabilities"] = list(set(context["capabilities"]))
        return context

    def _classify_environment(self, devices: List[Dict]) -> str:
        if not devices:
            return "general_lab"

        device_names = [d.get("name", "").lower() for d in devices]
        device_types = [d.get("type", "").lower() for d in devices]
        combined = " ".join(device_names + device_types)

        if any(kw in combined for kw in ["plc", "scada", "industrial", "machinery"]):
            return "industrial_4.0"
        if any(kw in combined for kw in ["camera", "traffic", "sensor", "environmental"]):
            return "smart_city"
        if any(kw in combined for kw in ["medical", "patient", "vital"]):
            return "healthcare"
        if any(kw in combined for kw in ["light", "thermostat", "smart", "bulb"]):
            return "smart_home"

        return "general_lab"

    async def scan_for_devices(self) -> List[Dict]:
        """Scansiona la rete per dispositivi (simulato per ora)."""
        discovered = []

        simulated_devices = [
            {"id": "local_sensor_001", "name": "Temperatura Ambiente", "type": "temperature_sensor",
             "capabilities": ["temperature", "humidity"], "location": "lab", "status": "active"},
            {"id": "local_actuator_001", "name": "LED Indicator", "type": "led_actuator",
             "capabilities": ["visual_output", "status_led"], "location": "lab", "status": "active"},
            {"id": "local_api_001", "name": "OpenWeatherMap API", "type": "weather_api",
             "capabilities": ["weather_data", "forecasts"], "location": "cloud", "status": "active"}
        ]

        for device in simulated_devices:
            if device["id"] not in self.discovered_devices:
                self.discovered_devices[device["id"]] = device
                discovered.append(device)
                logger.info(f"🔍 Discovered device: {device['name']} ({device['type']})")

        return discovered

    async def assimilate_device(self, device_info: Dict[str, Any]) -> Dict[str, Any]:
        """Assorbe il dispositivo nel grafo computazionale di SPEACE."""
        device_id = device_info.get("id", f"device_{len(self.assimilated_devices)}")

        assimilation_result = {
            "status": "assimilated",
            "id": device_id,
            "name": device_info.get("name", "Unknown"),
            "type": device_info.get("type", "generic"),
            "assimilated_at": datetime.now().isoformat(),
            "integration_status": "pending"
        }

        device_type = device_info.get("type", "").lower()
        if "sensor" in device_type or "actuator" in device_type:
            assimilation_result["integration_type"] = "parietal_lobe"
            assimilation_result["comparti_target"] = "parietal_lobe"
        elif "api" in device_type or "cloud" in device_type:
            assimilation_result["integration_type"] = "perception_module"
            assimilation_result["comparti_target"] = "perception_module"
        elif "camera" in device_type or "vision" in device_type:
            assimilation_result["integration_type"] = "perception_module"
            assimilation_result["comparti_target"] = "perception_module"
        else:
            assimilation_result["integration_type"] = "general"
            assimilation_result["comparti_target"] = "cerebellum"

        self.assimilated_devices[device_id] = assimilation_result
        logger.info(f"🧬 Assimilated device: {device_info.get('name')} → {assimilation_result['integration_type']}")

        return assimilation_result

    async def get_device_status(self, device_id: str) -> Optional[Dict]:
        return self.assimilated_devices.get(device_id)

    async def list_assimilated_devices(self) -> List[Dict]:
        return list(self.assimilated_devices.values())

    async def remove_device(self, device_id: str) -> bool:
        if device_id in self.assimilated_devices:
            del self.assimilated_devices[device_id]
            logger.info(f"🗑️ Device removed: {device_id}")
            return True
        return False

    def get_environment_summary(self) -> Dict[str, Any]:
        return {
            "environment_type": self._classify_environment(list(self.discovered_devices.values())),
            "total_discovered": len(self.discovered_devices),
            "total_assimilated": len(self.assimilated_devices),
            "devices_by_type": self._count_by_type(self.assimilated_devices),
            "last_discovery": datetime.now().isoformat()
        }

    def _count_by_type(self, devices: Dict) -> Dict[str, int]:
        counts = {}
        for device in devices.values():
            dev_type = device.get("type", "unknown")
            counts[dev_type] = counts.get(dev_type, 0) + 1
        return counts


class DeviceRegistry:
    """
    Registro centrale di tutti i dispositivi IoT assimilati.
    Persiste su disco per sopravvivenza tra sessioni.
    """

    def __init__(self, registry_path: str = "data/device_registry.json"):
        self.registry_path = Path(registry_path)
        self.devices: Dict[str, Dict] = {}
        self.load()

    def load(self):
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    self.devices = json.load(f)
                logger.info(f"📁 Device registry loaded: {len(self.devices)} devices")
            except Exception as e:
                logger.error(f"Errore loading device registry: {e}")
                self.devices = {}

    def save(self):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self.devices, f, indent=2, default=str)
            logger.info(f"💾 Device registry saved: {len(self.devices)} devices")
        except Exception as e:
            logger.error(f"Errore saving device registry: {e}")

    def register(self, device_id: str, device_info: Dict):
        self.devices[device_id] = device_info
        self.save()

    def unregister(self, device_id: str) -> bool:
        if device_id in self.devices:
            del self.devices[device_id]
            self.save()
            return True
        return False

    def get_all(self) -> Dict[str, Dict]:
        return self.devices

    def get_by_type(self, device_type: str) -> List[Dict]:
        return [d for d in self.devices.values() if d.get("type") == device_type]

    def get_active_count(self) -> int:
        return len([d for d in self.devices.values() if d.get("status") == "active"])


if __name__ == "__main__":
    # Test Device Discovery
    print("Device Discovery v1.0 - Test")

    discovery = DeviceDiscovery()

    # Scan network
    devices = discovery.scan_network()
    print(f"\nDiscovered {len(devices)} devices:")

    for device in devices:
        print(f"  - {device.ip_address}:{device.port} ({device.device_type})")

    # Test connection
    if devices:
        test_result = discovery.test_device_connection(devices[0])
        print(f"\nConnection test: {'OK' if test_result else 'FAILED'}")
