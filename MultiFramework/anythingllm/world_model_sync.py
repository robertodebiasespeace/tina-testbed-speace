"""
World Model Sync
Sincronizzazione cross-framework per World Model

Versione: 1.0
Data: 2026-04-17
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorldModel-Sync")


@dataclass
class SyncEvent:
    """Evento di sincronizzazione"""
    event_id: str
    timestamp: str
    source_framework: str
    sync_type: str  # "digitaldna_update", "team_output", "cortex_state"
    data: Dict[str, Any]
    status: str = "pending"


class WorldModelSync:
    """
    Gestisce sincronizzazione del World Model con altri componenti SPEACE.
    Sincronizza con: DigitalDNA, Team Scientifico, SPEACE Cortex, MultiFramework.
    """

    def __init__(self, query_interface=None):
        self.query_interface = query_interface
        self.sync_history: List[SyncEvent] = []
        self.last_sync: Optional[str] = None
        self.version = "1.0"
        logger.info("WorldModelSync initialized (v1.0)")

    def sync_digitaldna(self, genome_data: Dict, epigenome_data: Dict) -> bool:
        """
        Sincronizza DigitalDNA updates nel World Model.
        Called quando DigitalDNA viene modificato.
        """
        event = SyncEvent(
            event_id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            source_framework="digitaldna",
            sync_type="digitaldna_update",
            data={
                "genome": genome_data,
                "epigenome": epigenome_data
            }
        )

        try:
            # In real impl: update vector store with new DNA info
            logger.info(f"DigitalDNA synced: alignment={epigenome_data.get('stato_corrente', {}).get('alignment_score', 'N/A')}")
            self.sync_history.append(event)
            self.last_sync = event.timestamp
            return True
        except Exception as e:
            logger.error(f"DigitalDNA sync failed: {e}")
            return False

    def sync_team_output(self, agent_name: str, report_data: Dict) -> bool:
        """
        Sincronizza output del Team Scientifico nel World Model.
        Called quando un agente genera un report.
        """
        event = SyncEvent(
            event_id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            source_framework="team_scientifico",
            sync_type="team_output",
            data={
                "agent": agent_name,
                "report": report_data
            }
        )

        try:
            logger.info(f"Team output synced: {agent_name}")
            self.sync_history.append(event)
            self.last_sync = event.timestamp
            return True
        except Exception as e:
            logger.error(f"Team output sync failed: {e}")
            return False

    def sync_cortex_state(self, cortex_state: Dict) -> bool:
        """
        Sincronizza stato Cortex nel World Model.
        Called periodicamente o su cambiamento stato.
        """
        event = SyncEvent(
            event_id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            source_framework="cortex",
            sync_type="cortex_state",
            data=cortex_state
        )

        try:
            logger.info(f"Cortex state synced")
            self.sync_history.append(event)
            self.last_sync = event.timestamp
            return True
        except Exception as e:
            logger.error(f"Cortex state sync failed: {e}")
            return False

    def sync_multi_framework(self, framework_name: str, status_data: Dict) -> bool:
        """
        Sincronizza status da altro framework (IronClaw, SuperAGI, NanoClaw).
        """
        event = SyncEvent(
            event_id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            source_framework=framework_name,
            sync_type="framework_status",
            data=status_data
        )

        try:
            logger.info(f"Framework sync: {framework_name}")
            self.sync_history.append(event)
            self.last_sync = event.timestamp
            return True
        except Exception as e:
            logger.error(f"Framework sync failed: {e}")
            return False

    def get_sync_status(self) -> Dict[str, Any]:
        """Status della sincronizzazione"""
        return {
            "version": self.version,
            "last_sync": self.last_sync,
            "sync_events_count": len(self.sync_history),
            "recent_syncs": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp,
                    "source": e.source_framework,
                    "type": e.sync_type
                }
                for e in self.sync_history[-5:]
            ]
        }

    def get_knowledge_update(self, topic: str) -> List[Dict[str, Any]]:
        """
        Recupera updates recenti su un topic.
        Useful per queries tipo "latest on climate".
        """
        relevant = [
            {
                "event_id": e.event_id,
                "timestamp": e.timestamp,
                "source": e.source_framework,
                "type": e.sync_type,
                "summary": str(e.data)[:200]
            }
            for e in self.sync_history
            if topic.lower() in str(e.data).lower()
        ]
        return relevant


if __name__ == "__main__":
    # Test
    sync = WorldModelSync()

    # Simulate DigitalDNA sync
    sync.sync_digitaldna(
        genome_data={"obiettivi_primari": ["test"]},
        epigenome_data={"stato_corrente": {"alignment_score": 67.3}}
    )

    # Simulate team output
    sync.sync_team_output(
        agent_name="Climate Agent",
        report_data={"summary": "Temperature anomaly detected"}
    )

    status = sync.get_sync_status()
    print(f"Sync status: {status['sync_events_count']} events")
    print(f"Last sync: {status['last_sync']}")
