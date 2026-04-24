"""
SPEACE Swarm - Multi-Instance e Replica
Versione: 1.0
Data: 24 Aprile 2026
"""

import uuid
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger("SwarmNode")


@dataclass
class NodeInfo:
    """Informazioni su un nodo nello swarm"""
    node_id: str
    role: str  # cortex, edge, iot, relay
    url: Optional[str] = None
    capabilities: List[str] = None
    status: str = "unknown"
    last_heartbeat: Optional[str] = None
    c_index: float = 0.0

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


class SwarmNode:
    """
    Nodo SPEACE nello swarm distribuito.
    Può operare come:
    - cortex: nodo principale con tutti i comparti
    - edge: nodo edge con percezione locale
    - iot: nodo IoT con sensori/attuatori
    - relay: nodo per comunicazione tra nodi
    """

    def __init__(self, role: str = "cortex", node_id: Optional[str] = None):
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.role = role
        self.peers: Dict[str, NodeInfo] = {}
        self.message_queue: List[Dict] = []
        self.max_peers = 50

    def register_peer(self, peer_url: str, peer_info: Optional[Dict] = None) -> bool:
        """Registra un peer nello swarm"""
        if len(self.peers) >= self.max_peers:
            logger.warning(f"Max peers reached ({self.max_peers}), cannot register more")
            return False

        peer_id = peer_info.get("node_id", peer_url.split("//")[-1].split(":")[0]) if peer_info else peer_url
        self.peers[peer_id] = NodeInfo(
            node_id=peer_id,
            role=peer_info.get("role", "edge") if peer_info else "unknown",
            url=peer_url,
            capabilities=peer_info.get("capabilities", []) if peer_info else [],
            status="active",
            last_heartbeat=datetime.now().isoformat()
        )
        logger.info(f"🔗 Peer registered: {peer_id} ({self.peers[peer_id].role})")
        return True

    def unregister_peer(self, peer_id: str) -> bool:
        """Rimuove un peer dallo swarm"""
        if peer_id in self.peers:
            del self.peers[peer_id]
            logger.info(f"🔌 Peer unregistered: {peer_id}")
            return True
        return False

    def get_peer_status(self, peer_id: str) -> Optional[Dict]:
        """Ritorna status di un peer"""
        if peer_id not in self.peers:
            return None
        peer = self.peers[peer_id]
        return {
            "node_id": peer.node_id,
            "role": peer.role,
            "status": peer.status,
            "last_heartbeat": peer.last_heartbeat,
            "c_index": peer.c_index,
            "capabilities": peer.capabilities
        }

    def list_peers(self, role_filter: Optional[str] = None) -> List[Dict]:
        """Lista tutti i peer, opzionalmente filtrati per ruolo"""
        peers = list(self.peers.values())
        if role_filter:
            peers = [p for p in peers if p.role == role_filter]
        return [
            {
                "node_id": p.node_id,
                "role": p.role,
                "status": p.status,
                "capabilities": p.capabilities
            }
            for p in peers
        ]

    async def broadcast_message(self, message: Dict, target_role: Optional[str] = None):
        """Broadcast un messaggio a tutti i peer o solo a quelli con un certo ruolo"""
        targets = self.list_peers(role_filter=target_role) if target_role else self.list_peers()

        for target in targets:
            logger.debug(f"Broadcast to {target['node_id']}: {message.get('type', 'unknown')}")

        # In produzione, usare NATS o gRPC per comunicazione reale
        # Questa è una simulazione per ora
        self.message_queue.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "targets": [t["node_id"] for t in targets],
            "broadcast": target_role is None
        })

    def update_heartbeat(self, peer_id: str, c_index: float = 0.0):
        """Aggiorna heartbeat di un peer"""
        if peer_id in self.peers:
            self.peers[peer_id].last_heartbeat = datetime.now().isoformat()
            self.peers[peer_id].c_index = c_index
            self.peers[peer_id].status = "active"

    def get_swarm_status(self) -> Dict[str, Any]:
        """Ritorna status completo dello swarm"""
        peers_by_role = {}
        for peer in self.peers.values():
            if peer.role not in peers_by_role:
                peers_by_role[peer.role] = 0
            peers_by_role[peer.role] += 1

        return {
            "node_id": self.node_id,
            "role": self.role,
            "total_peers": len(self.peers),
            "peers_by_role": peers_by_role,
            "queue_size": len(self.message_queue),
            "timestamp": datetime.now().isoformat()
        }


class SwarmOrchestrator:
    """
    Orchestrator per gestire swarm di nodi SPEACE.
    Implementa discovery, health monitoring e task routing.
    """

    def __init__(self, local_node: Optional[SwarmNode] = None):
        self.local_node = local_node or SwarmNode(role="cortex")
        self.health_check_interval = 30  # secondi
        self.running = False

    async def start(self):
        """Avvia l'orchestrator dello swarm"""
        self.running = True
        logger.info(f"Swarm Orchestrator started with node {self.local_node.node_id} ({self.local_node.role})")

        while self.running:
            await self._health_check()
            await asyncio.sleep(self.health_check_interval)

    async def stop(self):
        """Ferma l'orchestrator"""
        self.running = False
        logger.info("Swarm Orchestrator stopped")

    async def _health_check(self):
        """Verifica salute di tutti i peer"""
        now = datetime.now()
        stale_threshold = 120  # secondi

        for peer_id, peer in list(self.local_node.peers.items()):
            if peer.last_heartbeat:
                last = datetime.fromisoformat(peer.last_heartbeat)
                if (now - last).total_seconds() > stale_threshold:
                    peer.status = "stale"
                    logger.warning(f"Peer {peer_id} is stale (no heartbeat for {(now - last).total_seconds():.0f}s)")

    async def discover_peers(self, discovery_method: str = "manual"):
        """
        Scopri nuovi peer nello swarm.
        Metodi: manual, mDNS, bootstrap_nodes
        """
        if discovery_method == "manual":
            logger.info("Manual peer discovery - use register_peer() to add peers")
        # In produzione implementare: mDNS, gossip protocol, bootstrap nodes

    def get_discovery_info(self) -> Dict[str, Any]:
        """Ritorna informazioni di discovery per altri nodi"""
        return {
            "node_id": self.local_node.node_id,
            "role": self.local_node.role,
            "capabilities": ROLE_CAPABILITIES.get(self.local_node.role, []),
            "bootstrap_urls": []  # In produzione: lista di nodi noti
        }


# Utility per Node roles
ROLE_CAPABILITIES = {
    "cortex": ["all_comparti", "neural_bridge", "learning_core", "digital_dna"],
    "edge": ["perception", "local_processing", "caching"],
    "iot": ["sensors", "actuators", "real_time_data"],
    "relay": ["message_routing", "protocol_translation", "caching"]
}


if __name__ == "__main__":
    # Test Swarm Node
    print("=" * 60)
    print("SPEACE Swarm Node - Test")
    print("=" * 60)

    # Crea nodo locale
    local = SwarmNode(role="cortex", node_id="cortex_main")
    print(f"Local node: {local.node_id} ({local.role})")

    # Registra alcuni peer
    local.register_peer("http://192.168.1.100:8000", {"node_id": "edge_001", "role": "edge"})
    local.register_peer("http://192.168.1.101:8000", {"node_id": "iot_001", "role": "iot"})

    # Mostra peer
    print(f"\nRegistered peers: {len(local.peers)}")
    for peer in local.list_peers():
        print(f"  - {peer['node_id']} ({peer['role']})")

    # Status swarm
    print(f"\nSwarm status:")
    print(json.dumps(local.get_swarm_status(), indent=2))