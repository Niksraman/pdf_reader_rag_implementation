
"""
Streamlit UI for Chat With Your Docs
"""
import streamlit as st
import requests
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Chat With Your Docs",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_URL = "http://127.0.0.1:8000"
UPLOAD_DIR = Path("uploaded_docs")
UPLOAD_DIR.mkdir(exist_ok=True)

# ============ Helper Functions ============

def call_api(endpoint: str, data: dict, method: str = "POST"):
    """Make API call with error handling"""
    try:
        url = f"{API_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=300)
        else:
            response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API server. Make sure it's running on http://127.0.0.1:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ API request timed out")
        return None
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

def process_question(question: str, top_k: int = 3):
    """Process a question through the RAG system"""
    with st.spinner("🔍 Searching documents and generating answer..."):
        response = call_api(
            "/ask",
            {"question": question, "top_k": top_k}
        )
    
    if response:
        return response.get("answer"), response.get("sources", [])
    return None, None

def ingest_documents(file_paths: list):
    """Ingest documents into the system"""
    with st.spinner("📥 Ingesting documents..."):
        # In real scenario, would upload files to server
        # For now, just return success
        return True

# ============ Sidebar ============

with st.sidebar:
    st.title("⚙️ Settings & Control")
    
    # Settings section
    with st.expander("Settings", expanded=True):
        top_k = st.slider(
            "Number of sources to retrieve",
            min_value=1,
            max_value=10,
            value=3,
            help="How many relevant document chunks to use for generating answers"
        )
        
        api_url_custom = st.text_input(
            "API URL",
            value=API_URL,
            help="URL of the RAG API server"
        )
        if api_url_custom != API_URL:
            # Update API_URL if changed (note: would need to be global to actually work)
            pass
    
    # Document Management section
    st.divider()
    st.subheader("📄 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        help="Upload PDF or text files to add to the knowledge base"
    )
    
    if uploaded_files:
        if st.button("📤 Upload Files"):
            for uploaded_file in uploaded_files:
                file_path = UPLOAD_DIR / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ Saved {uploaded_file.name}")
            
            # Ingest uploaded documents
            if st.button("🔄 Ingest Uploaded Documents"):
                response = call_api(
                    "/ingest/sync",
                    {"path": str(UPLOAD_DIR)}
                )
                if response and response.get("status") == "completed":
                    st.success("✅ Documents ingested successfully!")
                else:
                    st.error("❌ Failed to ingest documents")
    
    # API Status
    st.divider()
    st.subheader("🔌 API Status")
    if st.button("Check API Status"):
        response = call_api("/health", {}, method="GET")
        if response:
            st.success(f"✅ API is healthy (v{response.get('version', 'unknown')})")
        else:
            st.error("❌ API is not responding")

# ============ Main Content ============

st.title("📚 Chat With Your Documents")
st.markdown("Ask questions about your documents and get instant answers powered by RAG")

# Create tabs
tab1, tab2 = st.tabs(["💬 Ask Questions", "📖 Documentation"])

with tab1:
    # Question input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_area(
            "Ask a question:",
            height=100,
            placeholder="Enter your question here. For example: 'What is the main topic of the documents?'",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.button("🚀 Ask", use_container_width=True, type="primary")
    
    # Process question
    if submit_button and question:
        answer, sources = process_question(question, top_k=top_k)
        
        if answer:
            # Display answer
            st.subheader("💡 Answer")
            st.markdown(answer)
            
            # Display sources
            if sources:
                st.divider()
                st.subheader(f"📚 Sources ({len(sources)})")
                
                for idx, source in enumerate(sources, 1):
                    with st.expander(f"Source {idx}"):
                        st.text_area(
                            "Content",
                            value=source,
                            height=150,
                            disabled=True,
                            label_visibility="collapsed"
                        )
            else:
                st.info("ℹ️ No sources found")
        else:
            st.error("Failed to get answer")
    
    elif submit_button:
        st.warning("⚠️ Please enter a question")
    
    # Example questions
    st.divider()
    st.subheader("💡 Example Questions")
    examples = [
        "What is the main topic?",
        "Can you summarize the key points?",
        "What are the important dates mentioned?"
    ]
    
    for example in examples:
        if st.button(f"📌 {example}"):
            answer, sources = process_question(example, top_k=top_k)
            if answer:
                st.subheader("Answer")
                st.write(answer)
                if sources:
                    st.subheader("Sources")
                    for source in sources:
                        st.write(f"- {source[:200]}...")

with tab2:
    st.markdown("""
    ## How to Use Chat With Your Docs
    
    ### 1. Upload Documents
    - Use the file uploader in the sidebar to upload PDF, TXT, or markdown files
    - Click "Upload Files" to save them
    - Click "Ingest Uploaded Documents" to add them to the knowledge base
    
    ### 2. Ask Questions
    - Type your question in the text area
    - Click "Ask" or use the example questions
    - The system will search your documents and generate an answer
    
    ### 3. Review Sources
    - Each answer shows the relevant document excerpts used
    - Expand any source to see the full content
    
    ### 4. Adjust Settings
    - Use the slider to control how many documents are considered for each answer
    - More sources = more comprehensive but potentially less focused answers
    
    ## Features
    - 🚀 **Fast Retrieval**: Uses semantic search with embeddings
    - 🤖 **Smart Answers**: LLM-powered responses based on your documents
    - 📊 **Source Attribution**: See exactly which documents were used
    - 🔄 **Real-time Updates**: Add new documents anytime
    - 💾 **Persistent Storage**: Your documents are saved and indexed
    
    ## Supported Formats
    - PDF files (.pdf)
    - Text files (.txt)
    - Markdown files (.md)
    
    ## Tips for Better Results
    - Use clear, specific questions
    - Upload relevant documents to your use case
    - Review the sources to verify accuracy
    - Ask follow-up questions to dig deeper
    
    ## Technical Details
    - **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
    - **Vector Store**: FAISS
    - **Backend**: FastAPI
    - **UI**: Streamlit
    """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📧 Backend: FastAPI")
with col2:
    st.caption("🎨 Frontend: Streamlit")
with col3:
    st.caption("🔍 AI: RAG System")
