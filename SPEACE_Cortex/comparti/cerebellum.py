"""
Cerebellum - Low-level Execution
Composto per esecuzione di basso livello e automazione.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import subprocess
import logging

logger = logging.getLogger("Cerebellum")


class Cerebellum:
    """
    Cerebellum - Low-level Execution e Automation.

    Responsabilita:
    - Esecuzione script e comandi di basso livello
    - Automazione task ripetitivi
    - Motor schema execution
    - Habit learning
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "cerebellum"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Script registry
        self.scripts: Dict[str, Callable] = {}
        self.script_history: List[Dict] = []
        self.max_history = self.config.get("max_history", 100)

        # Habit memory (azioni automatiche)
        self.habits: Dict[str, Dict] = {}
        self.habit_threshold = self.config.get("habit_threshold", 5)

        # Execution settings
        self.sandbox_mode = self.config.get("sandbox", True)
        self.allowed_commands = ["python", "pip", "git"]
        self.denied_commands = ["rm -rf", "format", "del /f"]

        self.last_execution = datetime.now()
        self.execution_count = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Cerebellum.

        Args:
            context: Contesto con operation, command, script

        Returns:
            Dict con execution_results
        """
        self.last_execution = datetime.now()

        try:
            operation = context.get("operation", "execute")

            if operation == "execute":
                result = self._execute_command(context)
            elif operation == "run_script":
                result = self._run_script(context)
            elif operation == "learn_habit":
                result = self._learn_habit(context)
            elif operation == "check_habit":
                result = self._check_habit(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Cerebellum error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _execute_command(self, context: Dict) -> Dict[str, Any]:
        """Esegue un comando shell"""
        command = context.get("command", "")

        # Security check
        if self._is_command_safe(command):
            try:
                if self.sandbox_mode:
                    result = {"simulated": True, "command": command}
                    success = True
                else:
                    proc = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    result = {
                        "stdout": proc.stdout,
                        "stderr": proc.stderr,
                        "returncode": proc.returncode,
                    }
                    success = proc.returncode == 0

            except subprocess.TimeoutExpired:
                result = {"error": "Command timeout (30s)"}
                success = False
            except Exception as e:
                result = {"error": str(e)}
                success = False
        else:
            result = {"error": "Command not allowed", "command": command}
            success = False

        self._log_execution(command, success, result)
        return {
            "command": command,
            "success": success,
            "result": result,
        }

    def _is_command_safe(self, command: str) -> bool:
        """Verifica se il comando e sicuro"""
        for denied in self.denied_commands:
            if denied in command:
                return False
        return True

    def _run_script(self, context: Dict) -> Dict[str, Any]:
        """Esegue uno script registrato"""
        script_name = context.get("script_name", "")
        script_args = context.get("script_args", {})

        if script_name in self.scripts:
            try:
                result = self.scripts[script_name](**script_args)
                success = True
            except Exception as e:
                result = {"error": str(e)}
                success = False
        else:
            result = {"error": "Script not found", "script": script_name}
            success = False

        self._log_execution(f"script:{script_name}", success, result)
        return {
            "script": script_name,
            "success": success,
            "result": result,
        }

    def register_script(self, name: str, func: Callable):
        """Registra uno script"""
        self.scripts[name] = func
        logger.info(f"Registered script: {name}")

    def _learn_habit(self, context: Dict) -> Dict[str, Any]:
        """Impara un nuovo habit"""
        action = context.get("action", "")
        trigger = context.get("trigger", "")
        reward = context.get("reward", 0.0)

        if action not in self.habits:
            self.habits[action] = {"trigger": trigger, "count": 0, "total_reward": 0.0}

        self.habits[action]["count"] += 1
        self.habits[action]["total_reward"] += reward
        self.habits[action]["avg_reward"] = (
            self.habits[action]["total_reward"] / self.habits[action]["count"]
        )

        learned = self.habits[action]["count"] >= self.habit_threshold

        return {
            "action": action,
            "trigger": trigger,
            "count": self.habits[action]["count"],
            "habit_learned": learned,
            "avg_reward": self.habits[action]["avg_reward"],
        }

    def _check_habit(self, context: Dict) -> Dict[str, Any]:
        """Verifica se un action e un habit"""
        action = context.get("action", "")

        if action in self.habits:
            habit = self.habits[action]
            return {
                "action": action,
                "is_habit": habit["count"] >= self.habit_threshold,
                "count": habit["count"],
                "trigger": habit.get("trigger", ""),
            }

        return {"action": action, "is_habit": False, "count": 0}

    def _log_execution(self, command: str, success: bool, result: Any):
        """Log dell'esecuzione"""
        self.execution_count += 1
        self.script_history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
            "result_type": type(result).__name__,
        })

        if len(self.script_history) > self.max_history:
            self.script_history = self.script_history[-self.max_history:]

    def get_available_scripts(self) -> List[str]:
        """API per ottenere script disponibili"""
        return list(self.scripts.keys())

    def get_habits(self) -> Dict[str, Dict]:
        """API per ottenere habits"""
        return dict(self.habits)

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "scripts_registered": len(self.scripts),
            "habits_learned": len(self.habits),
            "execution_count": self.execution_count,
            "sandbox_mode": self.sandbox_mode,
            "last_execution": self.last_execution.isoformat(),
        }
