"""
Document Ingester
Pipeline per ingestione documenti SPEACE in vector store

Versione: 1.0
Data: 2026-04-17
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Document-Ingester")


@dataclass
class DocumentMetadata:
    """Metadata documento ingestito"""
    doc_id: str
    source_path: str
    title: str
    doc_type: str
    ingested_at: str
    size_bytes: int
    chunks_count: int = 0


class DocumentIngester:
    """
    Pipeline per ingestione documenti in AnythingLLM.
    Supporta: markdown, YAML, TXT, PDF (future).
    """

    def __init__(self, vector_store_path: str = "./vector_data"):
        self.vector_store_path = vector_store_path
        self.ingested_docs: List[DocumentMetadata] = []
        self.version = "1.0"
        logger.info(f"DocumentIngester initialized (path: {vector_store_path})")

    def discover_documents(self, root_path: str) -> List[str]:
        """
        Scopri tutti i documenti processabili.
        Cerca in: .md, .yaml, .yml, .txt
        """
        discovered = []
        root = Path(root_path)

        extensions = [".md", ".yaml", ".yml", ".txt"]

        for ext in extensions:
            discovered.extend([str(p) for p in root.rglob(f"*{ext}")])

        # Filter out common non-content files
        exclude_dirs = {".git", ".claude", "__pycache__", "node_modules"}
        filtered = [
            d for d in discovered
            if not any(ex in d for ex in exclude_dirs)
        ]

        logger.info(f"Discovered {len(filtered)} documents")
        return filtered

    def chunk_document(self, content: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Suddivide documento in chunks.
        In implementation reale: smarter chunking con sentences/paragraphs.
        """
        chunks = []
        lines = content.split("\n")

        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line)
            if current_size + line_size > chunk_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                # Keep overlap
                overlap_lines = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk[-1:]
                current_chunk = overlap_lines + [line]
                current_size = sum(len(l) for l in current_chunk)
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Estrae metadata da file"""
        path = Path(file_path)
        stat = path.stat()

        return {
            "source_path": file_path,
            "title": path.stem,
            "doc_type": path.suffix.lower(),
            "size_bytes": stat.st_size,
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

    def ingest_file(self, file_path: str) -> Optional[DocumentMetadata]:
        """
        Ingestisce singolo file.
        1. Legge contenuto
        2. Estrae metadata
        3. Chunking
        4. Genera embeddings (stub)
        5. Salva in vector store (stub)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return None

            # Read content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract metadata
            meta = self.extract_metadata(file_path)

            # Chunk
            chunks = self.chunk_document(content)
            logger.info(f"File chunked into {len(chunks)} pieces: {file_path}")

            # Stub: Generate embeddings (in real impl: call embedder)
            embeddings = [self._generate_embedding(c) for c in chunks]

            # Stub: Save to vector store (in real impl: LanceDB, ChromaDB)
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            metadata = DocumentMetadata(
                doc_id=doc_id,
                source_path=file_path,
                title=meta["title"],
                doc_type=meta["doc_type"],
                ingested_at=datetime.now().isoformat(),
                size_bytes=meta["size_bytes"],
                chunks_count=len(chunks)
            )

            self.ingested_docs.append(metadata)
            logger.info(f"Document ingested: {metadata.title} ({metadata.chunks_count} chunks)")

            return metadata

        except Exception as e:
            logger.error(f"Error ingesting {file_path}: {e}")
            return None

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding stub.
        In real implementation: nomic-embed-text or OpenAI embeddings.
        Returns random vector for testing.
        """
        import random
        dimension = 768
        return [random.uniform(-1, 1) for _ in range(dimension)]

    def ingest_directory(self, dir_path: str, recursive: bool = True) -> List[DocumentMetadata]:
        """
        Ingestisce tutti i documenti in una directory.
        """
        discovered = self.discover_documents(dir_path)
        results = []

        for doc_path in discovered:
            meta = self.ingest_file(doc_path)
            if meta:
                results.append(meta)

        logger.info(f"Directory ingest complete: {len(results)}/{len(discovered)} documents")
        return results

    def get_ingested_docs(self) -> List[DocumentMetadata]:
        """Lista documenti ingestiti"""
        return self.ingested_docs

    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Statistiche ingestione"""
        total_chunks = sum(d.chunks_count for d in self.ingested_docs)
        total_size = sum(d.size_bytes for d in self.ingested_docs)

        return {
            "total_documents": len(self.ingested_docs),
            "total_chunks": total_chunks,
            "total_size_bytes": total_size,
            "by_type": {
                doc_type: len([d for d in self.ingested_docs if d.doc_type == doc_type])
                for doc_type in set(d.doc_type for d in self.ingested_docs)
            }
        }


if __name__ == "__main__":
    # Test
    ingester = DocumentIngester()
    docs = ingester.discover_documents(".")
    print(f"Discovered {len(docs)} documents")

    # Ingest first few
    for doc in docs[:5]:
        ingester.ingest_file(doc)

    stats = ingester.get_ingestion_stats()
    print(f"Ingested: {stats}")
