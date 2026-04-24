"""
SPEACE Neural Bridge – Integrazione tra Neural Engine e componenti SPEACE esistenti
Coordinatore del grafo computazionale che mappa i componenti SPEACE su neuroni funzionali.

Versione: 1.0
Data: 22 aprile 2026
"""

from __future__ import annotations

import sys
import time
import threading
from pathlib import Path
from typing import Any, Dict, Optional, List

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from neural_engine import (
    ComputationalGraph,
    InteropProtocol,
    create_protocol,
    SynapseManager,
    SynapticPlasticity,
    StructuralPlasticity,
    ExecutionEngine,
    EvolutionEngine,
    EnvironmentSensor,
    LoadBalancer,
    NeuronType,
    ExecutionContext,
    SignalType,
    BaseNeuron,
    NeuronFactory,
)
from neural_engine.graph_core import EdgeType

from neural_engine.wrappers.speace_neurons import (
    SafeProactiveNeuron,
    SMFOIKerneNeuron,
    WorldModelNeuron,
    ScientificTeamNeuron,
    DigitalDNANeuron,
    MemoryNeuron,
    StatusMonitorNeuron,
    AGPTNeuron,
    HermesAgentNeuron,
)

# Import 9 Comparti Cerebrali
from .comparti import COMPARTI_REGISTRY, COMPARTI_LAZY
from .world_model.knowledge_graph import KnowledgeGraph
from .cortex_orchestrator import CortexOrchestrator
from .graph_engine import GraphEngine
from .swarm.swarm_node import SwarmNode, SwarmOrchestrator
from .agente_organismo.device_discovery import OrganismDeviceDiscovery, DeviceRegistry


class SPEACENeuralBridge:
    """
    Bridge principale che integra il Neural Engine nell'architettura SPEACE.
    Crea un grafo computazionale dove ogni componente è un neurone funzionale.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        safe_proactive=None,
        smfoi_kernel=None,
        world_model=None,
        scientific_team=None,
        status_monitor=None,
    ):
        self.running = False
        self.cycle_count = 0
        self.start_time = 0.0

        # Core Neural Engine
        self.graph = ComputationalGraph(name="SPEACE_Neural_Graph")
        self.protocol = create_protocol()
        self.synapse_manager = SynapseManager()
        self.plasticity = StructuralPlasticity(self.graph, self.synapse_manager)
        self.execution_engine = ExecutionEngine(self.graph, self.synapse_manager, self.protocol)
        self.evolution_engine = EvolutionEngine(self.graph, self.synapse_manager, self.plasticity)
        self.environment_sensor = EnvironmentSensor()
        self.load_balancer = LoadBalancer()

        # Riferimenti ai componenti SPEACE esistenti
        self.sp = safe_proactive
        self.kernel = smfoi_kernel
        self.wm = world_model
        self.team = scientific_team
        self.monitor = status_monitor

        # Neuroni wrapper (popolati in initialize)
        self.neurons: Dict[str, BaseNeuron] = {}

        # 9 Comparti Cerebrali (popolati in initialize_compartments)
        self.compartments: Dict[str, Any] = {}
        self.knowledge_graph = KnowledgeGraph()
        self.orchestrator: CortexOrchestrator = None

        # Learning Core (popolato in initialize_full_cortex)
        self.learning_core = None

        # Structural Plasticity components
        self.graph_engine: Optional[GraphEngine] = None
        self.swarm_node: Optional[SwarmNode] = None
        self.swarm_orchestrator: Optional[SwarmOrchestrator] = None
        self.device_registry: Optional[DeviceRegistry] = None

        self._background_thread: Optional[threading.Thread] = None
        self._evolution_thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

    # -----------------------------------------------------------------------
    # Inizializzazione Comparti Cerebrali
    # -----------------------------------------------------------------------
    def initialize_compartments(self):
        """Carica tutti i 9 comparti cerebrali dal registry"""
        print("[NeuralBridge] Inizializzazione 9 comparti cerebrali...")
        for name, CompartmentClass in COMPARTI_REGISTRY.items():
            try:
                instance = CompartmentClass()  # Crea istanza senza bridge
                instance.set_bridge(self)  # Passa bridge separatamente
                self.compartments[name] = instance
                print(f"  [OK] Comparto caricato: {name}")
            except Exception as e:
                print(f"  [!!] Errore caricamento {name}: {e}")

        print(f"[NeuralBridge] Comparti attivati: {len(self.compartments)}/9")
        return self.compartments

    def initialize_full_cortex(self):
        """Inizializza tutti i 9 comparti + Orchestrator centrale"""
        print("[NeuralBridge] Inizializzazione completa del Cortex SPEACE...")

        # Carica i 9 comparti
        for name, CompartmentClass in COMPARTI_REGISTRY.items():
            try:
                instance = CompartmentClass()
                instance.set_bridge(self)
                self.compartments[name] = instance
                print(f"  [OK] {name.replace('_', ' ').title()}")
            except Exception as e:
                print(f"  [!!] Errore {name}: {e}")

        # Carica comparti lazy (richiedono bridge reference)
        for name, factory_fn in COMPARTI_LAZY.items():
            try:
                CompartmentClass = factory_fn()
                instance = CompartmentClass()
                instance.set_bridge(self)
                self.compartments[name] = instance
                print(f"  [OK] {name.replace('_', ' ').title()} (lazy)")
            except Exception as e:
                print(f"  [!!] Errore lazy {name}: {e}")

        # Crea l'orchestrator centrale
        self.orchestrator = CortexOrchestrator(self)

        # Inizializza Learning Core
        try:
            from .learning_core.online_learner import SPEACEOnlineLearner
            self.learning_core = SPEACEOnlineLearner()
            print(f"  [OK] Learning Core initialized")
        except ImportError as e:
            print(f"  [!!] Learning Core not available: {e}")
            self.learning_core = None

        # Inizializza GraphEngine (plasticità strutturale)
        try:
            self.graph_engine = GraphEngine(name="SPEACE_Structural_Graph")
            print(f"  [OK] Graph Engine initialized")
        except Exception as e:
            print(f"  [!!] Graph Engine not available: {e}")
            self.graph_engine = None

        # Inizializza Swarm Node
        try:
            self.swarm_node = SwarmNode(role="cortex", node_id=f"cortex_{self.cycle_count}")
            self.swarm_orchestrator = SwarmOrchestrator(local_node=self.swarm_node)
            print(f"  [OK] Swarm Node initialized")
        except Exception as e:
            print(f"  [!!] Swarm Node not available: {e}")
            self.swarm_node = None

        # Inizializza Device Registry
        try:
            self.device_registry = DeviceRegistry()
            print(f"  [OK] Device Registry loaded: {self.device_registry.get_active_count()} devices")
        except Exception as e:
            print(f"  [!!] Device Registry not available: {e}")
            self.device_registry = None

        print(f"[NeuralBridge] Cortex attivato: {len(self.compartments)} comparti + Orchestrator + Swarm + GraphEngine")
        return self.compartments

    async def run_full_cognitive_cycle(self, input_data: dict):
        """Ciclo cognitivo completo (end-to-end)"""
        if not self.orchestrator:
            self.initialize_full_cortex()

        return await self.orchestrator.run_cycle(input_data)

    async def process(self, context: dict):
        """Process method for compatibility - routes to full cognitive cycle"""
        return await self.run_full_cognitive_cycle(context)

    async def process_cortex(self, input_data: dict) -> Dict[str, Any]:
        """Orchestra l'elaborazione attraverso tutti i comparti"""
        results = {}

        # Prefrontal decide prima (planning)
        if "prefrontal" in self.compartments:
            comp = self.compartments["prefrontal"]
            result = comp.process(input_data) if hasattr(comp, "process") else {"status": "no_process"}
            results["prefrontal"] = result

        # Safety check sempre
        if "safety" in self.compartments:
            comp = self.compartments["safety"]
            result = comp.process({"operation": "assess_risk", "action": "cortex_process"})
            results["safety"] = result

        # Gli altri comparti elaborano
        for name, comp in self.compartments.items():
            if name not in ["prefrontal", "safety"]:
                try:
                    result = comp.process(input_data) if hasattr(comp, "process") else {"status": "no_process"}
                    results[name] = result
                except Exception as e:
                    results[name] = {"status": "error", "error": str(e)}

        return results

    def process_cortex_sync(self, input_data: dict) -> Dict[str, Any]:
        """Versione sincrona di process_cortex"""
        results = {}

        if "prefrontal" in self.compartments:
            comp = self.compartments["prefrontal"]
            result = comp.process(input_data) if hasattr(comp, "process") else {"status": "no_process"}
            results["prefrontal"] = result

        if "safety" in self.compartments:
            comp = self.compartments["safety"]
            result = comp.process({"operation": "assess_risk", "action": "cortex_process"})
            results["safety"] = result

        for name, comp in self.compartments.items():
            if name not in ["prefrontal", "safety"]:
                try:
                    result = comp.process(input_data) if hasattr(comp, "process") else {"status": "no_process"}
                    results[name] = result
                except Exception as e:
                    results[name] = {"status": "error", "error": str(e)}

        return results

    def get_cortex_status(self) -> Dict[str, Any]:
        """Stato di tutti i comparti cerebrali"""
        status = {
            "compartments_initialized": len(self.compartments),
            "knowledge_graph_stats": self.knowledge_graph.get_stats() if self.knowledge_graph else {},
            "graph_engine": self.get_graph_engine_status(),
            "swarm": self.get_swarm_status(),
            "device_registry": self.get_device_registry_status(),
        }
        for name, comp in self.compartments.items():
            if hasattr(comp, "get_status"):
                status[name] = comp.get_status()
        return status

    def get_graph_engine_status(self) -> Dict[str, Any]:
        """Stato del Graph Engine (plasticità strutturale)"""
        if self.graph_engine is None:
            return {"status": "not_initialized"}
        return self.graph_engine.get_graph_snapshot()

    def get_swarm_status(self) -> Dict[str, Any]:
        """Stato dello Swarm Node"""
        if self.swarm_node is None:
            return {"status": "not_initialized"}
        return self.swarm_node.get_swarm_status()

    def get_device_registry_status(self) -> Dict[str, Any]:
        """Stato del Device Registry"""
        if self.device_registry is None:
            return {"status": "not_initialized"}
        return {
            "total_devices": len(self.device_registry.devices),
            "active_count": self.device_registry.get_active_count(),
            "types": list(set(d.get("type") for d in self.device_registry.devices.values())),
        }

    def get_c_index(self) -> float:
        """Ritorna il C-index corrente del cortex"""
        if not self.compartments:
            return 0.0

        # Calcola C-index basato su comparti attivi
        success_count = 0
        for comp in self.compartments.values():
            if hasattr(comp, "get_status"):
                status = comp.get_status()
                if status.get("status") == "success" or status.get("activation_count", 0) > 0:
                    success_count += 1

        base_c_index = 0.65
        compartment_factor = success_count / max(len(self.compartments), 1) * 0.15
        return min(0.95, base_c_index + compartment_factor)

    # -----------------------------------------------------------------------
    # Inizializzazione
    # -----------------------------------------------------------------------
    def initialize(self):
        """Costruisce il grafo neurale con i neuroni wrapper e le connessioni."""
        print(f"[NeuralBridge] Inizializzazione grafo v{self.VERSION}...")

        self._create_neurons()
        self._create_synapses()
        self.evolution_engine.initialize()

        # Inizializza anche i 9 comparti cerebrali
        self.initialize_compartments()

        print(f"[NeuralBridge] Neurons: {len(self.graph._neurons)}")
        print(f"[NeuralBridge] Synapses: {len(self.synapse_manager._synapses)}")
        print(f"[NeuralBridge] Compartments: {len(self.compartments)}/9")
        print("[NeuralBridge] Ready")

    def _create_neurons(self):
        """Istanzia i neuroni wrapper e li registra nel grafo."""
        # SafeProactive
        n_sp = SafeProactiveNeuron(safe_proactive_instance=self.sp)
        self.graph.add_neuron(n_sp)
        self.neurons["safeproactive"] = n_sp

        # SMFOI-KERNEL
        n_smfoi = SMFOIKerneNeuron(kernel_instance=self.kernel)
        self.graph.add_neuron(n_smfoi)
        self.neurons["smfoi"] = n_smfoi

        # WorldModel
        n_wm = WorldModelNeuron(wm_instance=self.wm)
        self.graph.add_neuron(n_wm)
        self.neurons["worldmodel"] = n_wm

        # ScientificTeam
        n_team = ScientificTeamNeuron(orchestrator_instance=self.team)
        self.graph.add_neuron(n_team)
        self.neurons["scientificteam"] = n_team

        # DigitalDNA
        n_dna = DigitalDNANeuron()
        self.graph.add_neuron(n_dna)
        self.neurons["digitaldna"] = n_dna

        # Memory
        n_mem = MemoryNeuron()
        self.graph.add_neuron(n_mem)
        self.neurons["memory"] = n_mem

        # StatusMonitor
        n_mon = StatusMonitorNeuron(monitor_instance=self.monitor)
        self.graph.add_neuron(n_mon)
        self.neurons["statusmonitor"] = n_mon

        # AutoGPT Forge (MultiFramework) — con tool locali operativi
        def _tool_calculator(goal, ctx):
            expr = ctx.get("expression", "")
            try:
                return {"result": eval(expr, {"__builtins__": {}}, {})}
            except Exception as e:
                return {"error": str(e)}

        def _tool_file_ops(goal, ctx):
            path = ctx.get("path", "")
            operation = ctx.get("operation", "read")
            try:
                p = Path(path)
                if operation == "read" and p.exists():
                    return {"content": p.read_text(encoding="utf-8", errors="ignore")[:2000]}
                elif operation == "list" and p.exists():
                    return {"entries": [str(x) for x in p.iterdir()][:50]}
                return {"error": "Unsupported file operation or path not found"}
            except Exception as e:
                return {"error": str(e)}

        n_agpt = AGPTNeuron(local_tools={"calculator": _tool_calculator, "file_ops": _tool_file_ops})
        self.graph.add_neuron(n_agpt)
        self.neurons["agpt"] = n_agpt

        # Hermes Agent (Team Scientifico) — lazy init da env vars
        n_hermes = HermesAgentNeuron()
        self.graph.add_neuron(n_hermes)
        self.neurons["hermes"] = n_hermes

        # Neuroni evolutivi interni (opzionali)
        # n_env = self.evolution_engine._create_environment_neuron()
        # if n_env:
        #     self.graph.add_neuron(n_env)
        #     self.neurons["environment"] = n_env

    def _create_synapses(self):
        """Crea le connessioni sinaptiche tra i neuroni (topologia iniziale)."""
        conn = [
            # DigitalDNA -> tutti (fonte di verità)
            ("digitaldna", "safeproactive", EdgeType.DATA, 1.0),
            ("digitaldna", "smfoi", EdgeType.DATA, 1.0),
            ("digitaldna", "worldmodel", EdgeType.DATA, 0.9),
            ("digitaldna", "scientificteam", EdgeType.DATA, 0.8),
            ("digitaldna", "statusmonitor", EdgeType.DATA, 0.7),

            # SafeProactive -> SMFOI (gate decisionale)
            ("safeproactive", "smfoi", EdgeType.CONTROL, 1.0),

            # SMFOI -> WorldModel (lettura/scrittura memoria)
            ("smfoi", "worldmodel", EdgeType.BIDIRECTIONAL, 0.9),

            # WorldModel -> ScientificTeam (dati per analisi)
            ("worldmodel", "scientificteam", EdgeType.DATA, 0.7),

            # ScientificTeam -> SafeProactive (proposte)
            ("scientificteam", "safeproactive", EdgeType.FEEDBACK, 0.8),

            # StatusMonitor -> tutti (feedback loop)
            ("statusmonitor", "safeproactive", EdgeType.FEEDBACK, 0.5),
            ("statusmonitor", "smfoi", EdgeType.FEEDBACK, 0.5),
            ("statusmonitor", "worldmodel", EdgeType.FEEDBACK, 0.5),

            # Memory -> tutti (memoria persistente)
            ("memory", "smfoi", EdgeType.DATA, 0.6),
            ("memory", "worldmodel", EdgeType.DATA, 0.6),
            ("memory", "scientificteam", EdgeType.DATA, 0.5),

            # AutoGPT Forge -> SMFOI (task decomposition)
            ("agpt", "smfoi", EdgeType.DATA, 0.7),
            ("agpt", "worldmodel", EdgeType.DATA, 0.6),

            # Hermes Agent -> ScientificTeam (task scheduling e ricordi)
            ("hermes", "scientificteam", EdgeType.DATA, 0.8),
            ("hermes", "memory", EdgeType.BIDIRECTIONAL, 0.7),

            # DigitalDNA -> Framework esterni (config condivisa)
            ("digitaldna", "agpt", EdgeType.DATA, 0.5),
            ("digitaldna", "hermes", EdgeType.DATA, 0.5),
        ]

        for src, tgt, etype, weight in conn:
            sid = self._neuron_id(src)
            tid = self._neuron_id(tgt)
            if sid and tid:
                self.graph.connect(sid, tid, edge_type=etype, weight=weight)
                self.synapse_manager.create_synapse(sid, tid, edge_type=etype, initial_weight=weight)

    def _neuron_id(self, name: str) -> Optional[str]:
        n = self.neurons.get(name)
        return n.id if n else None

    # -----------------------------------------------------------------------
    # Esecuzione cicli
    # -----------------------------------------------------------------------
    def run_cycle(self, cycle_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Esegue un ciclo completo del grafo neurale."""
        self.cycle_count += 1
        ctx = cycle_context or {}

        # 1. Leggi stato da DigitalDNA
        dna_ctx = ExecutionContext(
            execution_id=f"cycle_{self.cycle_count}_dna",
            neuron_id=self.neurons["digitaldna"].id,
            inputs={"operation": "read", "file": "epigenome.yaml"}
        )
        dna_result = self.neurons["digitaldna"].execute(dna_ctx)

        # 2. Esegui SMFOI-KERNEL come neurone
        smfoi_ctx = ExecutionContext(
            execution_id=f"cycle_{self.cycle_count}_smfoi",
            neuron_id=self.neurons["smfoi"].id,
            inputs={
                "mode": ctx.get("mode", "single"),
                "cycle": self.cycle_count,
                "context": {
                    **ctx,
                    "dna_state": dna_result.get("result", {}),
                }
            }
        )
        smfoi_result = self.neurons["smfoi"].execute(smfoi_ctx)

        # 3. Propaga segnali attraverso le sinapsi
        self.synapse_manager.propagate_signal(
            self.neurons["smfoi"].id,
            SignalType.RESULT,
            smfoi_result
        )

        # 4. Aggiorna plasticità
        self._update_plasticity(smfoi_result)

        # 5. Esegui StatusMonitor
        mon_ctx = ExecutionContext(
            execution_id=f"cycle_{self.cycle_count}_mon",
            neuron_id=self.neurons["statusmonitor"].id,
            inputs={"action": "heartbeat"}
        )
        mon_result = self.neurons["statusmonitor"].execute(mon_ctx)

        return {
            "cycle": self.cycle_count,
            "dna_result": dna_result,
            "smfoi_result": smfoi_result,
            "monitor_result": mon_result,
            "synapse_stats": self.synapse_manager.get_synapse_stats(),
            "plasticity_report": self.plasticity.get_plasticity_report(),
        }

    def _update_plasticity(self, smfoi_result: Dict):
        """Aggiorna i pesi sinaptici in base all'esito del ciclo SMFOI."""
        success = smfoi_result.get("status") != "error"
        outcome = 1.0 if success else 0.0

        for synapse_id, synapse in self.synapse_manager._synapses.items():
            self.synapse_manager.update_from_outcome(
                synapse_id,
                execution_success=success,
                outcome_metric=outcome
            )

    # -----------------------------------------------------------------------
    # Background loop
    # -----------------------------------------------------------------------
    def start_background(self, interval: float = 60.0):
        """Avvia il loop continuo in background."""
        if self.running:
            return
        self.running = True
        self.start_time = time.time()
        self._background_thread = threading.Thread(target=self._loop, args=(interval,), daemon=True)
        self._background_thread.start()
        print(f"[NeuralBridge] Background loop avviato (interval={interval}s)")

    def stop_background(self):
        """Ferma il loop continuo."""
        self.running = False
        if self._background_thread:
            self._background_thread.join(timeout=5)
        print("[NeuralBridge] Background loop fermato")

    def _loop(self, interval: float):
        while self.running:
            try:
                result = self.run_cycle({"mode": "continuous"})
                print(f"[NeuralBridge] Ciclo #{result['cycle']} completato | "
                      f"Sinapsi: {result['synapse_stats']['total_synapses']} | "
                      f"Fitness avg: {result['plasticity_report']['average_fitness']:.3f}")
            except Exception as e:
                print(f"[NeuralBridge] ⚠️ Errore ciclo: {e}")
            time.sleep(interval)

    # -----------------------------------------------------------------------
    # Stato e reporting
    # -----------------------------------------------------------------------
    def get_state(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "running": self.running,
            "cycle_count": self.cycle_count,
            "uptime": time.time() - self.start_time,
            "neurons": {k: v.get_status() for k, v in self.neurons.items()},
            "compartments": {k: v.get_status() if hasattr(v, "get_status") else {} for k, v in self.compartments.items()},
            "cortex_compartments_initialized": len(self.compartments),
            "graph": self.graph.get_state(),
            "synapses": self.synapse_manager.get_synapse_stats(),
            "plasticity": self.plasticity.get_plasticity_report(),
        }

    def export_graph(self) -> Dict[str, Any]:
        return self.graph.export_to_dict()


# Re-export per compatibilità
__all__ = ["SPEACENeuralBridge"]
