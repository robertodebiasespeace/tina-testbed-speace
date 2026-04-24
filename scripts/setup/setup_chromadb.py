#!/usr/bin/env python3
"""
SPEACE ChromaDB Vector Store Setup
Configura e inizializza ChromaDB per memoria semantica

Versione: 1.0
Data: 21 aprile 2026
"""

import subprocess
import sys
import os
from pathlib import Path
import json

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def install_chromadb():
    """Installa ChromaDB"""
    print_header("INSTALLAZIONE CHROMADB")

    try:
        import chromadb
        print_success("ChromaDB già installato")
        print_info(f"Versione: {chromadb.__version__}")
        return True
    except ImportError:
        print_info("Installazione ChromaDB...")

    # Usa pip
    venv_pip = Path(".venv-speace-ml/Scripts/pip.exe")
    if venv_pip.exists():
        pip_cmd = str(venv_pip)
    else:
        pip_cmd = "pip"

    result = subprocess.run(
        [pip_cmd, "install", "chromadb>=0.4.0"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print_success("ChromaDB installato")
        return True
    else:
        print_error(f"Installazione fallita: {result.stderr}")
        return False

def setup_directories():
    """Crea directory per ChromaDB"""
    print_header("SETUP DIRECTORY")

    dirs = [
        "chroma_db",
        "chroma_db/backups",
        "chroma_db/logs",
    ]

    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_success(f"Directory creata: {directory}")

    return True

def initialize_chromadb():
    """Inizializza database ChromaDB"""
    print_header("INIZIALIZZAZIONE CHROMADB")

    try:
        import chromadb
        from chromadb.config import Settings

        print_info("Connessione a ChromaDB...")

        # Configura client con persistenza
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))

        # Crea collections per SPEACE
        collections = [
            ("documents", "Documenti ingegneristici e tecnici"),
            ("experiences", "Esperienze passate del sistema"),
            ("concepts", "Concetti e astrazioni"),
            ("proposals", "Proposte SafeProactive"),
        ]

        for coll_name, description in collections:
            try:
                collection = client.get_or_create_collection(coll_name)
                print_success(f"Collection creata: {coll_name} - {description}")
                print_info(f"  Elementi: {collection.count()}")
            except Exception as e:
                print_error(f"Errore creazione {coll_name}: {e}")

        # Persiste
        client.persist()
        print_success("Database persistito su disco")

        return True

    except Exception as e:
        print_error(f"Errore inizializzazione: {e}")
        return False

def install_sentence_transformers():
    """Installa sentence-transformers per embeddings"""
    print_header("INSTALLAZIONE SENTENCE-TRANSFORMERS")

    try:
        from sentence_transformers import SentenceTransformer
        print_success("Sentence-transformers già installato")

        # Verifica modello
        print_info("Download modello all-MiniLM-L6-v2...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print_success("Modello pronto")
        return True

    except ImportError:
        print_info("Installazione sentence-transformers...")

        venv_pip = Path(".venv-speace-ml/Scripts/pip.exe")
        pip_cmd = str(venv_pip) if venv_pip.exists() else "pip"

        result = subprocess.run(
            [pip_cmd, "install", "sentence-transformers>=2.2.0"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success("Sentence-transformers installato")
            return True
        else:
            print_error(f"Installazione fallita: {result.stderr}")
            return False

def create_sample_data():
    """Crea dati di esempio per testing"""
    print_header("CREAZIONE DATI ESEMPIO")

    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        from chromadb.config import Settings

        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))

        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Documenti esempio SPEACE
        sample_docs = [
            {
                "id": "doc_001",
                "text": "SPEACE (SuPer Entità Autonoma Cibernetica Evolutiva) è un super-organismo tecnico-biologico.",
                "source": "README.md",
                "type": "descrizione"
            },
            {
                "id": "doc_002",
                "text": "SMFOI-KERNEL implementa un protocollo 6-step per l'orientamento ricorsivo dell'intelligenza.",
                "source": "SMFOI_DOCUMENTATION",
                "type": "tecnico"
            },
            {
                "id": "doc_003",
                "text": "DigitalDNA utilizza un sistema genetico-epigenetico per l'evoluzione autonoma.",
                "source": "DigitalDNA",
                "type": "architettura"
            },
            {
                "id": "doc_004",
                "text": "SafeProactive garantisce approvazione umana per azioni ad alto rischio.",
                "source": "Security",
                "type": "sicurezza"
            },
        ]

        collection = client.get_collection("documents")

        for doc in sample_docs:
            embedding = model.encode(doc["text"]).tolist()

            collection.add(
                ids=[doc["id"]],
                embeddings=[embedding],
                documents=[doc["text"]],
                metadatas=[{
                    "source": doc["source"],
                    "type": doc["type"]
                }]
            )
            print_success(f"Documento inserito: {doc['id']}")

        # Test query
        print_info("\nTest query semantica...")
        query = "Come funziona l'intelligenza artificiale in SPEACE?"
        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )

        print_info(f"Query: '{query}'")
        print_info("Risultati:")
        for i, doc_id in enumerate(results['ids'][0]):
            distance = results['distances'][0][i]
            text = results['documents'][0][i][:50]
            print_info(f"  {doc_id}: {distance:.3f} - {text}...")

        client.persist()
        return True

    except Exception as e:
        print_error(f"Errore creazione dati: {e}")
        return False

def generate_config():
    """Genera file configurazione"""
    print_header("GENERAZIONE CONFIGURAZIONE")

    config = {
        "vector_store": {
            "type": "chromadb",
            "persist_directory": "chroma_db",
            "implementation": "duckdb+parquet",
            "collections": ["documents", "experiences", "concepts", "proposals"]
        },
        "embeddings": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "dimension": 384,
            "local": True,
            "device": "cpu"
        },
        "retrieval": {
            "default_n_results": 5,
            "similarity_threshold": 0.7,
            "max_distance": 1.0
        },
        "backup": {
            "enabled": True,
            "interval_hours": 24,
            "retention_days": 7,
            "path": "chroma_db/backups"
        }
    }

    config_path = Path("config/vector_store.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print_success(f"Configurazione salvata: {config_path}")

    # Salva anche in YAML
    try:
        import yaml
        yaml_path = Path("config/vector_store.yaml")
        with open(yaml_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print_success(f"Configurazione YAML: {yaml_path}")
    except ImportError:
        pass

    return True

def create_test_script():
    """Crea script di test"""
    print_header("CREAZIONE SCRIPT TEST")

    test_script = '''#!/usr/bin/env python3
"""
SPEACE Vector Store Test
Verifica funzionamento ChromaDB
"""

import sys
from pathlib import Path

def test_vector_store():
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        from chromadb.config import Settings

        print("Test connessione ChromaDB...")
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))

        # Test collection
        collection = client.get_collection("documents")
        count = collection.count()
        print(f"✓ Collection 'documents' trovata: {count} elementi")

        # Test query
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query = "intelligenza artificiale"
        embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[embedding],
            n_results=2
        )

        print(f"✓ Query eseguita: '{query}'")
        print(f"  Risultati trovati: {len(results['ids'][0])}")

        return True

    except Exception as e:
        print(f"✗ Test fallito: {e}")
        return False

if __name__ == "__main__":
    success = test_vector_store()
    sys.exit(0 if success else 1)
'''

    test_path = Path("scripts/test_vector_store.py")
    test_path.parent.mkdir(parents=True, exist_ok=True)

    with open(test_path, 'w') as f:
        f.write(test_script)

    print_success(f"Script test creato: {test_path}")
    return True

def main():
    """Main function"""
    print_header("SPEACE CHROMADB SETUP")
    print(f"Data: {__import__('datetime').datetime.now().isoformat()}")
    print()

    steps = [
        ("Install ChromaDB", install_chromadb),
        ("Setup directories", setup_directories),
        ("Install sentence-transformers", install_sentence_transformers),
        ("Initialize ChromaDB", initialize_chromadb),
        ("Create sample data", create_sample_data),
        ("Generate config", generate_config),
        ("Create test script", create_test_script),
    ]

    results = {}
    for step_name, step_func in steps:
        try:
            success = step_func()
            results[step_name] = "SUCCESS" if success else "FAILED"
        except Exception as e:
            print_error(f"Errore in {step_name}: {e}")
            results[step_name] = f"ERROR: {e}"

    # Summary
    print_header("SETUP SUMMARY")

    for step_name, result in results.items():
        status_icon = "✓" if result == "SUCCESS" else "✗"
        color = Colors.OKGREEN if result == "SUCCESS" else Colors.FAIL
        print(f"{color}{status_icon} {step_name}: {result}{Colors.ENDC}")

    all_success = all(r == "SUCCESS" for r in results.values())

    if all_success:
        print_header("SETUP COMPLETATO CON SUCCESSO")
        print_info("ChromaDB pronto per SPEACE Semantic Memory")
        print_info("Prossimo passo: implementare SPEACESemanticMemory")
        print_info("Test: python scripts/test_vector_store.py")
        return 0
    else:
        print_header("SETUP COMPLETATO CON ERRORI")
        return 1

if __name__ == "__main__":
    sys.exit(main())
