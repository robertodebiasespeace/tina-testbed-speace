# SPEACE Machine Learning Environment Setup

**Documento:** README_ML.md  
**Versione:** 1.1  
**Data:** 23 aprile 2026  
**Task:** ML-001 — Setup Environment ML

---

## Stato

| Componente | Versione Installata | CUDA | Status |
|---|---|---|---|
| Python | 3.12.10 | N/A | Sistema ML |
| PyTorch | 2.5.1+cu121 | 12.1 | **OK** |
| River | 0.24.2 | N/A | OK |
| Stable-Baselines3 | 2.8.0 | 12.1 | OK |
| sentence-transformers | 5.4.1 | N/A | OK |
| scikit-learn | 1.8.0 | N/A | OK |
| numpy | 2.4.3 | N/A | OK |

---

## Virtual Environment

### venv_ml (consigliato — con CUDA)

Creato in: `venv_ml/` (Python 3.12.10)

Attivazione:
```bash
# Windows (Git Bash / MSYS)
source venv_ml/Scripts/activate

# Windows (CMD)
venv_ml\Scripts\activate.bat

# Windows (PowerShell)
venv_ml\Scripts\Activate.ps1
```

### venv (legacy — CPU-only, Python 3.14)

Creato in: `venv/` (Python 3.14.2)

Usare solo se necessario compatibilita con codice Python 3.14.

---

## Installazione (venv_ml con CUDA)

### Prerequisiti

1. Installare **Python 3.12** via winget:
   ```bash
   winget install --id Python.Python.3.12 --exact
   ```
2. Verificare il percorso:
   ```bash
   C:\Users\rober\AppData\Local\Programs\Python\Python312\python.exe --version
   ```

### Passo 1: Creare venv

```bash
C:\Users\rober\AppData\Local\Programs\Python\Python312\python.exe -m venv venv_ml
```

### Passo 2: PyTorch con CUDA 12.1

```bash
venv_ml\Scripts\python.exe -m pip install --upgrade pip
venv_ml\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Passo 3: River (Online Learning)

```bash
venv_ml\Scripts\python.exe -m pip install river
```

### Passo 4: Stable-Baselines3 (Reinforcement Learning)

```bash
venv_ml\Scripts\python.exe -m pip install stable-baselines3
```

### Passo 5: Sentence Transformers (Embeddings)

```bash
venv_ml\Scripts\python.exe -m pip install sentence-transformers
```

---

## Verifica

### Verifica import moduli

```bash
venv_ml\Scripts\python.exe -c "import river, torch, stable_baselines3, sentence_transformers; print('OK')"
```

Output atteso:
```
OK
```

### Verifica GPU / CUDA

```bash
venv_ml\Scripts\python.exe -c "import torch; print(torch.cuda.is_available())"
```

Output atteso:
```
True
```

Verifica dettagliata GPU:
```bash
venv_ml\Scripts\python.exe -c "import torch; print('torch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"
```

Output atteso:
```
torch: 2.5.1+cu121
CUDA: True
GPU: NVIDIA GeForce RTX 3060 Laptop GPU
```

---

## Nota sulla Compatibilita CUDA / GPU RTX 3060

**Risolto il 23 aprile 2026.** Installando Python 3.12 e PyTorch `cu121`, CUDA e' ora pienamente funzionante.

**Hardware confermato:**
- GPU: NVIDIA GeForce RTX 3060 Laptop GPU
- Driver: 552.12
- CUDA Driver: 12.4
- CUDA Runtime (PyTorch): 12.1
- VRAM: 6 GB

**Limitazione precedente (documentata per riferimento):**
Su Python 3.14 non esistono wheel PyTorch con CUDA. L'ambiente `venv/` (Python 3.14.2) resta disponibile con `torch 2.11.0+cpu` per eventuali test di compatibilita con Python 3.14.

---

## Dipendenze aggiuntive installate automaticamente

- numpy 2.4.3
- scipy 1.17.1
- pandas 2.3.3
- scikit-learn 1.8.0
- matplotlib 3.10.8
- gymnasium 1.2.3
- transformers 5.6.0
- huggingface-hub 1.11.0
- pillow 12.1.1
- pyyaml 6.0.3
- regex 2026.4.4
- tqdm 4.67.3

---

## Criteri Completamento ML-001

| Criterio | Stato | Note |
|---|---|---|
| `python -c "import river, torch, stable_baselines3; print('OK')"` | **OK** | Eseguito con successo su venv_ml |
| GPU rilevata da PyTorch (`torch.cuda.is_available()` = True) | **OK** | RTX 3060 riconosciuta, CUDA 12.1 attivo |
| Tutti i moduli importabili senza errori | **OK** | Verificato |

---

**Autore:** SPEACE Cortex  
**Task Tracker:** docs/SPEACE-Tasks-Tracker.md — Area 1: Infrastruttura ML Proprietaria
