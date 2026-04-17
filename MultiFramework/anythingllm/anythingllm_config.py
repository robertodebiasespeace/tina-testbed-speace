"""
AnythingLLM Configuration
Configurazione workspace e vector database per SPEACE World Model

Versione: 1.0
Data: 2026-04-17
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnythingLLM-Config")


@dataclass
class EmbedderConfig:
    """Configurazione embedder"""
    provider: str = "native"  # native, openai, anthropic
    model: str = "nomic-embed-text"
    api_key: Optional[str] = None
    embedding_dimension: int = 768


@dataclass
class VectorDBConfig:
    """Configurazione vector database"""
    type: str = "lancedb"  # lancedb (embedded), chromadb, pinecone
    persistence_path: str = "./vector_data"
    distance_metric: str = "cosine"


@dataclass
class WorkspaceConfig:
    """Configurazione workspace singolo"""
    workspace_id: str
    workspace_name: str
    description: str
    document_paths: List[str] = field(default_factory=list)
    embedding_config: EmbedderConfig = field(default_factory=EmbedderConfig)
    vector_db_config: VectorDBConfig = field(default_factory=VectorDBConfig)
    max_tokens: int = 4096
    similarity_threshold: float = 0.7


@dataclass
class AnythingLLMConfig:
    """
    Configurazione principale AnythingLLM per SPEACE World Model.
    Mantiene settings per tutti i workspace e il sistema.
    """

    version: str = "1.0"
    created: str = field(default_factory=lambda: datetime.now().isoformat())

    # System-wide settings
    port: int = 8003
    host: str = "localhost"

    # Embedder settings
    default_embedder: EmbedderConfig = field(default_factory=EmbedderConfig)

    # Vector DB settings
    default_vector_db: VectorDBConfig = field(default_factory=VectorDBConfig)

    # Workspaces
    workspaces: List[WorkspaceConfig] = field(default_factory=list)

    # System prompts
    system_prompt: str = """
You are SPEACE World Model, an advanced knowledge graph system.
Your purpose is to maintain accurate, up-to-date information about:
- SPEACE architecture and components
- DigitalDNA state and mutations
- Team Scientifico outputs
- Planetary health metrics
- Multi-framework system status

Provide accurate, concise answers based on ingested documents.
When uncertain, state clearly that information is not in your knowledge base.
"""

    # Query settings
    query_settings: Dict[str, Any] = field(default_factory=lambda: {
        "max_sources": 5,
        "temperature": 0.3,
        "rerank": True,
        "hybrid_search": True
    })

    @classmethod
    def create_speace_default(cls) -> "AnythingLLMConfig":
        """Factory: crea configurazione di default per SPEACE"""
        config = cls()

        # SPEACE Documents workspace
        speace_docs = WorkspaceConfig(
            workspace_id="speace_docs",
            workspace_name="SPEACE Documentation",
            description="Engineering documents, SPECS, and technical specifications",
            document_paths=[
                "SPEACE-Engineering-Document-v1.1.md",
                "SPECS/",
                "SPEACE_Cortex/",
            ]
        )

        # DigitalDNA workspace
        digitaldna_workspace = WorkspaceConfig(
            workspace_id="digitaldna",
            workspace_name="DigitalDNA",
            description="DigitalDNA genome, epigenome, and mutation rules",
            document_paths=[
                "DigitalDNA/genome.yaml",
                "DigitalDNA/epigenome.yaml",
                "DigitalDNA/mutation_rules.yaml",
            ]
        )

        # Team Scientifico workspace
        team_workspace = WorkspaceConfig(
            workspace_id="team_scientifico",
            workspace_name="Team Scientifico",
            description="Team outputs, reports, and analysis",
            document_paths=[
                "Team_Scientifico/output/",
            ]
        )

        config.workspaces = [speace_docs, digitaldna_workspace, team_workspace]
        return config

    def add_workspace(self, workspace: WorkspaceConfig):
        """Aggiunge workspace alla configurazione"""
        existing = [w.workspace_id for w in self.workspaces]
        if workspace.workspace_id in existing:
            logger.warning(f"Workspace {workspace.workspace_id} already exists, skipping")
            return False
        self.workspaces.append(workspace)
        logger.info(f"Workspace added: {workspace.workspace_name}")
        return True

    def get_workspace(self, workspace_id: str) -> Optional[WorkspaceConfig]:
        """Ottiene workspace per ID"""
        for ws in self.workspaces:
            if ws.workspace_id == workspace_id:
                return ws
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Serializza in dict"""
        return {
            "version": self.version,
            "created": self.created,
            "port": self.port,
            "host": self.host,
            "default_embedder": {
                "provider": self.default_embedder.provider,
                "model": self.default_embedder.model,
                "embedding_dimension": self.default_embedder.embedding_dimension
            },
            "default_vector_db": {
                "type": self.default_vector_db.type,
                "persistence_path": self.default_vector_db.persistence_path,
                "distance_metric": self.default_vector_db.distance_metric
            },
            "workspaces": [
                {
                    "workspace_id": ws.workspace_id,
                    "workspace_name": ws.workspace_name,
                    "description": ws.description,
                    "document_paths": ws.document_paths,
                    "max_tokens": ws.max_tokens,
                    "similarity_threshold": ws.similarity_threshold
                }
                for ws in self.workspaces
            ],
            "system_prompt": self.system_prompt,
            "query_settings": self.query_settings
        }

    def save(self, path: str):
        """Salva configurazione su file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Config saved to {path}")

    @classmethod
    def load(cls, path: str) -> "AnythingLLMConfig":
        """Carica configurazione da file"""
        with open(path, 'r') as f:
            data = json.load(f)
        config = cls()
        config.port = data.get("port", 8003)
        config.host = data.get("host", "localhost")
        # Load workspaces etc.
        logger.info(f"Config loaded from {path}")
        return config


class WorkspaceManager:
    """Gestisce lifecycle dei workspace"""

    def __init__(self, config: AnythingLLMConfig):
        self.config = config
        self.active_workspaces: Dict[str, Dict[str, Any]] = {}
        logger.info("WorkspaceManager initialized")

    def initialize_workspace(self, workspace_id: str) -> bool:
        """
        Inizializza workspace.
        In implementation reale: crea LanceDB, carica documenti.
        """
        ws = self.config.get_workspace(workspace_id)
        if not ws:
            logger.error(f"Workspace not found: {workspace_id}")
            return False

        self.active_workspaces[workspace_id] = {
            "config": ws,
            "status": "initialized",
            "documents_loaded": 0,
            "last_sync": datetime.now().isoformat()
        }
        logger.info(f"Workspace initialized: {workspace_id}")
        return True

    def get_workspace_status(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        """Status workspace"""
        return self.active_workspaces.get(workspace_id)

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """Lista tutti i workspace"""
        return [
            {
                "workspace_id": ws.workspace_id,
                "workspace_name": ws.workspace_name,
                "description": ws.description,
                "status": self.active_workspaces.get(ws.workspace_id, {}).get("status", "not_initialized")
            }
            for ws in self.config.workspaces
        ]


if __name__ == "__main__":
    # Test configuration
    config = AnythingLLMConfig.create_speace_default()
    print(f"Created config with {len(config.workspaces)} workspaces:")
    for ws in config.workspaces:
        print(f"  - {ws.workspace_name} ({ws.workspace_id})")
