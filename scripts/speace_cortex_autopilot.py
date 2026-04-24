"""
SPEACE Cortex Autopilot - Loop Cognitivo Autonomo Continuo
Versione: 1.2 - Fixed asyncio + robust error handling
"""

import asyncio
import time
import logging
import sys
from datetime import datetime
from pathlib import Path

# ====================== FIX ENCODING WINDOWS ======================
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# ====================== LOGGING ======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("speace_autopilot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)
logger = logging.getLogger(__name__)

# ====================== IMPORTS ======================
sys.path.insert(0, str(Path(__file__).parent.parent))

from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge


class SPEACEAutopilot:
    def __init__(self, cycle_interval: int = 30):
        self.bridge = SPEACENeuralBridge()
        self.cycle_interval = cycle_interval
        self.cycle_count = 0
        self.running = False
        logger.info("SPEACE Cortex Autopilot inizializzato")

    async def start(self):
        """Loop principale autonomo"""
        self.running = True
        logger.info(f"Autopilot avviato - Ciclo ogni {self.cycle_interval} secondi")
        logger.info("Premi Ctrl+C per fermare\n")

        # Inizializzazione completa del cervello
        self.bridge.initialize_full_cortex()

        while self.running:
            try:
                self.cycle_count += 1
                start_time = time.time()

                input_data = {
                    "query": f"Ciclo cognitivo autonomo #{self.cycle_count} - Analisi SPEACE & Rigene Project",
                    "push_intensity": 0.65 + (self.cycle_count % 10) * 0.035,
                    "environment": "reale",
                    "timestamp": datetime.now().isoformat(),
                    "mode": "autopilot",
                    "cycle_number": self.cycle_count
                }

                result = await self.bridge.run_full_cognitive_cycle(input_data)

                duration = time.time() - start_time
                c_index = result.get("c_index", 0.0)
                fitness_delta = result.get("fitness_delta", 0.0)

                logger.info(
                    f"Cycle #{self.cycle_count:3d} | "
                    f"C-index: {c_index:.3f} | "
                    f"Fitness Δ: {fitness_delta:+.3f} | "
                    f"Duration: {duration:.2f}s | "
                    f"Comparti: {len(result.get('compartments', {}))}/9"
                )

                # Learning Core
                if hasattr(self.bridge, 'learning_core') and self.bridge.learning_core:
                    try:
                        features = {
                            "c_index": c_index,
                            "compartments_active": len(result.get("compartments", {})),
                            "push_intensity": input_data["push_intensity"],
                            "cycle_duration": duration
                        }
                        self.bridge.learning_core.learn(features, fitness_delta)
                    except Exception as e:
                        logger.debug(f"Learning core skip: {e}")

                # Salva stato per Dashboard live
                self._save_live_state({
                    "c_index": c_index,
                    "fitness_delta": fitness_delta,
                    "duration": duration,
                    "compartments": result.get("compartments", {})
                })

                await asyncio.sleep(self.cycle_interval)

            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                logger.error(f"Errore ciclo #{self.cycle_count}: {e}")
                await asyncio.sleep(5)

    def stop(self):
        self.running = False
        uptime = datetime.now() - self.start_time if self.start_time else 0
        logger.info(f"Autopilot fermato - Cicli eseguiti: {self.cycle_count}, Uptime: {uptime}")

    def _save_live_state(self, result: dict):
        """Salva stato ciclo per Dashboard live"""
        import json
        state_file = Path("data/speace_live_state.json")
        state_file.parent.mkdir(exist_ok=True)

        live_state = {
            "last_cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "c_index": result.get("c_index", 0.0),
            "fitness_delta": result.get("fitness_delta", 0.0),
            "duration": result.get("duration", 0.0),
            "compartments_active": len(result.get("compartments", {})),
            "status": "success"
        }

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(live_state, f, indent=2, default=str)

    async def test_agpt(self):
        """Comando manuale per testare AGPT"""
        logger.info("🧪 Test AGPTNeuron avviato")
        agpt_comp = self.bridge.compartments.get("agpt")
        if agpt_comp:
            result = await agpt_comp.process({"task": "Ricerca informazioni su Rigene Project"})
            logger.info(f"AGPT Result: {result}")
            return result
        return {"status": "agpt_not_available"}

    async def test_hermes(self):
        """Comando manuale per testare Hermes"""
        logger.info("🧪 Test HermesAgentNeuron avviato")
        hermes_comp = self.bridge.compartments.get("hermes")
        if hermes_comp:
            result = await hermes_comp.process({"query": "Ricorda stato precedente del ciclo", "mode": "recall"})
            logger.info(f"Hermes Result: {result}")
            return result
        return {"status": "hermes_not_available"}

    async def run_manual_test(self, agent: str = "agpt"):
        """Esegue test manuale di un agente specifico"""
        if agent == "agpt":
            return await self.test_agpt()
        elif agent == "hermes":
            return await self.test_hermes()
        return {"error": f"Unknown agent: {agent}"}


async def main():
    autopilot = SPEACEAutopilot(cycle_interval=30)
    try:
        await autopilot.start()
    except KeyboardInterrupt:
        autopilot.stop()
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        autopilot.stop()


if __name__ == "__main__":
    print("=============================================================")
    print("SPEACE CORTEX AUTOPILOT - Loop Cognitivo Autonomo")
    print("=============================================================")
    asyncio.run(main())
