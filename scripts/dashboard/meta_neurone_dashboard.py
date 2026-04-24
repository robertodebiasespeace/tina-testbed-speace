"""
SPEACE Meta-Neurone Dialogic - Chat Dashboard
Interfaccia dedicata al dialogo con Gemma3:12b via Ollama
Port: 8502
"""

import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="SPEACE - Meta-Neurone Dialogic",
    page_icon="🧠",
    layout="wide"
)

# ====================== TEMA ======================
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #00ff9d; }
    .stButton>button { background-color: #00cc77; color: black; border: 1px solid #00ff9d; }
    .stTextInput>div>div>input { background-color: #111111; color: #00ff9d; border: 1px solid #00ff9d; }
    .stTextArea>div>div>textarea { background-color: #111111; color: #00ff9d; border: 1px solid #00ff9d; }
    h1, h2, h3 { color: #00ff9d; }
    .chat-message { padding: 12px; border-radius: 8px; margin: 6px 0; }
    .user-msg { background-color: #1a1a2e; border-left: 3px solid #00ff9d; }
    .assistant-msg { background-color: #0d1f1a; border-left: 3px solid #00cc77; }
    ::selection { background-color: #00ff9d; color: black; }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.title("🧠 SPEACE - Meta-Neurone Dialogic")
st.caption(f"Gemma3:12b · Ollama · Apprendimento Online · {datetime.now().strftime('%H:%M:%S')}")

# ====================== SESSION STATE ======================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "bridge_initialized" not in st.session_state:
    st.session_state.bridge_initialized = False

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("⚙️ Configurazione")

    st.subheader("🔗 Connessioni")
    try:
        from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge

        if not st.session_state.bridge_initialized:
            bridge = SPEACENeuralBridge()
            bridge.initialize_full_cortex()
            st.session_state.bridge_initialized = True
            st.session_state.bridge = bridge
    except Exception as e:
        st.error(f"Bridge error: {e}")

    if st.session_state.get("bridge"):
        bridge = st.session_state.bridge
        c_idx = bridge.get_c_index()
        st.metric("C-index", f"{c_idx:.3f}")
        st.metric("Comparti", len(bridge.compartments))

        lc = bridge.learning_core
        st.metric("Learning Core", "✅ Attivo" if lc else "⚠️ Spento")
        if lc:
            metrics = lc.get_metrics()
            st.caption(f"Avg Fitness: {metrics.get('avg_fitness', 0):.3f}")
            st.caption(f"Cicli appresi: {metrics.get('cycles_learned', 0)}")

    st.markdown("---")
    st.subheader("🤖 Modello")

    try:
        import ollama
        models = ollama.list()
        model_names = [m['name'] for m in models.get('models', [])]
        if model_names:
            st.success(f"Ollama attivo - {len(model_names)} modelli")
            st.selectbox("Modello", model_names, index=model_names.index("gemma3:12b") if "gemma3:12b" in model_names else 0, key="selected_model")
        else:
            st.warning("Nessun modello caricato")
    except ImportError:
        st.error(" Libreria ollama non installata")
        st.code("pip install ollama")
    except Exception as e:
        st.warning(f"Ollama non raggiungibile: {e}")

    st.markdown("---")
    if st.button("🗑️ Pulisci Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("📊 Status Completo", use_container_width=True):
        if st.session_state.get("agent"):
            st.json(st.session_state.agent.get_status())

# ====================== MAIN CHAT AREA ======================

# Status bar
col_status = st.columns(3)
with col_status[0]:
    model_name = st.session_state.get("selected_model", "gemma3:12b")
    st.metric("Modello", model_name)
with col_status[1]:
    st.metric("Ollama", "✅ Attivo" if "ollama" in sys.modules else "⏸️ Spento")
with col_status[2]:
    lc_connected = st.session_state.get("bridge") and st.session_state.get("bridge").learning_core is not None
    st.metric("Learning Core", "✅ Collegato" if lc_connected else "⏸️ Disconnesso")

st.markdown("---")

# Chat container
st.subheader("💬 Conversazione")
chat_container = st.container(height=450)

with chat_container:
    if not st.session_state.chat_history:
        st.info("Nessun messaggio ancora. Scrivi la tua domanda per iniziare il dialogo con SPEACE.")
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-msg">
                <strong style="color:#00ff9d">Tu:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-msg">
                <strong style="color:#00cc77">🧠 SPEACE:</strong><br>
                {msg['content']}
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")

# Input form
with st.form("chat_form", clear_on_submit=True):
    col_input = st.columns([4, 1])
    with col_input[0]:
        user_query = st.text_area(
            "La tua domanda a SPEACE:",
            placeholder="Es: Qual è il tuo stato attuale? Cosa dovremmo migliorare oggi?",
            height=80,
            label_visibility="collapsed"
        )
    with col_input[1]:
        st.write("")  # spacing
        send = st.form_submit_button("🧠 Invia", type="primary", use_container_width=True)

    if send and user_query.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.spinner("Meta-Neurone sta ragionando con Gemma3:12b..."):
            try:
                from SPEACE_Cortex.comparti.self_dialogue_agent import SelfDialogueAgent

                if not st.session_state.get("bridge"):
                    from SPEACE_Cortex.neural_bridge import SPEACENeuralBridge
                    bridge = SPEACENeuralBridge()
                    bridge.initialize_full_cortex()
                    st.session_state.bridge = bridge
                    st.session_state.bridge_initialized = True

                agent = SelfDialogueAgent()
                agent.set_bridge(st.session_state.bridge)
                st.session_state.agent = agent

                result = asyncio.run(agent.process({"query": user_query}))

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result["response"]
                })

                with st.expander("📋 Dettagli risposta"):
                    st.write(f"**Suggerimento:** {result.get('suggestion', 'N/A')}")
                    st.write(f"**Confidence:** {result.get('confidence', 0):.2f}")
                    st.write(f"**Model:** {result.get('model', 'N/A')}")
                    st.write(f"**Learning Core:** {'✅ Collegato' if result.get('learning_core_connected') else '⚠️ Non collegato'}")

            except Exception as e:
                st.error(f"Errore durante il dialogo: {str(e)}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Errore: {str(e)}"
                })

        st.rerun()

# ====================== FOOTER ======================
st.markdown("---")
st.caption("SPEACE Meta-Neurone Dialogic v2.0 · Powered by Gemma3:12b + Ollama · Architettura SPEACE completa")