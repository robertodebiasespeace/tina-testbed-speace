"""
Hermes Agent Neuron – Neurone wrapper per Hermes Agent di Nous Research.
Agente autonomo locale con ricordi persistenti, task schedulati e browser automation.
Quando configurato con HERMES_BASE_URL, usa run_agent.AIAgent in modalita operativa.
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, List

# Neural Engine imports (relativi al package)
from ...neural_engine.neuron_base import (
    BaseNeuron, NeuronType, NeuronState, ExecutionContext, Contract, Port, NeuronFactory
)


ROOT_DIR = Path(__file__).parent.parent.parent.parent


class HermesAgentNeuron(BaseNeuron):
    """
    Neurone che wrappa Hermes Agent per task avanzati nel Team Scientifico.
    Gestisce ricordi persistenti, task schedulati, browser automation e agenti secondari.
    """

    def __init__(self, hermes_instance=None, **kwargs):
        self.hermes = hermes_instance
        self._memory_path = kwargs.pop("memory_path", ROOT_DIR / ".speace" / "hermes_memory")
        self._scheduled_tasks: List[Dict] = kwargs.pop("scheduled_tasks", [])
        self._hermes_config = kwargs.pop("hermes_config", {})
        self._ai_agent_cls = None
        self._try_import_hermes()
        super().__init__(
            neuron_id="neuron_hermes",
            name="HermesAgent",
            neuron_type=NeuronType.CORTEX_MODULE,
            **kwargs
        )

    def _try_import_hermes(self):
        vendor = ROOT_DIR / "vendor" / "hermes-agent"
        if str(vendor) not in sys.path:
            sys.path.insert(0, str(vendor))
        try:
            from run_agent import AIAgent
            self._ai_agent_cls = AIAgent
        except Exception:
            self._ai_agent_cls = None

    def _get_hermes_agent(self):
        if self.hermes is not None:
            return self.hermes
        if self._ai_agent_cls is None:
            return None
        cfg = self._hermes_config or {}
        base_url = cfg.get("base_url") or os.environ.get("HERMES_BASE_URL")
        api_key = cfg.get("api_key") or os.environ.get("HERMES_API_KEY")
        model = cfg.get("model") or os.environ.get("HERMES_MODEL", "")
        if not base_url:
            return None
        try:
            self.hermes = self._ai_agent_cls(
                base_url=base_url,
                api_key=api_key,
                model=model,
                max_iterations=cfg.get("max_iterations", 90),
                verbose_logging=cfg.get("verbose_logging", False),
                quiet_mode=cfg.get("quiet_mode", True),
            )
            return self.hermes
        except Exception:
            return None

    def _default_contract(self) -> Contract:
        return Contract(
            input_ports=[
                Port(name="task", data_type="string", direction="in", required=True),
                Port(name="context", data_type="dict", direction="in"),
                Port(name="mode", data_type="string", direction="in"),
            ],
            output_ports=[
                Port(name="result", data_type="dict", direction="out"),
                Port(name="memory_update", data_type="dict", direction="out"),
                Port(name="status", data_type="string", direction="out"),
            ],
            execution_timeout=90.0
        )

    def _execute(self, context: ExecutionContext) -> Dict[str, Any]:
        task = context.inputs.get("task", "")
        ctx = context.inputs.get("context", {})
        mode = context.inputs.get("mode", "execute")

        hermes = self._get_hermes_agent()

        if hermes is None:
            self._memory_path.mkdir(parents=True, exist_ok=True)
            if mode == "execute":
                return {
                    "result": {
                        "task": task,
                        "simulated": True,
                        "output": f"[STUB] Hermes processed task: {task}",
                        "tools_used": ["browser", "recall"],
                        "agent_secondary": None
                    },
                    "memory_update": {
                        "stored_in": str(self._memory_path),
                        "task_hash": f"h_{hash(task) & 0xFFFFFF:06x}",
                        "timestamp": time.time()
                    },
                    "status": "simulated"
                }

            elif mode == "schedule":
                scheduled = {
                    "task_id": f"sched_{int(time.time())}",
                    "task": task,
                    "delay_seconds": ctx.get("delay", 300),
                    "scheduled_at": time.time()
                }
                self._scheduled_tasks.append(scheduled)
                return {
                    "result": {"scheduled": scheduled, "total_pending": len(self._scheduled_tasks)},
                    "memory_update": {},
                    "status": "scheduled"
                }

            elif mode == "recall":
                return {
                    "result": {
                        "query": task,
                        "recalled": [f"Memory stub for: {task}"],
                        "confidence": 0.7
                    },
                    "memory_update": {},
                    "status": "recalled"
                }

            return {
                "result": {"error": f"Unknown mode: {mode}"},
                "memory_update": {},
                "status": "error"
            }

        try:
            if mode == "execute":
                conversation = hermes.run_conversation(
                    user_message=task,
                    system_message=ctx.get("system_message"),
                    conversation_history=ctx.get("conversation_history"),
                )
                result = {"conversation": conversation, "task": task}
            elif mode == "schedule":
                scheduled = {
                    "task_id": f"sched_{int(time.time())}",
                    "task": task,
                    "delay_seconds": ctx.get("delay", 300),
                    "scheduled_at": time.time()
                }
                self._scheduled_tasks.append(scheduled)
                result = {"scheduled": scheduled, "total_pending": len(self._scheduled_tasks)}
            elif mode == "recall":
                summary = hermes.get_activity_summary() if hasattr(hermes, "get_activity_summary") else {}
                result = {"query": task, "activity_summary": summary}
            else:
                result = {"error": f"Unknown mode: {mode}"}
            return {
                "result": result,
                "memory_update": {"last_task": task, "timestamp": time.time()},
                "status": "completed"
            }
        except Exception as e:
            return {
                "result": {"error": str(e), "traceback": traceback.format_exc()},
                "memory_update": {},
                "status": "error"
            }


NeuronFactory.register("hermes", HermesAgentNeuron)
