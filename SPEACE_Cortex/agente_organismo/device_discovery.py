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
