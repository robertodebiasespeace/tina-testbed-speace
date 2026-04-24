"""
SPEACE Cortex - Registry dei 12 Comparti Cerebrali
Versione: 1.1 - Con SelfDialogue + Organism Discovery
Data: 24 Aprile 2026
"""

from .prefrontal_cortex import PrefrontalCortex
from .perception_module import PerceptionModule
from .world_model_knowledge import WorldModelKnowledge
from .hippocampus import Hippocampus
from .temporal_lobe import TemporalLobe
from .parietal_lobe import ParietalLobe
from .cerebellum import Cerebellum
from .default_mode_network import DefaultModeNetwork
from .curiosity_module import CuriosityModule
from .safety_module import SafetyModule
from .self_dialogue_agent import SelfDialogueAgent

# Organism Discovery (lazy loading con adapter)
_OrganismDeviceDiscovery = None

class OrganismDiscoveryAdapter:
    """Adapter per compatibilità con il sistema comparti"""
    def __init__(self):
        from ..agente_organismo.device_discovery import OrganismDeviceDiscovery
        self._impl = OrganismDeviceDiscovery()
        self.name = "organism_discovery"

    def set_bridge(self, bridge):
        self._impl._bridge = bridge

    async def process(self, input_data=None):
        try:
            discovered = await self._impl.discover_environment()
            return {"status": "success", "discovered": discovered}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_status(self):
        return self._impl.get_environment_summary()


def _get_organism_discovery():
    global _OrganismDeviceDiscovery
    if _OrganismDeviceDiscovery is None:
        _OrganismDeviceDiscovery = OrganismDiscoveryAdapter
    return _OrganismDeviceDiscovery


__all__ = [
    "PrefrontalCortex", "PerceptionModule", "WorldModelKnowledge",
    "Hippocampus", "TemporalLobe", "ParietalLobe", "Cerebellum",
    "DefaultModeNetwork", "CuriosityModule", "SafetyModule",
    "SelfDialogueAgent",
]

# Registry per accesso rapido dal Neural Bridge
COMPARTI_REGISTRY = {
    "prefrontal": PrefrontalCortex,
    "perception": PerceptionModule,
    "world_model": WorldModelKnowledge,
    "hippocampus": Hippocampus,
    "temporal": TemporalLobe,
    "parietal": ParietalLobe,
    "cerebellum": Cerebellum,
    "default_mode": DefaultModeNetwork,
    "curiosity": CuriosityModule,
    "safety": SafetyModule,
    "self_dialogue": SelfDialogueAgent,
}

# Comparti lazy (richiedono bridge dopo init)
COMPARTI_LAZY = {
    "organism_discovery": _get_organism_discovery,
}

# Mappa comparti -> funzione primaria
COMPARTI_FUNCTIONS = {
    "prefrontal": "Planning & Decision Making",
    "perception": "Sensori, API, IoT fetches",
    "world_model": "Modello interno realta, inferenza",
    "hippocampus": "Memory & Long-term Storage",
    "temporal": "Language, Crypto, Market Analysis",
    "parietal": "Sensory/Tools integration",
    "cerebellum": "Low-level Execution",
    "default_mode": "Reflection & Self-Improving",
    "curiosity": "Exploration & Novel Mutation",
    "safety": "Risk Gates & SafeProactive",
    "self_dialogue": "Internal Dialogue & Self-Reflection",
    "organism_discovery": "IoT Device Auto-Discovery & Assimilation",
}
