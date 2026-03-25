import streamlit as st
import sys
import os

# ── path setup so app.* imports work inside Docker ───────────────────────────
sys.path.insert(0, "/app")

# ── page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    .hero-header {
        text-align: center;
        padding: 2rem 0 1.5rem;
    }
    .hero-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.4rem;
    }

    .chat-user {
        display: flex;
        justify-content: flex-end;
        margin: 0.75rem 0;
    }
    .chat-user .bubble {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        border-radius: 18px 18px 4px 18px;
        padding: 0.8rem 1.2rem;
        max-width: 72%;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }

    .chat-assistant {
        display: flex;
        justify-content: flex-start;
        margin: 0.75rem 0;
    }
    .chat-assistant .avatar {
        width: 2.2rem;
        height: 2.2rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #34d399, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
        margin-right: 0.6rem;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.4);
    }
    .chat-assistant .bubble {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        border-radius: 4px 18px 18px 18px;
        padding: 0.8rem 1.2rem;
        max-width: 72%;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .context-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-top: 0.4rem;
        font-size: 0.82rem;
        color: #94a3b8;
        font-style: italic;
        line-height: 1.5;
    }

    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.05) !important;
        border-top: 1px solid rgba(255,255,255,0.1) !important;
    }
    .stChatInput textarea {
        background: rgba(255,255,255,0.08) !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    .status-badge {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        border: 1px solid rgba(52, 211, 153, 0.4);
        color: #34d399;
        border-radius: 20px;
        padding: 0.2rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        color: #cbd5e1;
        font-size: 0.83rem;
    }
    .metric-card span {
        font-weight: 600;
        color: #a78bfa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── lazy-load the RAG engine (cached across reruns) ───────────────────────────
@st.cache_resource(show_spinner=False)
def load_engine():
    from app.rag.engine import RAGEngine
    return RAGEngine()


# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 RAG Assistant")
    st.markdown('<div class="status-badge">● Online</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### ⚙️ Configuration")
    st.markdown(
        """
        <div class="metric-card">📄 Knowledge base: <span>knowledge.pdf</span></div>
        <div class="metric-card">🔢 Chunk size: <span>500 tokens</span></div>
        <div class="metric-card">🔁 Overlap: <span>50 tokens</span></div>
        <div class="metric-card">🔍 Retrieval top-k: <span>3 chunks</span></div>
        <div class="metric-card">🤖 LLM: <span>llama-3.3-70b</span></div>
        <div class="metric-card">📦 Embeddings: <span>all-MiniLM-L6-v2</span></div>
        <div class="metric-card">🗄️ Vector store: <span>FAISS</span></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    example_qs = [
        "What is this document about?",
        "Summarise the key points",
        "What are the main findings?",
        "Explain the conclusion",
    ]
    for q in example_qs:
        if st.button(q, use_container_width=True, key=f"ex_{q}"):
            st.session_state["prefill"] = q

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["contexts"] = []
        st.rerun()

    st.markdown(
        "<div style='color:#475569;font-size:0.75rem;margin-top:1rem;text-align:center;'>"
        "Powered by LangChain · FAISS · Groq</div>",
        unsafe_allow_html=True,
    )


# ── main area ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-header">
        <h1>🧠 Knowledge Assistant</h1>
        <p>Ask anything about your PDF — answers are grounded in your document.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# session state init
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "contexts" not in st.session_state:
    st.session_state["contexts"] = []
if "engine_loaded" not in st.session_state:
    st.session_state["engine_loaded"] = False

# load engine
if not st.session_state["engine_loaded"]:
    with st.spinner("⚙️  Loading knowledge base… this may take a moment on first run."):
        engine = load_engine()
    st.session_state["engine_loaded"] = True
else:
    engine = load_engine()

# ── render conversation history ───────────────────────────────────────────────
for i, msg in enumerate(st.session_state["messages"]):
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><div class="bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        ctx_chunks = st.session_state["contexts"][i // 2] if i // 2 < len(st.session_state["contexts"]) else []
        st.markdown(
            f'<div class="chat-assistant">'
            f'<div class="avatar">🤖</div>'
            f'<div class="bubble">{msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if ctx_chunks:
            with st.expander("📄 Retrieved context chunks", expanded=False):
                for j, chunk in enumerate(ctx_chunks):
                    st.markdown(
                        f'<div class="context-box"><b>Chunk {j+1}:</b><br>{chunk}</div>',
                        unsafe_allow_html=True,
                    )

# ── handle prefilled question from sidebar buttons ────────────────────────────
prefill = st.session_state.pop("prefill", None)

# ── chat input ────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask a question about your document…") or prefill

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.markdown(
        f'<div class="chat-user"><div class="bubble">{prompt}</div></div>',
        unsafe_allow_html=True,
    )

    with st.spinner("🔍 Searching knowledge base and generating answer…"):
        try:
            contexts = engine.vector_store.search(prompt, k=3)
            answer = engine.generate_answer(prompt)
        except Exception as e:
            contexts = []
            answer = f"⚠️ Error: {e}"

    st.session_state["contexts"].append(contexts)
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    st.markdown(
        f'<div class="chat-assistant">'
        f'<div class="avatar">🤖</div>'
        f'<div class="bubble">{answer}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if contexts:
        with st.expander("📄 Retrieved context chunks", expanded=False):
            for j, chunk in enumerate(contexts):
                st.markdown(
                    f'<div class="context-box"><b>Chunk {j+1}:</b><br>{chunk}</div>',
                    unsafe_allow_html=True,
                )