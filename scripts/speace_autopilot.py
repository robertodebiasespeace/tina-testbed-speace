"""
SPEACE Cortex Autopilot - Loop Cognitivo Autonomo Continuo
Esegue cicli completi del cervello SPEACE ogni X secondi
Versione: 1.1 - Fixed encoding + robust logging
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

# ====================== IMPORTS SPEACE ======================
sys.path.insert(0, str(Path(__file__).parent.parent))

from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge


class SPEACEAutopilot:
    def __init__(self, cycle_interval: int = 45):
        self.bridge = SPEACENeuralBridge()
        self.cycle_interval = cycle_interval
        self.cycle_count = 0
        self.running = False
        logger.info("🚀 SPEACE Cortex Autopilot inizializzato")

    async def start(self):
        """Avvia il loop autonomo continuo"""
        self.running = True
        
        # Inizializzazione completa del cervello
        logger.info("🧠 Inizializzazione completa del Cortex SPEACE...")
        self.bridge.initialize_full_cortex()

        logger.info(f"✅ Autopilot avviato - Ciclo cognitivo ogni {self.cycle_interval} secondi")
        logger.info("Premi Ctrl+C per fermare")

        while self.running:
            try:
                self.cycle_count += 1
                start_time = time.time()

                # Input contestuale per il ciclo
                input_data = {
                    "query": f"Ciclo cognitivo autonomo #{self.cycle_count} - "
                             f"Analisi stato SPEACE, Rigene Project e obiettivi evolutivi",
                    "push_intensity": 0.65 + (self.cycle_count % 10) * 0.035,
                    "environment": "reale",
                    "timestamp": datetime.now().isoformat(),
                    "mode": "autopilot",
                    "cycle_number": self.cycle_count
                }

                # Esecuzione ciclo cognitivo completo
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

                # Learning Core (se disponibile)
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
                        logger.warning(f"Learning core error: {e}")

                await asyncio.sleep(self.cycle_interval)

            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                logger.error(f"Errore durante ciclo #{self.cycle_count}: {e}")
                await asyncio.sleep(10)

    def stop(self):
        self.running = False
        logger.info("⛔ SPEACE Autopilot fermato dall'utente")


async def main():
    autopilot = SPEACEAutopilot(cycle_interval=45)
    
    try:
        await autopilot.start()
    except KeyboardInterrupt:
        autopilot.stop()
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        autopilot.stop()


if __name__ == "__main__":
    print("=" * 60)
    print("SPEACE CORTEX AUTOPILOT - Loop Cognitivo Autonomo")
    print("=" * 60)
    asyncio.run(main())
