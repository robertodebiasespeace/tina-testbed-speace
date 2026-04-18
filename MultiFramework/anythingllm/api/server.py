"""
AnythingLLM API Server
REST API per World Model

Versione: 1.0
Data: 2026-04-17
"""

import sys
import os
import json
import logging
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnythingLLM-API")


def create_app(query_interface=None, ingester=None) -> Flask:
    """
    Factory: crea Flask app con endpoint AnythingLLM.
    """
    app = Flask(__name__)
    qi = query_interface
    ing = ingester

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "anythingllm-world-model",
            "version": "1.0",
            "timestamp": datetime.now().isoformat()
        })

    @app.route("/workspaces", methods=["GET"])
    def list_workspaces():
        """Lista workspace disponibili"""
        workspaces = [
            {"id": "speace_docs", "name": "SPEACE Documentation", "status": "active"},
            {"id": "digitaldna", "name": "DigitalDNA", "status": "active"},
            {"id": "team_scientifico", "name": "Team Scientifico", "status": "active"},
        ]
        return jsonify({"workspaces": workspaces})

    @app.route("/query", methods=["POST"])
    def query():
        """
        Query World Model.
        Request body:
        {
            "query": "question string",
            "workspace_id": "speace_docs",  // optional
            "max_sources": 5,                // optional
            "similarity_threshold": 0.7      // optional
        }
        """
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "query field required"}), 400

        # Create query request
        from .query_interface import QueryRequest
        query_req = QueryRequest(
            query=data["query"],
            workspace_id=data.get("workspace_id", "speace_docs"),
            max_sources=data.get("max_sources", 5),
            similarity_threshold=data.get("similarity_threshold", 0.7)
        )

        # Process query
        if qi:
            response = qi.query(query_req)
            return jsonify({
                "answer": response.answer,
                "sources": [
                    {
                        "doc_id": s.doc_id,
                        "title": s.title,
                        "source_path": s.source_path,
                        "chunk_content": s.chunk_content[:200] + "...",
                        "similarity_score": s.similarity_score
                    }
                    for s in response.sources
                ],
                "model": response.model,
                "timestamp": response.timestamp,
                "query_time_ms": response.query_time_ms,
                "confidence": response.confidence,
                "workspace_id": response.workspace_id
            })
        else:
            return jsonify({"error": "Query interface not initialized"}), 500

    @app.route("/ingest", methods=["POST"])
    def ingest():
        """
        Ingest documento.
        Request body:
        {
            "file_path": "path/to/document.md"
        }
        """
        data = request.get_json()

        if not data or "file_path" not in data:
            return jsonify({"error": "file_path required"}), 400

        if ing:
            result = ing.ingest_file(data["file_path"])
            if result:
                return jsonify({
                    "status": "success",
                    "doc_id": result.doc_id,
                    "title": result.title,
                    "chunks_count": result.chunks_count
                })
            else:
                return jsonify({"error": "Failed to ingest file"}), 500
        else:
            return jsonify({"error": "Ingester not initialized"}), 500

    @app.route("/stats", methods=["GET"])
    def stats():
        """Statistiche sistema"""
        stats_data = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "service": "anythingllm-world-model"
        }

        if qi:
            stats_data["query_stats"] = qi.get_stats()

        if ing:
            stats_data["ingestion_stats"] = ing.get_ingestion_stats()

        return jsonify(stats_data)

    @app.route("/sync/status", methods=["GET"])
    def sync_status():
        """Status sincronizzazione"""
        return jsonify({
            "status": "active",
            "timestamp": datetime.now().isoformat()
        })

    logger.info("AnythingLLM API routes registered")
    return app


def run_server(host: str = "0.0.0.0", port: int = 8003):
    """
    Avvia server AnythingLLM.
    """
    from ..anythingllm_config import AnythingLLMConfig
    from ..document_ingester import DocumentIngester
    from ..query_interface import WorldModelQueryInterface

    logger.info("Initializing AnythingLLM components...")

    # Initialize components
    config = AnythingLLMConfig.create_speace_default()
    ingester = DocumentIngester("./vector_data")
    qi = WorldModelQueryInterface(ingester)

    # Create app with initialized components
    app = create_app(qi, ingester)

    logger.info(f"Starting AnythingLLM server on {host}:{port}")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    import os
    # Change to workspace root if run directly
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

    run_server()
