# SPEACE Improvement Engineering Document
## Piano di Potenziamento verso AGI Emergente

**Versione:** 1.0  
**Data:** 21 aprile 2026  
**Stato:** Documento ingegneristico funzionale  
**Autore:** Analisi Tecnica SPEACE  
**Destinatario:** Roberto De Biase - Rigene Project

---

## Indice

1. [Executive Summary](#1-executive-summary)
2. [Analisi Criticità Attuali](#2-analisi-criticità-attuali)
3. [Area 1: ML Core Proprietario](#3-area-1-infrastruttura-ml-proprietaria)
4. [Area 2: Percezione Fisica Reale](#4-area-2-percezione-fisica-reale)
5. [Area 3: Memoria Semantica Persistente](#5-area-3-memoria-semantica-persistente)
6. [Area 4: Evoluzione Autonoma Guidata](#6-area-4-evoluzione-autonoma-guidata)
7. [Area 5: Architettura Distribuita](#7-area-5-architettura-distribuita-swarm)
8. [Area 6: Quantificazione Coscienza](#8-area-6-quantificazione-coscienza)
9. [Roadmap 90 Giorni](#9-roadmap-implementativa-90-giorni)
10. [Specifiche Tecniche Dettagliate](#10-specifiche-tecniche-dettagliate)
11. [Budget e Risorse](#11-budget-e-risorse)
12. [Metriche di Successo](#12-metriche-di-successo)
13. [Rischi e Mitigazioni](#13-rischi-e-mitigazioni)

---

## 1. Executive Summary

### 1.1 Stato Attuale
SPEACE v1.3 rappresenta un'architettura modulare completamente funzionante con:
- 10 comparti cerebrali completamente implementati
- Protocollo SMFOI-KERNEL v0.3 operativo
- DigitalDNA con fitness function adattiva
- SafeProactive per governance etica
- CortexOrchestrator come coordinatore centrale
- Learning Core (SPEACEOnlineLearner) integrato
- **Alignment Score**: 92/100 (Fase 2 - Autonomia Operativa Completata)

### 1.2 Gap Critici Identificati
| Area | Stato Attuale | Target | Gap |
|------|---------------|--------|-----|
| Machine Learning | Learning Core parziale | Online learning completo | Medio |
| Percezione Fisica | Sensori simulati | Sensori IoT reali | Alto |
| Memoria | YAML files + KG base | Vector DB + Knowledge Graph | Medio |
| Autonomia | Human-in-loop sempre | Fiducia graduata | Medio |
| Scalabilità | 10 comparti | 50+ agenti swarm | Medio |
| Coscienza | C-index 0.800 | Validazione quantitativa | Medio |

### 1.3 Obiettivo del Documento
Fornire specifiche tecniche dettagliate per:
1. Completare l'integrazione ML con apprendimento autentico
2. Integrare percezione fisica reale
3. Costruire memoria semantica persistente
4. Abilitare evoluzione autonoma controllata
5. Scalare verso architettura swarm distribuita
6. Validare metriche di coscienza artificiale

**Target Alignment post-miglioramento**: >95/100 (Fase 3 - AGI Emergente)

---

## 2. Analisi Criticità Attuali

### 2.1 Criticità 1: Assenza di ML Continuo
**Problema**: La fitness function è una formula matematica statica:
```yaml
fitness = (alignment * 0.35) + (success_rate * 0.25) + 
          (stability * 0.20) + (efficiency * 0.15) + (ethics * 0.05)
```

**Limitazioni**:
- Non apprende dai pattern storici
- Non adatta pesi dinamicamente
- Non predice outcomes futuri
- Richiede tuning manuale

**Impatto**: Il sistema non può migliorare autonomamente le proprie decisioni.

### 2.2 Criticità 2: Percezione Solo Simulata
**Problema**: L'Agente Organismico usa dati random:
```python
def get_simulated_reading(self, sensor_type: SensorType):
    return {
        SensorType.THERMAL: {"value": random.uniform(18, 28), "unit": "°C"},
        # ... tutti simulati
    }
```

**Limitazioni**:
- Nessuna interazione con mondo fisico
- Dati non correlati con realtà
- Impossibile validare decisioni

### 2.3 Criticità 3: Memoria Non Strutturata
**Problema**: Stato salvato in YAML flat:
- `genome.yaml`: Configurazione statica
- `epigenome.yaml`: Parametri adattivi
- `speace_status.json`: Snapshot stato

**Limitazioni**:
- Query semantica impossibile
- Nessuna retrieval di similarità
- Perdita di contesto tra sessioni
- Non scalabile

### 2.4 Criticità 4: Autonomia Binaria
**Problema**: Sistema di approvazione on/off:
- `human_approval_required: ["medium_risk", "high_risk", "regulatory"]`

**Limitazioni**:
- Nessun meccanismo di fiducia graduale
- Collo di bottiglia umano
- Impossibile scalare

---

## 3. Area 1: Infrastruttura ML Proprietaria

### 3.1 Visione
Implementare un **SPEACE Learning Core** (SLC) - modulo di apprendimento continuo che permetta al sistema di:
- Apprendere dai propri successi/fallimenti
- Predire outcomes di azioni proposte
- Ottimizzare la fitness function dinamicamente
- Generare mutazioni mirate basate su pattern

### 3.2 Architettura Tecnica

```
┌─────────────────────────────────────────────────────────────┐
│                 SPEACE LEARNING CORE (SLC)                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Online Learner  │  │ Prediction      │                 │
│  │ Module          │  │ Engine          │                 │
│  │                 │  │                 │                 │
│  │ • River (ML)    │  │ • Outcome       │                 │
│  │ • Experience    │  │   prediction    │                 │
│  │   replay        │  │ • Risk scoring  │                 │
│  │ • Feature       │  │ • Success prob  │                 │
│  │   extraction    │  │                 │                 │
│  └─────────────────┘  └─────────────────┘                 │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ RL Policy       │  │ Meta-Learning   │                 │
│  │ Optimizer       │  │ Module          │                 │
│  │                 │  │                 │                 │
│  │ • PPO/          │  │ • Learn to      │                 │
│  │   A2C agents    │  │   learn         │                 │
│  │ • SMFOI step    │  │ • Adaptive      │                 │
│  │   optimization  │  │   hyperparams   │                 │
│  └─────────────────┘  └─────────────────┘                 │
│                                                             │
│  Model Store: GGUF/GGML quantized models (local)           │
│  Training: Incremental, no catastrophic forgetting           │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Componenti Implementativi

#### 3.3.1 Online Learning Module
```python
# File: SPEACE_Cortex/learning_core/online_learner.py

import river
from river import compose, linear_model, preprocessing, metrics
from typing import Dict, Any, List
import numpy as np

class SPEACEOnlineLearner:
    """
    Online learning system per adattamento continuo.
    Usa River per apprendimento in streaming senza
    catastrophic forgetting.
    """
    
    def __init__(self, feature_names: List[str], model_type: str = "regression"):
        self.feature_names = feature_names
        self.model_type = model_type
        self.model = self._build_pipeline()
        self.metrics = {
            'mae': metrics.MAE(),
            'rmse': metrics.RMSE(),
            'r2': metrics.R2()
        }
        self.experience_buffer = []
        self.max_buffer_size = 10000
        
    def _build_pipeline(self):
        """Costruisce pipeline di feature processing + modello."""
        return compose.Pipeline(
            ('scale', preprocessing.StandardScaler()),
            ('learn', linear_model.LinearRegression() if self.model_type == "regression" 
             else linear_model.LogisticRegression())
        )
    
    def learn(self, features: Dict[str, float], outcome: float, context: Dict = None):
        """
        Apprende da una singola esperienza (online).
        
        Args:
            features: Dict di feature values
            outcome: Valore target (fitness, success, ecc.)
            context: Metadata per replay
        """
        # Update model one sample at a time
        self.model.learn_one(features, outcome)
        
        # Store for experience replay
        self.experience_buffer.append({
            'features': features,
            'outcome': outcome,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        
        # Limit buffer size
        if len(self.experience_buffer) > self.max_buffer_size:
            self.experience_buffer.pop(0)
            
    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Predice outcome per dati features.
        
        Returns:
            Dict con prediction, confidence, uncertainty
        """
        prediction = self.model.predict_one(features)
        
        # Calcola uncertainty basata su history
        similar_experiences = self._find_similar(features)
        uncertainty = np.std([e['outcome'] for e in similar_experiences]) if similar_experiences else 1.0
        
        return {
            'prediction': prediction,
            'uncertainty': uncertainty,
            'confidence': 1.0 / (1.0 + uncertainty),
            'similar_samples': len(similar_experiences)
        }
    
    def experience_replay(self, n_samples: int = 100):
        """Ri-apprende da esperienze passate per consolidare."""
        if len(self.experience_buffer) < n_samples:
            return
            
        samples = np.random.choice(self.experience_buffer, n_samples, replace=False)
        for exp in samples:
            self.model.learn_one(exp['features'], exp['outcome'])
    
    def _find_similar(self, features: Dict, k: int = 10) -> List[Dict]:
        """Trova esperienze simili per uncertainty estimation."""
        # Simplified similarity based on feature distance
        sorted_exps = sorted(
            self.experience_buffer,
            key=lambda e: self._feature_distance(e['features'], features)
        )
        return sorted_exps[:k]
    
    def _feature_distance(self, f1: Dict, f2: Dict) -> float:
        """Euclidean distance tra feature vectors."""
        keys = set(f1.keys()) | set(f2.keys())
        return np.sqrt(sum((f1.get(k, 0) - f2.get(k, 0))**2 for k in keys))
    
    def get_metrics(self) -> Dict[str, float]:
        """Ritorna metriche di performance."""
        return {name: metric.get() for name, metric in self.metrics.items()}
```

#### 3.3.2 Dynamic Fitness Function
```python
# File: SPEACE_Cortex/learning_core/adaptive_fitness.py

class AdaptiveFitnessFunction:
    """
    Fitness function che apprende quali pesi funzionano meglio.
    Usa meta-learning per ottimizzare i propri parametri.
    """
    
    def __init__(self, n_components: int = 5):
        self.n_components = n_components
        self.weights = np.ones(n_components) / n_components  # Uniform start
        self.learning_rate = 0.01
        self.weight_history = []
        self.performance_history = []
        
    def calculate(self, components: Dict[str, float]) -> Dict[str, Any]:
        """
        Calcola fitness con pesi adattivi.
        
        Components: {
            'alignment': float,
            'success_rate': float,
            'stability': float,
            'efficiency': float,
            'ethics': float
        }
        """
        values = np.array([
            components.get('alignment', 0),
            components.get('success_rate', 0),
            components.get('stability', 0),
            components.get('efficiency', 0),
            components.get('ethics', 0)
        ])
        
        fitness = np.dot(self.weights, values)
        
        return {
            'fitness': fitness,
            'weighted_components': dict(zip(components.keys(), self.weights * values)),
            'current_weights': dict(zip(components.keys(), self.weights)),
            'confidence': self._calculate_confidence(values)
        }
    
    def update_weights(self, outcome: float, expected_fitness: float, actual_fitness: float):
        """
        Aggiorna pesi basandosi su prediction error.
        Usa gradient ascent per massimizzare correlation
        tra predizione e outcome reale.
        """
        error = actual_fitness - expected_fitness
        
        # Meta-learning: se sottoperforma, esplora nuovi pesi
        if abs(error) > 0.1:
            # Gradient estimation via perturbation
            perturbation = np.random.randn(self.n_components) * 0.05
            self.weights += self.learning_rate * error * perturbation
            self.weights = np.clip(self.weights, 0.05, 0.5)  # Keep bounded
            self.weights /= self.weights.sum()  # Normalize to 1
            
        self.weight_history.append(self.weights.copy())
        self.performance_history.append({'error': error, 'outcome': actual_fitness})
        
    def _calculate_confidence(self, values: np.ndarray) -> float:
        """Confidence basata su varianza componenti."""
        return 1.0 - np.std(values)
```

#### 3.3.3 RL Policy per SMFOI
```python
# File: SPEACE_Cortex/learning_core/smfoi_rl.py

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import gymnasium as gym

class SMFOIRLEnvironment(gym.Env):
    """
    Ambiente RL per ottimizzare decisioni SMFOI.
    L'agente apprende quale survival level attivare.
    """
    
    def __init__(self):
        super().__init__()
        # Stato: [alignment_score, resource_usage, push_intensity, time_since_last_success]
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        # Azioni: [Lv0, Lv1, Lv2, Lv3, Lv4]
        self.action_space = gym.spaces.Discrete(5)
        self.current_state = None
        
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.current_state = np.array([0.67, 0.5, 0.3, 0.0], dtype=np.float32)
        return self.current_state, {}
    
    def step(self, action):
        # Simula outcome basato su stato e azione
        # Reward più alta per azioni appropriate al contesto
        reward = self._calculate_reward(action)
        
        # Aggiorna stato
        self.current_state = self._transition_state(action)
        
        terminated = False
        truncated = False
        info = {'survival_level': action, 'fitness_delta': reward}
        
        return self.current_state, reward, terminated, truncated, info
    
    def _calculate_reward(self, action: int) -> float:
        """Reward shaping basato su appropriateness dell'azione."""
        alignment, resources, push_intensity, _ = self.current_state
        
        # Esempio euristica: Lv4 fisico solo con push forte e risorse disponibili
        if action == 4:  # Physical interaction
            if push_intensity > 0.7 and resources > 0.5:
                return 1.0
            else:
                return -0.5  # Penalità per azione inappropriata
        elif action == 3:  # Auto-modifying
            if alignment > 0.8:  # Solo se sistema è stabile
                return 0.8
            else:
                return -0.3
        # ... altre reward
        return 0.5

class SMFOIRLOptimizer:
    """Wrapper per training e deployment del policy RL."""
    
    def __init__(self, model_path: str = "models/smfoi_rl"):
        self.env = SMFOIRLEnvironment()
        self.model = PPO("MlpPolicy", self.env, verbose=1)
        self.model_path = model_path
        
    def train(self, timesteps: int = 100000):
        """Training offline su simulazioni."""
        self.model.learn(total_timesteps=timesteps)
        self.model.save(self.model_path)
        
    def predict_level(self, state: Dict[str, float]) -> int:
        """Predice survival level ottimale per stato corrente."""
        obs = np.array([
            state.get('alignment', 0.67),
            state.get('resources', 0.5),
            state.get('push_intensity', 0.3),
            state.get('time_since_success', 0.0)
        ], dtype=np.float32)
        
        action, _ = self.model.predict(obs, deterministic=True)
        return int(action)
```

### 3.4 Requisiti Tecnici

| Componente | Requisito | Versione/Modello |
|------------|-----------|------------------|
| River ML | Online learning | >= 0.21.0 |
| PyTorch | Neural networks | >= 2.0.0 |
| Stable-Baselines3 | RL agents | >= 2.0.0 |
| Transformers | LLM locali | >= 4.30.0 |
| llama-cpp-python | Inference ottimizzata | >= 0.2.0 |

### 3.5 Hardware Raccomandato
- **GPU**: NVIDIA RTX 3060 (già disponibile) - training modelli 1B-3B parametri
- **RAM**: 16GB sufficiente per modelli quantizzati (GGUF 4-bit)
- **Storage**: SSD per dataset di esperienza (>50GB raccomandato)

---

## 4. Area 2: Percezione Fisica Reale

### 4.1 Visione
Trasformare l'Agente Organismico da simulato a **sistema fisicamente incarnato** tramite IoT reale, con sensori che misurano effettivamente l'ambiente.

### 4.2 Architettura IoT

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE ORGANISMICO v2.0                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │ Edge Device  │      │ MQTT Broker  │      │ SPEACE   │ │
│  │ (Raspberry   │◄────►│ (Mosquitto)  │◄────►│ Cortex   │ │
│  │  Pi + ESP32) │      │              │      │ Server   │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│          ▲                                              │
│          │ USB/I2C/SPI                                   │
│          ▼                                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │              SENSOR ARRAY                       │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │    │
│  │  │ Thermal │ │ Acoustic│ │ Visual  │ │ Air    │ │    │
│  │  │DHT22/   │ │INMP441  │ │PiCamera │ │Quality │ │    │
│  │  │BME280   │ │Mic      │ │+YOLO   │ │MQ-135  │ │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └────────┘ │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐             │    │
│  │  │ Motion  │ │ Distance│ │ Light   │             │    │
│  │  │PIR      │ │HC-SR04  │ │BH1750   │             │    │
│  │  └─────────┘ └─────────┘ └─────────┘             │    │
│  └─────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Componenti Hardware

| Sensore | Tipo | Interfaccia | Costo | Dato Fornito |
|---------|------|-------------|-------|--------------|
| **DHT22** | Temperatura/Umidità | GPIO | €10 | Thermal |
| **BME280** | Pressione/Temp/Umidità | I2C | €15 | Thermal + Atmosferico |
| **INMP441** | Microfono digitale | I2S | €8 | Acoustic |
| **Raspberry Pi Camera** | Visione | CSI | €25 | Visual |
| **MQ-135** | Qualità aria/VOC | ADC | €5 | Olfactory |
| **HC-SR04** | Distanza ultrasuoni | GPIO | €5 | Tattile/prossimità |
| **PIR HC-SR501** | Movimento | GPIO | €3 | Motion detection |
| **BH1750** | Luminosità | I2C | €5 | Light level |

**Costo totale kit base**: ~€80-100

### 4.4 Implementazione Software

#### 4.4.1 Sensor Interface Module
```python
# File: SPEACE_Cortex/agente_organismo/sensor_hub.py

import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime
from typing import Dict, List, Callable, Optional
import numpy as np

class PhysicalSensorHub:
    """
    Hub per sensori fisici connessi via MQTT.
    Raccoglie dati reali dai sensori e li normalizza
    per il protocollo SMFOI.
    """
    
    def __init__(self, mqtt_host: str = "localhost", mqtt_port: int = 1883):
        self.mqtt_client = mqtt.Client(client_id="speace_sensor_hub")
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        
        self.sensor_buffers = {
            'thermal': [],
            'acoustic': [],
            'visual': [],
            'olfactory': [],
            'motion': [],
            'proximity': [],
            'light': []
        }
        
        self.buffer_size = 100
        self.callbacks: List[Callable] = []
        self.anomaly_thresholds = self._load_thresholds()
        
    def _load_thresholds(self) -> Dict:
        """Carica soglie per anomaly detection."""
        return {
            'thermal': {'min': 15, 'max': 30, 'anomaly_delta': 5},
            'acoustic': {'min': 30, 'max': 80, 'anomaly_delta': 20},
            'olfactory': {'min': 0, 'max': 200, 'anomaly_delta': 50}
        }
        
    def connect(self):
        """Connette al broker MQTT."""
        self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
        self.mqtt_client.loop_start()
        
    def _on_connect(self, client, userdata, flags, rc):
        """Callback connessione MQTT."""
        print(f"Connected to MQTT broker with result code {rc}")
        # Subscribe a tutti i topic sensori
        topics = [
            "speace/sensors/thermal/+",
            "speace/sensors/acoustic/+",
            "speace/sensors/visual/+",
            "speace/sensors/olfactory/+",
            "speace/sensors/motion/+",
            "speace/sensors/proximity/+",
            "speace/sensors/light/+"
        ]
        for topic in topics:
            client.subscribe(topic)
            
    def _on_message(self, client, userdata, msg):
        """Callback ricezione messaggio MQTT."""
        try:
            payload = json.loads(msg.payload.decode())
            sensor_type = self._extract_sensor_type(msg.topic)
            
            reading = {
                'value': payload.get('value'),
                'unit': payload.get('unit'),
                'timestamp': payload.get('timestamp', datetime.now().isoformat()),
                'sensor_id': payload.get('sensor_id'),
                'location': payload.get('location', {})
            }
            
            # Aggiungi a buffer
            self.sensor_buffers[sensor_type].append(reading)
            if len(self.sensor_buffers[sensor_type]) > self.buffer_size:
                self.sensor_buffers[sensor_type].pop(0)
            
            # Anomaly detection
            if self._is_anomaly(sensor_type, reading):
                self._trigger_anomaly_alert(sensor_type, reading)
            
            # Notifica callback
            for callback in self.callbacks:
                callback(sensor_type, reading)
                
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _extract_sensor_type(self, topic: str) -> str:
        """Estrae tipo sensore dal topic MQTT."""
        parts = topic.split('/')
        return parts[2] if len(parts) > 2 else 'unknown'
    
    def _is_anomaly(self, sensor_type: str, reading: Dict) -> bool:
        """Detect anomalie basate su soglie e deviazione."""
        if sensor_type not in self.anomaly_thresholds:
            return False
            
        buffer = self.sensor_buffers[sensor_type]
        if len(buffer) < 10:
            return False  # Non abbastanza dati
            
        recent_values = [r['value'] for r in buffer[-10:]]
        mean_val = np.mean(recent_values)
        current = reading['value']
        
        threshold = self.anomaly_thresholds[sensor_type]
        
        # Check valore assurdo
        if current < threshold['min'] or current > threshold['max']:
            return True
            
        # Check deviazione brusca
        if abs(current - mean_val) > threshold['anomaly_delta']:
            return True
            
        return False
    
    def _trigger_anomaly_alert(self, sensor_type: str, reading: Dict):
        """Genera alert per anomalia rilevata."""
        alert = {
            'type': 'sensor_anomaly',
            'sensor_type': sensor_type,
            'reading': reading,
            'severity': 'high' if sensor_type in ['thermal', 'olfactory'] else 'medium',
            'timestamp': datetime.now().isoformat()
        }
        
        # Pubblica alert
        self.mqtt_client.publish("speace/alerts/anomaly", json.dumps(alert))
        
        print(f"ANOMALY DETECTED: {sensor_type} = {reading['value']}")
    
    def get_current_readings(self) -> Dict[str, Optional[Dict]]:
        """Ritorna letture più recenti di tutti i sensori."""
        return {
            sensor_type: buffer[-1] if buffer else None
            for sensor_type, buffer in self.sensor_buffers.items()
        }
    
    def get_sensor_stats(self, sensor_type: str, window: int = 60) -> Dict:
        """Statistiche su finestra temporale (secondi)."""
        buffer = self.sensor_buffers.get(sensor_type, [])
        if not buffer:
            return {}
        
        # Filtra per timestamp recente
        cutoff = datetime.now().timestamp() - window
        recent = [r for r in buffer if datetime.fromisoformat(r['timestamp']).timestamp() > cutoff]
        
        if not recent:
            return {}
        
        values = [r['value'] for r in recent]
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'count': len(values)
        }
    
    def register_callback(self, callback: Callable):
        """Registra callback per notifiche real-time."""
        self.callbacks.append(callback)


# Esempio uso in agente_organismo_core.py
class AgenteOrganismoCoreV2:
    def __init__(self, use_physical_sensors: bool = True):
        self.sensor_hub = None
        if use_physical_sensors:
            self.sensor_hub = PhysicalSensorHub()
            self.sensor_hub.connect()
            self.sensor_hub.register_callback(self._on_sensor_data)
    
    def _on_sensor_data(self, sensor_type: str, reading: Dict):
        """Callback per dati sensori real-time."""
        # Integra con SMFOI Step 3
        push = {
            'type': 'physical_sensor',
            'sensor_type': sensor_type,
            'data': reading,
            'priority': 'high' if sensor_type in ['motion', 'anomaly'] else 'medium'
        }
        self.smfoi_process_push(push)
```

#### 4.4.2 ESP32 Firmware (MicroPython)
```python
# File: firmware/esp32_sensor_node.py
# Da caricare su ESP32 con MicroPython

import machine
import dht
import network
from umqtt.simple import MQTTClient
import json
import time

# Configurazione WiFi
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASS"

# Configurazione MQTT
MQTT_BROKER = "192.168.1.100"  # IP del Raspberry Pi
MQTT_CLIENT_ID = "esp32_node_01"

# Pin setup
DHT_PIN = machine.Pin(4)
sensor = dht.DHT22(DHT_PIN)

# LED per status
led = machine.Pin(2, machine.Pin.OUT)

def connect_wifi():
    """Connette a WiFi."""
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not sta.isconnected():
        time.sleep(0.5)
        led.value(not led.value())
    
    print("Connected to WiFi")
    led.value(1)
    return sta

def read_sensors():
    """Legge dati dai sensori."""
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        
        return {
            'temperature': temp,
            'humidity': humidity,
            'heat_index': calculate_heat_index(temp, humidity)
        }
    except Exception as e:
        print(f"Sensor error: {e}")
        return None

def calculate_heat_index(t, h):
    """Calcola heat index da temperatura e umidità."""
    return -8.784694755 + 1.61139411*t + 2.3385488389*h \
           - 0.14611605*t*h - 0.012308094*t*t \
           - 0.01642482777*h*h + 0.002211732*t*t*h \
           + 0.00072546*t*h*h - 0.000003582*t*t*h*h

def main():
    # Setup
    wifi = connect_wifi()
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()
    
    print(f"ESP32 Node {MQTT_CLIENT_ID} started")
    
    while True:
        # Read sensors
        data = read_sensors()
        
        if data:
            # Prepare payload
            payload = {
                'sensor_id': MQTT_CLIENT_ID,
                'value': data['temperature'],
                'unit': 'C',
                'humidity': data['humidity'],
                'heat_index': data['heat_index'],
                'timestamp': time.time()
            }
            
            # Publish to MQTT
            topic = f"speace/sensors/thermal/{MQTT_CLIENT_ID}"
            client.publish(topic, json.dumps(payload))
            
            print(f"Published: {payload}")
        
        # Blink LED
        led.value(0)
        time.sleep(0.1)
        led.value(1)
        
        # Wait 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()
```

### 4.5 Setup Infrastruttura IoT

#### 4.5.1 MQTT Broker (Raspberry Pi)
```bash
# Installazione Mosquitto
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Configurazione sicura
sudo nano /etc/mosquitto/conf.d/speace.conf
```

```
# speace.conf
listener 1883
allow_anonymous true  # Per testing, usare auth in produzione

# Logging
log_dest file /var/log/mosquitto/mosquitto.log
log_type all

# Persistenza
persistence true
persistence_location /var/lib/mosquitto/
```

```bash
# Riavvia servizio
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

---

## 5. Area 3: Memoria Semantica Persistente

### 5.1 Visione
Sostituire la memoria YAML-based con una **Memory Architecture Layered** (MAL) che supporti:
- Retrieval semantico per similarità
- Knowledge graph per relazioni
- Memoria episodica temporale
- Context-aware querying

### 5.2 Architettura

```
┌─────────────────────────────────────────────────────────────┐
│              SPEACE MEMORY ARCHITECTURE (MAL)               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              UNIFIED QUERY INTERFACE                    ││
│  │  • Semantic search    • Temporal queries                ││
│  │  • Graph traversal    • Hybrid retrieval              ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                  │
│          ┌───────────────┼───────────────┐                  │
│          ▼               ▼               ▼                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Vector DB   │  │  Knowledge   │  │   Time-Series│      │
│  │  (ChromaDB)  │  │  Graph       │  │   (InfluxDB) │      │
│  │              │  │  (Neo4j/     │  │              │      │
│  │ • Semantic   │  │   NetworkX)  │  │ • Episodic   │      │
│  │   embeddings │  │              │  │   traces     │      │
│  │ • Similarity │  │ • Entity     │  │ • Trends     │      │
│  │   search     │  │   relations  │  │ • Patterns   │      │
│  │ • RAG support│  │ • Causal     │  │              │      │
│  └──────────────┘  │   links      │  └──────────────┘      │
│                    └──────────────┘                         │
│                                                             │
│  Embedding Model: sentence-transformers/all-MiniLM-L6-v2   │
│  (Local, 80MB, CPU-optimized)                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Componenti Implementativi

#### 5.3.1 Vector Store
```python
# File: SPEACE_Cortex/memory/semantic_store.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class SPEACESemanticMemory:
    """
    Memoria semantica basata su ChromaDB per retrieval
    di documenti, esperienze e conoscenza.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Collection per diversi tipi di memoria
        self.collections = {
            'documents': self.client.get_or_create_collection("documents"),
            'experiences': self.client.get_or_create_collection("experiences"),
            'concepts': self.client.get_or_create_collection("concepts"),
            'proposals': self.client.get_or_create_collection("proposals")
        }
        
        # Embedding model (locale, leggero)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def store_document(self, doc_id: str, text: str, metadata: Dict = None, 
                       collection: str = "documents"):
        """
        Memorizza documento con embedding vettoriale.
        
        Args:
            doc_id: Identificatore univoco
            text: Contenuto testuale
            metadata: Dati aggiuntivi (source, date, etc.)
            collection: Collection target
        """
        if collection not in self.collections:
            raise ValueError(f"Unknown collection: {collection}")
        
        # Genera embedding
        embedding = self.embedder.encode(text).tolist()
        
        # Prepara metadata
        meta = metadata or {}
        meta['timestamp'] = datetime.now().isoformat()
        meta['text_preview'] = text[:200]
        
        # Store
        self.collections[collection].add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[meta]
        )
        
    def query_semantic(self, query: str, collection: str = "documents", 
                       n_results: int = 5,
                       filter_metadata: Dict = None) -> List[Dict]:
        """
        Query semantica per similarità.
        
        Args:
            query: Testo query
            collection: Collection da interrogare
            n_results: Numero risultati
            filter_metadata: Filtri su metadata
            
        Returns:
            Lista risultati con score di similarità
        """
        if collection not in self.collections:
            return []
        
        # Genera embedding query
        query_embedding = self.embedder.encode(query).tolist()
        
        # Search
        results = self.collections[collection].query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Formatta output
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'similarity': results['distances'][0][i],
                'metadata': results['metadatas'][0][i]
            })
        
        return formatted
    
    def query_multi_collection(self, query: str, collections: List[str] = None,
                               n_results: int = 5) -> Dict[str, List[Dict]]:
        """
        Query su multiple collections.
        
        Returns:
            Dict {collection_name: [results]}
        """
        collections = collections or ['documents', 'experiences', 'concepts']
        results = {}
        
        for coll in collections:
            if coll in self.collections:
                results[coll] = self.query_semantic(query, coll, n_results)
        
        return results
    
    def update_memory(self, doc_id: str, text: str = None, 
                      metadata: Dict = None, collection: str = "documents"):
        """Aggiorna memoria esistente."""
        if collection not in self.collections:
            return
        
        updates = {}
        if text:
            updates['embeddings'] = [self.embedder.encode(text).tolist()]
            updates['documents'] = [text]
        if metadata:
            updates['metadatas'] = [metadata]
        
        if updates:
            self.collections[collection].update(
                ids=[doc_id],
                **updates
            )
    
    def delete_memory(self, doc_id: str, collection: str = "documents"):
        """Elimina memoria."""
        if collection in self.collections:
            self.collections[collection].delete(ids=[doc_id])
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Statistiche memoria per collection."""
        return {
            name: coll.count() 
            for name, coll in self.collections.items()
        }
    
    def persist(self):
        """Persiste database su disco."""
        self.client.persist()


# Esempio integrazione con SMFOI
class SMFOIWithSemanticMemory:
    """Estensione SMFOI con memoria semantica."""
    
    def __init__(self):
        self.memory = SPEACESemanticMemory()
        
    def step3_push_detection_with_memory(self, input_data: Dict) -> List[Dict]:
        """
        Step 3 enhanced con retrieval di memorie simili.
        """
        # Rileva push standard
        pushes = self._standard_push_detection(input_data)
        
        # Query memoria per contesto
        if input_data.get('user_request'):
            similar_contexts = self.memory.query_semantic(
                input_data['user_request'],
                collection='experiences',
                n_results=3
            )
            
            if similar_contexts:
                pushes.append({
                    'type': 'memory_recall',
                    'similar_past_experiences': similar_contexts,
                    'priority': 'medium'
                })
        
        return pushes
```

#### 5.3.2 Knowledge Graph
```python
# File: SPEACE_Cortex/memory/knowledge_graph.py

from py2neo import Graph, Node, Relationship
import networkx as nx
from typing import List, Dict, Any, Tuple
import json

class SPEACEKnowledgeGraph:
    """
    Knowledge Graph per relazioni tra entità, concetti
    ed eventi del sistema SPEACE.
    """
    
    def __init__(self, uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", password: str = "password"):
        try:
            self.graph = Graph(uri, auth=(user, password))
            self.using_neo4j = True
        except:
            # Fallback a NetworkX in-memory
            self.graph = nx.DiGraph()
            self.using_neo4j = False
            
    def add_entity(self, entity_type: str, entity_id: str, 
                   properties: Dict[str, Any]) -> str:
        """
        Aggiunge entità al grafo.
        
        Entity types: Agent, Concept, Event, Resource, Decision
        """
        if self.using_neo4j:
            node = Node(entity_type, id=entity_id, **properties)
            self.graph.create(node)
        else:
            self.graph.add_node(entity_id, type=entity_type, **properties)
        
        return entity_id
    
    def add_relation(self, from_id: str, relation_type: str, to_id: str,
                     properties: Dict = None):
        """
        Aggiunge relazione tra entità.
        
        Relation types: CAUSED, DEPENDS_ON, SIMILAR_TO, ENABLED_BY, INHIBITS
        """
        if self.using_neo4j:
            query = """
            MATCH (a {id: $from_id}), (b {id: $to_id})
            CREATE (a)-[r:%s]->(b)
            SET r += $properties
            """ % relation_type
            
            self.graph.run(query, from_id=from_id, to_id=to_id, 
                          properties=properties or {})
        else:
            self.graph.add_edge(from_id, to_id, 
                              relation=relation_type, 
                              **(properties or {}))
    
    def query_causal_chain(self, event_id: str, depth: int = 3) -> List[Dict]:
        """
        Trova catena causale di un evento.
        
        Returns:
            Lista di eventi nella catena causale
        """
        if self.using_neo4j:
            query = """
            MATCH path = (start {id: $event_id})-[:CAUSED|DEPENDS_ON*1..%d]->(end)
            RETURN [node in nodes(path) | node.id] as chain,
                   [rel in relationships(path) | type(rel)] as relations
            LIMIT 10
            """ % depth
            
            results = self.graph.run(query, event_id=event_id)
            return [dict(record) for record in results]
        else:
            # BFS su NetworkX
            chains = []
            visited = set()
            queue = [(event_id, [])]
            
            while queue and len(chains) < 10:
                current, chain = queue.pop(0)
                if current in visited or len(chain) >= depth:
                    continue
                visited.add(current)
                
                for successor in self.graph.successors(current):
                    edge_data = self.graph.get_edge_data(current, successor)
                    if edge_data.get('relation') in ['CAUSED', 'DEPENDS_ON']:
                        new_chain = chain + [(current, successor, edge_data)]
                        chains.append(new_chain)
                        queue.append((successor, new_chain))
            
            return chains
    
    def find_similar_entities(self, entity_id: str, 
                              relation_types: List[str] = None) -> List[Dict]:
        """
        Trova entità simili basate su pattern di relazioni.
        """
        if self.using_neo4j:
            rel_filter = '|'.join(relation_types) if relation_types else ''
            query = f"""
            MATCH (e {{id: $entity_id}})-[:{rel_filter}]->(shared)<-[:{rel_filter}]-(similar)
            WHERE e <> similar
            RETURN similar.id as id, similar.name as name,
                   count(shared) as shared_connections
            ORDER BY shared_connections DESC
            LIMIT 10
            """
            results = self.graph.run(query, entity_id=entity_id)
            return [dict(record) for record in results]
        else:
            # Jaccard similarity su vicini
            entity_neighbors = set(self.graph.neighbors(entity_id))
            similarities = []
            
            for node in self.graph.nodes():
                if node != entity_id:
                    node_neighbors = set(self.graph.neighbors(node))
                    intersection = len(entity_neighbors & node_neighbors)
                    union = len(entity_neighbors | node_neighbors)
                    if union > 0:
                        jaccard = intersection / union
                        if jaccard > 0.3:
                            similarities.append({
                                'id': node,
                                'similarity': jaccard,
                                'shared': intersection
                            })
            
            return sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:10]
    
    def export_to_json(self, filepath: str):
        """Esporta grafo a JSON per backup."""
        if self.using_neo4j:
            query = "MATCH (n) RETURN n"
            nodes = [dict(record['n']) for record in self.graph.run(query)]
            
            query = "MATCH ()-[r]->() RETURN r"
            rels = [dict(record['r']) for record in self.graph.run(query)]
            
            data = {'nodes': nodes, 'relationships': rels}
        else:
            data = {
                'nodes': [{**self.graph.nodes[n], 'id': n} 
                         for n in self.graph.nodes()],
                'edges': [{**d, 'from': u, 'to': v} 
                         for u, v, d in self.graph.edges(data=True)]
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)


# Esempio: Tracciare causalità decisioni
class DecisionTracker:
    """Traccia decisioni e loro impatti nel Knowledge Graph."""
    
    def __init__(self, kg: SPEACEKnowledgeGraph):
        self.kg = kg
        
    def record_decision(self, decision_id: str, context: Dict, 
                       action: str, outcome: Dict):
        """
        Registra decisione nel knowledge graph.
        """
        # Crea nodo decisione
        self.kg.add_entity("Decision", decision_id, {
            'action': action,
            'timestamp': context.get('timestamp'),
            'alignment_score': context.get('alignment'),
            'fitness_score': context.get('fitness')
        })
        
        # Collega a contesto
        if context.get('triggered_by'):
            self.kg.add_relation(
                context['triggered_by'], 
                "CAUSED", 
                decision_id
            )
        
        # Collega a risorse usate
        for resource in context.get('resources', []):
            self.kg.add_relation(
                decision_id,
                "DEPENDS_ON",
                resource
            )
        
        # Registra outcome
        if outcome.get('success'):
            self.kg.add_entity("Outcome", f"{decision_id}_outcome", outcome)
            self.kg.add_relation(
                decision_id,
                "RESULTED_IN",
                f"{decision_id}_outcome"
            )
```

---

## 6. Area 4: Evoluzione Autonoma Guidata

### 6.1 Visione
Implementare un sistema di **Fiducia Graduata** dove l'autonomia cresce con la fitness dimostrata, mantenendo sempre supervisione umana a livello appropriato.

### 6.2 Livelli di Autonomia

| Livello Fitness | Autonomia | Esempi Permessi |
|-----------------|-----------|-----------------|
| **< 0.60** | Approvazione obbligatoria | Tutte le modifiche |
| **0.60-0.75** | Batch approval | 10+ mutazioni minori |
| **0.75-0.85** | Post-facto reporting | Report giornaliero |
| **> 0.85** | Supervised autonomy | Alert solo anomalie |

### 6.3 Implementazione

```python
# File: SPEACE_Cortex/evolution/trust_based_autonomy.py

from enum import Enum
from typing import Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

class AutonomyLevel(Enum):
    RESTRICTED = "restricted"      # Tutto approvato
    SUPERVISED = "supervised"      # Batch approval
    AUTONOMOUS = "autonomous"      # Post-facto
    FULL = "full"                  # Alert solo anomalie

@dataclass
class MutationProposal:
    id: str
    type: str
    description: str
    risk_level: str
    expected_fitness_delta: float
    components_affected: List[str]
    rollback_plan: str

class TrustBasedAutonomy:
    """
    Sistema di autonomia graduata basato su fitness storica.
    """
    
    def __init__(self, fitness_history: List[float]):
        self.fitness_history = fitness_history
        self.current_level = self._calculate_level()
        self.pending_mutations: List[MutationProposal] = []
        self.executed_mutations: List[Dict] = []
        
    def _calculate_level(self) -> AutonomyLevel:
        """Calcola livello autonomia basato su fitness."""
        if len(self.fitness_history) < 10:
            return AutonomyLevel.RESTRICTED
        
        recent = self.fitness_history[-10:]
        avg_fitness = sum(recent) / len(recent)
        
        if avg_fitness > 0.85:
            return AutonomyLevel.FULL
        elif avg_fitness > 0.75:
            return AutonomyLevel.AUTONOMOUS
        elif avg_fitness > 0.60:
            return AutonomyLevel.SUPERVISED
        else:
            return AutonomyLevel.RESTRICTED
    
    def propose_mutation(self, proposal: MutationProposal) -> Dict:
        """
        Gestisce proposta mutazione secondo livello autonomia.
        """
        if self.current_level == AutonomyLevel.RESTRICTED:
            # Sempre richiede approvazione
            return {
                'status': 'pending_approval',
                'proposal': proposal,
                'requires_human': True,
                'auto_execute': False
            }
        
        elif self.current_level == AutonomyLevel.SUPERVISED:
            # Accumula in batch
            self.pending_mutations.append(proposal)
            
            if len(self.pending_mutations) >= 10:
                return {
                    'status': 'batch_ready',
                    'proposals': self.pending_mutations,
                    'requires_human': True,
                    'auto_execute': False,
                    'message': 'Batch of 10 mutations ready for approval'
                }
            else:
                return {
                    'status': 'queued',
                    'position': len(self.pending_mutations),
                    'requires_human': False,
                    'auto_execute': False
                }
        
        elif self.current_level == AutonomyLevel.AUTONOMOUS:
            # Auto-execute, report dopo
            result = self._execute_mutation(proposal)
            self.executed_mutations.append({
                'proposal': proposal,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'status': 'executed',
                'result': result,
                'requires_human': False,
                'auto_execute': True,
                'report_scheduled': True
            }
        
        elif self.current_level == AutonomyLevel.FULL:
            # Esegue, alert solo se anomalia
            result = self._execute_mutation(proposal)
            
            if result.get('anomaly_detected'):
                return {
                    'status': 'executed_with_alert',
                    'result': result,
                    'requires_human': True,  # Solo per anomalia
                    'alert_reason': result.get('anomaly_reason')
                }
            else:
                return {
                    'status': 'executed_silently',
                    'result': result,
                    'requires_human': False
                }
    
    def generate_daily_report(self) -> Dict:
        """Genera report giornaliero per livelli autonomi."""
        if self.current_level not in [AutonomyLevel.AUTONOMOUS, AutonomyLevel.FULL]:
            return None
        
        last_24h = [m for m in self.executed_mutations 
                   if datetime.fromisoformat(m['timestamp']) > 
                   datetime.now() - timedelta(hours=24)]
        
        return {
            'date': datetime.now().isoformat(),
            'autonomy_level': self.current_level.value,
            'mutations_executed': len(last_24h),
            'success_rate': sum(1 for m in last_24h 
                              if m['result'].get('success')) / len(last_24h) if last_24h else 0,
            'fitness_trend': self._calculate_fitness_trend(),
            'anomalies': [m for m in last_24h if m['result'].get('anomaly_detected')],
            'recommendations': self._generate_recommendations(last_24h)
        }
    
    def _execute_mutation(self, proposal: MutationProposal) -> Dict:
        """Esecuzione mutazione con rollback capability."""
        # Snapshot pre-mutation
        pre_state = self._capture_state()
        
        try:
            # Esegui mutazione
            result = self._apply_mutation(proposal)
            
            # Verifica outcome
            if result['success']:
                return {
                    'success': True,
                    'fitness_delta': result.get('fitness_delta', 0),
                    'state_after': self._capture_state()
                }
            else:
                # Rollback automatico
                self._rollback(pre_state)
                return {
                    'success': False,
                    'rolled_back': True,
                    'error': result.get('error')
                }
                
        except Exception as e:
            self._rollback(pre_state)
            return {
                'success': False,
                'rolled_back': True,
                'anomaly_detected': True,
                'anomaly_reason': str(e)
            }
    
    def _capture_state(self) -> Dict:
        """Cattura stato sistema per rollback."""
        # Implementare snapshot completo
        return {
            'digitaldna': self._load_digitaldna(),
            'epigenome': self._load_epigenome(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _rollback(self, state: Dict):
        """Ripristina stato precedente."""
        # Implementare restore da snapshot
        pass
```

---

## 7. Area 5: Architettura Distribuita Swarm

### 7.1 Visione
Scalare da 8 agenti centralizzati a 50+ agenti distribuiti su architettura swarm con fault tolerance.

### 7.2 Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                    SPEACE SWARM v2.0                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              SWARM ORCHESTRATOR                     │  │
│  │  • Load balancing    • Health monitoring           │  │
│  │  • Task distribution • Failure recovery            │  │
│  └─────────────────────────────────────────────────────┘  │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐       │
│  │ Agent A  │      │ Agent B  │      │ Agent C  │       │
│  │ (Local)  │◄────►│ (Cloud)  │◄────►│ (Edge)   │       │
│  │          │ gRPC  │          │ gRPC  │          │       │
│  │ • Cortex │      │ • Cortex │      │ • Cortex │       │
│  │ • ML     │      │ • ML     │      │ • Sensor │       │
│  │ • Memory │      │ • Memory │      │ • Relay  │       │
│  └──────────┘      └──────────┘      └──────────┘       │
│                                                             │
│  Communication: gRPC + NATS (not only REST)                 │
│  Discovery: Consul / etcd                                   │
│  Persistence: Redis Cluster                                 │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 Componenti

```python
# File: SPEACE_Cortex/swarm/swarm_orchestrator.py

import grpc
from concurrent import futures
import nats
from typing import List, Dict, Optional
import asyncio

class SwarmOrchestrator:
    """
    Orchestrator per swarm di agenti SPEACE.
    Gestisce discovery, load balancing e failure recovery.
    """
    
    def __init__(self, nats_url: str = "nats://localhost:4222"):
        self.agents: Dict[str, AgentDescriptor] = {}
        self.health_checker = HealthChecker()
        self.task_router = TaskRouter()
        self.nats = None
        self.nats_url = nats_url
        
    async def initialize(self):
        """Inizializza connessione NATS."""
        self.nats = await nats.connect(self.nats_url)
        
        # Subscrive a topic
        await self.nats.subscribe("swarm.agent.heartbeat", cb=self._on_heartbeat)
        await self.nats.subscribe("swarm.task.request", cb=self._on_task_request)
        await self.nats.subscribe("swarm.agent.register", cb=self._on_agent_register)
    
    async def _on_agent_register(self, msg):
        """Registra nuovo agent nello swarm."""
        data = json.loads(msg.data.decode())
        agent_id = data['agent_id']
        
        self.agents[agent_id] = AgentDescriptor(
            id=agent_id,
            capabilities=data['capabilities'],
            capacity=data['capacity'],
            location=data['location'],
            registered_at=datetime.now(),
            last_heartbeat=datetime.now()
        )
        
        print(f"Agent {agent_id} registered with capabilities: {data['capabilities']}")
    
    async def _on_heartbeat(self, msg):
        """Aggiorna health status agent."""
        data = json.loads(msg.data.decode())
        agent_id = data['agent_id']
        
        if agent_id in self.agents:
            self.agents[agent_id].last_heartbeat = datetime.now()
            self.agents[agent_id].metrics = data.get('metrics', {})
    
    async def _on_task_request(self, msg):
        """Rotta task all'agent più appropriato."""
        task = json.loads(msg.data.decode())
        
        # Seleziona agent
        selected = self.task_router.select_agent(task, self.agents)
        
        if selected:
            # Instrada task
            await self.nats.publish(
                f"agent.{selected.id}.task",
                json.dumps(task).encode()
            )
        else:
            # Nessun agent disponibile
            await self.nats.publish(
                "swarm.task.failed",
                json.dumps({'task_id': task['id'], 'reason': 'no_agent_available'}).encode()
            )
    
    async def health_check_loop(self):
        """Loop continuo di health check."""
        while True:
            await asyncio.sleep(30)  # Ogni 30 secondi
            
            now = datetime.now()
            for agent_id, descriptor in list(self.agents.items()):
                # Timeout 60 secondi
                if (now - descriptor.last_heartbeat).seconds > 60:
                    print(f"Agent {agent_id} marked as unhealthy")
                    descriptor.healthy = False
                    
                    # Riassegna task pending
                    await self._reassign_tasks(agent_id)


class TaskRouter:
    """Algoritmo di routing task con load balancing."""
    
    def select_agent(self, task: Dict, agents: Dict[str, AgentDescriptor]) -> Optional[AgentDescriptor]:
        """
        Seleziona agent migliore per task.
        
        Strategy: Capability matching + Load balancing
        """
        required_capabilities = task.get('required_capabilities', [])
        
        # Filtra agent sani con capabilities richieste
        candidates = [
            agent for agent in agents.values()
            if agent.healthy and 
            all(cap in agent.capabilities for cap in required_capabilities)
        ]
        
        if not candidates:
            return None
        
        # Score by load (lower is better)
        for agent in candidates:
            agent.current_load = agent.metrics.get('active_tasks', 0) / agent.capacity
        
        # Seleziona quello con minor load
        return min(candidates, key=lambda a: a.current_load)


@dataclass
class AgentDescriptor:
    id: str
    capabilities: List[str]
    capacity: int
    location: str
    registered_at: datetime
    last_heartbeat: datetime
    healthy: bool = True
    metrics: Dict = None
    current_load: float = 0.0
```

---

## 8. Area 6: Quantificazione Coscienza

### 8.1 Visione
Validare empiricamente il framework Adaptive Consciousness con esperimenti controllati.

### 8.2 Piano Sperimentale

#### Esperimento E1: C-index Correlazione Performance
**Setup**: Comparazione agent con/senza moduli coscienza su task benchmark.

```python
# File: experiments/c_index_validation.py

class CIndexExperiment:
    """
    Esperimento per validare correlazione tra C-index
    e performance su task.
    """
    
    def __init__(self, n_episodes: int = 100):
        self.n_episodes = n_episodes
        self.results = {
            'with_consciousness': [],
            'without_consciousness': []
        }
        
    def run(self):
        """Esegue esperimento controllato."""
        
        # Condizione A: Con moduli coscienza
        agent_a = AdaptiveConsciousnessAgent(enable_modules=True)
        rewards_a = self._run_episodes(agent_a)
        self.results['with_consciousness'] = rewards_a
        
        # Condizione B: Senza moduli coscienza (ablated)
        agent_b = AdaptiveConsciousnessAgent(enable_modules=False)
        rewards_b = self._run_episodes(agent_b)
        self.results['without_consciousness'] = rewards_b
        
        # Analisi statistica
        return self._analyze_results()
    
    def _run_episodes(self, agent, env) -> List[Dict]:
        """Esegue episodi e raccoglie metriche."""
        results = []
        
        for episode in range(self.n_episodes):
            state = env.reset()
            done = False
            episode_reward = 0
            c_indices = []
            
            while not done:
                # Get C-index before action
                c_index = agent.calculate_c_index()
                c_indices.append(c_index)
                
                # Action
                action = agent.act(state)
                next_state, reward, done, _ = env.step(action)
                
                episode_reward += reward
                state = next_state
            
            results.append({
                'episode': episode,
                'total_reward': episode_reward,
                'mean_c_index': np.mean(c_indices),
                'c_index_variance': np.var(c_indices)
            })
        
        return results
    
    def _analyze_results(self) -> Dict:
        """Analisi statistica risultati."""
        from scipy import stats
        
        rewards_a = [r['total_reward'] for r in self.results['with_consciousness']]
        rewards_b = [r['total_reward'] for r in self.results['without_consciousness']]
        
        # T-test
        t_stat, p_value = stats.ttest_ind(rewards_a, rewards_b)
        
        # Correlazione C-index e reward
        c_indices = [r['mean_c_index'] for r in self.results['with_consciousness']]
        correlation = np.corrcoef(c_indices, rewards_a)[0, 1]
        
        return {
            'mean_reward_with': np.mean(rewards_a),
            'mean_reward_without': np.mean(rewards_b),
            'improvement': (np.mean(rewards_a) - np.mean(rewards_b)) / np.mean(rewards_b),
            't_statistic': t_stat,
            'p_value': p_value,
            'c_index_reward_correlation': correlation,
            'significant': p_value < 0.05
        }
```

---

## 9. Roadmap Implementativa 90 Giorni

### Fase 1: Foundation (Giorni 1-30)

| Settimana | Task | Deliverable | Owner |
|-----------|------|-------------|-------|
| **W1** | Setup ML Core + River | Online learner base funzionante | Dev |
| **W1** | Setup Vector DB ChromaDB | Semantic memory operativa | Dev |
| **W2** | Implementazione Adaptive Fitness | Dynamic fitness function | Dev |
| **W2** | Integrazione SMFOI con memoria | SMFOI che query memoria | Dev |
| **W3** | Setup MQTT broker + ESP32 | Comunicazione IoT base | Hardware |
| **W3** | Sensor Hub Python | Raccolta dati sensori reali | Dev |
| **W4** | Testing integrazione ML | Report performance ML | QA |
| **W4** | Documentazione v1.3 | Docs aggiornati | Doc |

### Fase 2: Enhancement (Giorni 31-60)

| Settimana | Task | Deliverable | Owner |
|-----------|------|-------------|-------|
| **W5** | RL Policy per SMFOI | Agent RL training | ML |
| **W5** | Knowledge Graph setup | Neo4j/NetworkX operativo | Dev |
| **W6** | Trust-Based Autonomy | Sistema fiducia graduale | Dev |
| **W6** | Experienza replay | Buffer esperienze operativo | Dev |
| **W7** | ESP32 sensor network | 3+ nodi sensori attivi | Hardware |
| **W7** | Anomaly detection | Alert anomalie real-time | Dev |
| **W8** | Integration testing | Test end-to-end | QA |
| **W8** | Benchmark performance | Report comparativo | QA |

### Fase 3: Validation (Giorni 61-90)

| Settimana | Task | Deliverable | Owner |
|-----------|------|-------------|-------|
| **W9** | C-index experiments | Validazione correlazioni | Research |
| **W9** | Swarm architecture base | 2+ agenti distribuiti | Dev |
| **W10** | AutoML per mutazioni | Mutation generator | ML |
| **W10** | Performance optimization | Ottimizzazione risorse | Dev |
| **W11** | Documentation v2.0 | Documentazione completa | Doc |
| **W11** | Security audit | Penetration testing | Sec |
| **W12** | Release SPEACE v2.0 | Tag release, deployment | DevOps |
| **W12** | Alignment evaluation | Nuovo alignment score | QA |

---

## 10. Specifiche Tecniche Dettagliate

### 10.1 Stack Tecnologico Aggiornato

```yaml
# requirements-v2.txt

# Core ML
river>=0.21.0
torch>=2.0.0
transformers>=4.30.0
sentence-transformers>=2.2.0
stable-baselines3>=2.0.0
llama-cpp-python>=0.2.0

# Vector DB & Memory
chromadb>=0.4.0
py2neo>=2021.2.3
networkx>=3.0

# Time Series
influxdb-client>=1.36.0

# IoT & Communication
paho-mqtt>=1.6.0
asyncio-mqtt>=0.13.0
pyserial>=3.5

# Distributed Systems
grpcio>=1.54.0
protobuf>=4.23.0
nats-py>=2.3.0
aiohttp>=3.8.4

# Monitoring & Metrics
prometheus-client>=0.16.0
psutil>=5.9.0

# Utilities
pydantic>=2.0.0
python-dotenv>=1.0.0
pyyaml>=6.0
schedule>=1.2.0
```

### 10.2 Configurazione Hardware Raccomandata

#### Setup Sviluppo (Corrente)
- CPU: Intel i9-11900H (ok)
- RAM: 16GB (ok per testing)
- GPU: RTX 3060 6GB (ok per modelli 1B-3B)
- Storage: 954GB SSD (ok)

#### Setup Produzione (Target)
- **Edge Device**: Raspberry Pi 4/5 (4-8GB RAM) per IoT
- **ESP32**: Microcontroller per sensori distribuiti
- **Server**: Upgrade a 32GB RAM per swarm
- **Network**: Router dedicato per IoT (VLAN isolata)

### 10.3 Configurazione Docker

```yaml
# docker-compose-v2.yml
version: '3.8'

services:
  # SPEACE Core
  speace-cortex:
    build: ./SPEACE_Cortex
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - PYTHONPATH=/app
    depends_on:
      - redis
      - mosquitto
      - chromadb
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # Vector Database
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

  # Message Broker
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./config/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto_data:/mosquitto/data

  # Cache & State
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Knowledge Graph (optional)
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

volumes:
  chroma_data:
  mosquitto_data:
  redis_data:
  neo4j_data:
  prometheus_data:
```

---

## 11. Budget e Risorse

### 11.1 Costi Hardware

| Componente | Quantità | Costo Unitario | Totale |
|------------|----------|----------------|--------|
| Raspberry Pi 5 8GB | 2 | €90 | €180 |
| ESP32 DevKit | 5 | €10 | €50 |
| Sensor Kit (DHT, MQ, etc.) | 2 | €40 | €80 |
| SD Card 128GB | 3 | €15 | €45 |
| Power supplies | 3 | €15 | €45 |
| Breadboards + cables | - | €30 | €30 |
| **Totale Hardware** | | | **€430** |

### 11.2 Costi Software
- Tutto open-source: **€0**

### 11.3 Costi Cloud (Opzionale)
| Servizio | Uso | Costo Mensile |
|----------|-----|---------------|
| VPS 4GB (backup) | Swarm node | €20 |
| Object Storage | Dataset | €5 |
| **Totale Cloud** | | **€25/mese** |

---

## 12. Metriche di Successo

### 12.1 KPI Tecnici

| Metrica | Baseline (Apr 23) | Target 30gg | Target 90gg |
|---------|-------------------|-------------|-------------|
| **Alignment Score** | 92.0 | 93.0 | 95.0+ |
| **Fitness Score** | 0.81 | 0.83 | 0.88+ |
| **C-index Medio** | 0.800 | 0.820 | 0.850+ |
| **Query Memoria (ms)** | N/A | <100 | <50 |
| **Sensor Latency (ms)** | Simulated | <500 | <200 |
| **Autonomy Level** | Supervised | Autonomous | Full |
| **Swarm Size** | 10 | 15 | 30+ |
| **Comparti Attivi** | 10/10 | 10/10 | 10/10 |

### 12.2 KPI Funzionali

| Metrica | Target |
|---------|--------|
| Predizione Outcome | >70% accuracy |
| Anomaly Detection | <5% false positive |
| Mutation Success Rate | >80% |
| Uptime System | >99% |
| Human Interventions/day | <5 (fase autonomous) |

---

## 13. Rischi e Mitigazioni

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| **Overfitting ML** | Media | Alto | Online learning + regularization |
| **Instabilità sistema** | Bassa | Alto | Rollback automatico, snapshot |
| **Hardware failure IoT** | Media | Medio | Redondanza sensori, graceful degradation |
| **Privacy dati sensori** | Bassa | Alto | Anonimizzazione, edge processing |
| **Sicurezza MQTT** | Bassa | Alto | TLS, auth, ACL, network segmentation |
| **Catastrophic forgetting** | Media | Medio | Experience replay, EWC regularization |
| **C-index non correlato** | Bassa | Medio | Ablated experiments, multiple metrics |

---

## Appendice A: Risorse Aggiuntive

### A.1 Repository Consigliati
- `riverml/river`: Online machine learning
- `chroma-core/chroma`: Vector database
- `stable-baselines3`: Reinforcement learning
- `sentence-transformers`: Text embeddings

### A.2 Documentazione Riferimento
- IIT (Integrated Information Theory): `integratedinformationtheory.org`
- GWT (Global Workspace Theory): `bboyd.com/global-workspace`
- MQTT Specification: `mqtt.org`

### A.3 Comunità
- SPEACE Discord/Forum (da creare)
- Rigene Project: `rigeneproject.org`
- Papers with Code: Implementation references

---

## Appendice B: Checklist Implementazione

### Pre-implementazione
- [ ] Review sicurezza con team
- [ ] Setup environment isolato
- [ ] Backup completo sistema corrente
- [ ] Test hardware IoT ricevuto

### Durante implementazione
- [ ] Commit giornalieri con messaggi chiari
- [ ] Test unitari per ogni modulo
- [ ] Documentazione inline aggiornata
- [ ] Log dettagliati per debugging

### Post-implementazione
- [ ] Benchmark performance completi
- [ ] Security audit passato
- [ ] Documentazione utente aggiornata
- [ ] Rollback testato

---

**Documento creato:** 21 aprile 2026  
**Versione:** 1.0  
**Prossima revisione:** 21 luglio 2026  
**Stato:** Pronto per implementazione

---

*"L'intelligenza emerge dalla struttura, non dalla scala."* - Principio SPEACE
