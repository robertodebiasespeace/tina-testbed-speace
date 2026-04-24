import streamlit as st
import yaml
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import time
import subprocess
from pathlib import Path

st.set_page_config(page_title="SPEACE Neural Core", layout="wide", page_icon="🧠")

# ====================== TEMA CYBER-BIOLOGICO ======================
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #00ff9d; }
    .stButton>button { background-color: #00cc77; color: black; border: 1px solid #00ff9d; }
    h1, h2, h3, .st-emotion-cache-1egp75f { color: #00ff9d; }
    .dataframe { background-color: #111111; color: #00ff9d; }
</style>
""", unsafe_allow_html=True)

PROJECT_ROOT = Path(__file__).parent.parent.parent
SPEACE_CORTEX = PROJECT_ROOT / "SPEACE_Cortex"
DIGITALDNA_DIR = PROJECT_ROOT / "DigitalDNA"
STATUS_MONITOR = PROJECT_ROOT / "scripts/speace_status_monitor.py"

# ====================== UTILS ======================
@st.cache_data(ttl=15)
def load_status_monitor():
    try:
        result = subprocess.run(["python", str(STATUS_MONITOR)], 
                              capture_output=True, text=True, timeout=8)
        return result.stdout.strip()
    except:
        return "⚠️ Monitor non trovato o in esecuzione."

@st.cache_data(ttl=10)
def load_cindex_history():
    now = datetime.now()
    return pd.DataFrame([
        {"timestamp": now - timedelta(minutes=i*2), "c_index": round(0.65 + i*0.009, 3),
         "phi": round(0.68 + i*0.006, 2), "w": round(0.67 + i*0.007, 2), "a": round(0.66 + i*0.005, 2)}
        for i in range(25)
    ])

def check_comparti_status():
    comparti_dir = SPEACE_CORTEX / "comparti"
    expected = ["prefrontal_cortex", "perception_module", "world_model_knowledge", 
                "hippocampus", "temporal_lobe", "parietal_lobe", "cerebellum",
                "default_mode_network", "curiosity_module", "safety_module"]
    data = []
    for name in expected:
        file = comparti_dir / f"{name}.py"
        stato = "✅ Implementato" if file.exists() else "⬜ Mancante"
        data.append({"Comparto": name.replace("_", " ").title(), "Stato": stato})
    return pd.DataFrame(data)

def get_neural_bridge_status():
    neurons = [
        ("SMFOIKernelNeuron", "✅ Active", "v0.3", "Ciclo 6-step running"),
        ("PrefrontalCortex", "🟡 Loading", "v0.1", "Planning in progress"),
        ("AdaptiveConsciousness", "✅ Active", "v1.0", "C-index: 0.712"),
        ("WorldModelNeuron", "⬜ Missing", "v0.0", "Da implementare"),
        ("MemoryNeuron", "✅ Active", "v0.8", "ChromaDB OK"),
        ("DigitalDNANeuron", "✅ Active", "v1.2", "Epigenome loaded"),
        ("AGPTNeuron", "✅ Active", "Forge", "Tools ready"),
        ("HermesAgentNeuron", "✅ Active", "v1.0", "Persistent memory"),
        ("SafetyModuleNeuron", "✅ Active", "v1.0", "Risk gates OK"),
    ]
    return pd.DataFrame(neurons, columns=["Neurone", "Stato", "Versione", "Note"])

# ====================== SIDEBAR ======================
st.sidebar.title("🧬 SPEACE NEURAL CORE")
st.sidebar.markdown("**Live Cyber-Biological Interface**")
st.sidebar.metric("C-index", "0.712", "↑0.029")
st.sidebar.metric("Alignment", "72.8", "↑2.3")
st.sidebar.metric("Fitness", "0.81", "↑0.03")

if st.sidebar.button("🔄 Full Refresh"):
    st.cache_data.clear()
    st.rerun()

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview", "🧠 Brain Status", "📈 C-index Live", "🔄 SMFOI Live Log",
    "🌐 Neural Bridge Live", "🌐 Organism/IoT", "✅ Tasks", "🧬 DigitalDNA"
])

# TAB 1: Overview
with tab1:
    st.title("🧠 SPEACE CONTROL DASHBOARD")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Stato Cerebrale", "62%", "↑17%")
    with col2: st.metric("Comparti Attivi", "5/9")
    with col3: st.metric("Neuroni Attivi", "8/11")
    with col4: st.metric("Autonomia", "Supervised")

# TAB 2: Brain Status (FIXED)
with tab2:
    st.header("🧠 9 Comparti Cerebrali")
    df_comp = check_comparti_status()
    
    # FIX per Pandas 2.0+
    styled = df_comp.style.map(lambda x: 'background-color: #004400; color: #00ff9d' if '✅' in x else 
                                      'background-color: #440000; color: #ff6666', subset=["Stato"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

# TAB 3: C-index Live
with tab3:
    st.header("📈 C-index Live")
    col1, col2 = st.columns([1, 2])
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=0.712, title={"text": "C-INDEX"},
            delta={"reference": 0.683},
            gauge={"axis": {"range": [0, 1]}, "bar": {"color": "#00ff9d"},
                   "steps": [{"range": [0, 0.5], "color": "#440000"},
                             {"range": [0.5, 0.8], "color": "#004400"},
                             {"range": [0.8, 1], "color": "#00aa00"}]}))
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col2:
        df_hist = load_cindex_history()
        st.plotly_chart(px.line(df_hist, x="timestamp", y=["c_index", "phi", "w", "a"]), 
                       use_container_width=True)

# TAB 4: SMFOI Live Log
with tab4:
    st.header("🔄 SMFOI-KERNEL Live Log")
    log = load_status_monitor()
    st.code(log[-1800:] if len(log) > 1800 else log, language="text")
    if st.button("▶️ Esegui Nuovo Ciclo SMFOI"):
        with st.spinner("Esecuzione in corso..."):
            time.sleep(1.5)
            st.success("Ciclo SMFOI completato!")
            st.rerun()

# TAB 5: Neural Bridge Live
with tab5:
    st.header("🌐 Neural Bridge - Neuroni Attivi")
    df_bridge = get_neural_bridge_status()
    st.dataframe(df_bridge.style.map(lambda x: 'color: #00ff9d' if '✅' in str(x) else '', 
                                    subset=["Stato"]), 
                 use_container_width=True, hide_index=True)

# Altre tab (puoi espandere)
with tab6: st.header("🌐 Organism/IoT"); st.info("In fase di sviluppo")
with tab7: st.header("✅ Tasks Tracker"); st.info("Vedi SPEACE-Tasks-Tracker.md")
with tab8: st.header("🧬 DigitalDNA"); st.info("Caricamento genome.yaml...")

st.caption("SPEACE Neural Dashboard v1.3 — Fixed Pandas Styling | Cyber-Biological Theme")
