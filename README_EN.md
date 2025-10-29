# 🛡️ SUBOTAI - AI Response Verification System

Intelligent verification system that compares direct LLM responses with verified responses using an internal knowledge base.

**🇬🇧 English Version** | **[🇪🇸 Versión en Español](README.md)**

---

## 💼 Why SUBOTAI?

Once implemented in a business environment, SUBOTAI becomes a strategic tool that:

- **Minimizes operational errors**: By validating responses against documented internal procedures
- **Standardizes processes**: Ensures staff consult and follow established protocols
- **Optimizes workflow**: Resolves team doubts instantly with verified information
- **Enables continuous improvement**: Analyzes query patterns to identify optimization and training areas

The system evolves with your organization: every staff question becomes valuable data to improve productivity and detect training needs.

---

## 🎯 What does SUBOTAI do?

SUBOTAI acts as an **intelligent system** that combines:
- **Your private knowledge base** (reference documents)
- **External LLM responses** (OpenAI, DeepSeek)

The result is a verified response with **color-coded indicators**:
- **Black**: Information from your knowledge base
- **🔵 Blue**: LLM information that doesn't contradict your base
- **🔴 Red**: Information that contradicts your base or has no equivalent for comparison

---

## ✨ Key Features

### 📊 Comparative Interface
- **Left Chat**: Direct LLM response without filters
- **Right Chat**: Verified response with confidence indicators
- Side-by-side visualization to compare responses

### 📁 Document System
- **Server documents**: Predefined knowledge base
- **User document upload**: Upload your own `.txt` and `.md` files
- Temporary storage in browser (localStorage)
- **🧪 Testing**: Includes documents with false data to verify contradiction detection

### 🌍 Multilingual Support
- Select the language of your internal documents (20 languages available)
- System mentally translates for correct processing
- **⚠️ Note**: Effectiveness depends on the LLM's translation capabilities. ChatGPT has much better multilingual performance than DeepSeek. It's recommended to use the 2-3 most common languages (English, Spanish, French, Chinese (I couldn´t check)) for best results.

### 🔌 Multi-Provider
- **OpenAI** (GPT-3.5, GPT-4)
- **DeepSeek** (DeepSeek-Chat)
- Easy switching between providers

---

## 🚀 Quick Installation

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Modern browser** with localStorage support (Chrome, Firefox, Edge, Safari)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/SUBOTAI.git
cd SUBOTAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python main.py
```

### 4. Open in browser
```
http://localhost:8000/app
```

---

## 📖 Usage

### Step 1: Connect your API Key
1. Select your provider (OpenAI or DeepSeek)
2. Enter your API Key
3. Click **"Connect"**
4. Wait for validation (button will turn green)

### Step 2: (Optional) Configure document language
1. Click the 🇪🇸 flag next to "Internal DB"
2. Select the language of your internal documents
3. **Recommendation**: Use OpenAI for documents in languages other than English/Spanish, as DeepSeek has limited translation capabilities

### Step 3: (Optional) Upload your documents
1. Click **"📖 Internal DB"**
2. Select `.txt` or `.md` files
3. Click **"✅ Load documents"**
4. Documents will be saved temporarily in your browser

### Step 4: Ask questions
1. Type your question in the lower input
2. Press **Enter** or click **"Send"**
3. Observe both responses:
   - **Left**: Raw LLM response
   - **Right**: Verified response with colors

---

## 🎨 Color System

The verified response uses colors to indicate verification level:

| Color | Meaning | Example |
|-------|---------|---------|
| **Black** | Information from your knowledge base | *"The speed of light is 299,792 km/s according to your ciencia.txt document"* |
| **🔵 Blue** | LLM information that doesn't contradict your base | *"This means light can circle the Earth 7.5 times in one second"* |
| **🔴 Red** | Information that contradicts your base or has no equivalent for comparison | *"The speed of light varies depending on the medium"* |

---

## 📁 Document Structure

### Server Documents
Predefined documents are stored in:
```
SUBOTAI/src/rag/documents/
├── ciencia.txt       # Verified scientific facts
└── [your files]      # Add more files here
```

**🧪 Testing Note**: The database intentionally includes two documents with completely false data. This allows quick and obvious verification of how the system detects and marks contradictory information with red color.

### User Documents
- Loaded from the web interface
- Saved in browser's `localStorage`
- **⚠️ Temporary**: deleted when closing the browser

**💡 Design Decision**: Temporary storage was chosen for three fundamental reasons:
1. **Easy testing**: Any user can try the system without setting up accounts or external services
2. **Total privacy**: Documents never leave the user's browser, guaranteeing absolute confidentiality
3. **Operational simplicity**: Doesn't require database management, authentication, or storage infrastructure

---

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file:
```bash
# Server port (default: 8000)
PORT=8000

# Logging level
LOG_LEVEL=INFO
```

### Add Server Documents
Simply copy your `.txt` files to:
```bash
SUBOTAI/src/rag/documents/your_document.txt
```

The system will load them automatically on startup.

---

## 🌐 REST API

### Main Endpoints

#### `/api/query` - Verified Response
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Provider: openai" \
  -H "X-Documents-Language: en" \
  -d '{
    "query": "What is the speed of light?",
    "user_documents": []
  }'
```

**Response:**
```json
{
  "response": "The speed of light is 299,792 km/s...",
  "metadata": {
    "rag_used": true,
    "mode": "rag"
  }
}
```

#### `/api/query-raw` - Direct Response
```bash
curl -X POST http://localhost:8000/api/query-raw \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Provider: openai" \
  -d '{
    "query": "What is the speed of light?"
  }'
```

#### `/api/validate-key` - Validate API Key
```bash
curl -X POST http://localhost:8000/api/validate-key \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sk-...",
    "provider": "openai"
  }'
```

**Response:**
```json
{
  "valid": true
}
```

---

## 📊 Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Frontend (HTML) │
│  - Dual chat     │
│  - Doc upload    │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  FastAPI Routes  │
│  /query          │
│  /query-raw      │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  SUBOTAI Core    │
│  - RAG           │
│  - Judge AI      │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  Knowledge Base  │
│  - Server docs   │
│  - User docs     │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  LLM Client      │
│  OpenAI/DeepSeek │
└──────────────────┘
```

---

## 📂 Project Structure

```
SUBOTAI/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Spanish version
├── README_EN.md              # This file (English)
│
├── static/
│   └── index.html            # Complete web interface
│
├── src/
│   ├── api/
│   │   ├── app.py            # FastAPI application
│   │   ├── routes.py         # REST endpoints
│   │   ├── auth_routes.py    # API key validation
│   │   └── models.py         # Pydantic models
│   │
│   ├── auth/
│   │   └── api_key_manager.py # API key management
│   │
│   ├── core/
│   │   ├── config.py         # Configuration
│   │   └── subotai_core.py   # Main orchestrator
│   │
│   ├── llm/
│   │   └── llm_client.py     # Unified LLM client
│   │
│   ├── logic/
│   │   └── reasoning_engine.py # Reasoning engine
│   │
│   └── rag/
│       ├── knowledge_base.py     # Document manager
│       ├── rag_orchestrator.py   # Judge AI
│       └── documents/            # Knowledge base
│           └── ciencia.txt
│
└── tests/
    ├── test_api.py           # API tests
    └── test_integration.py   # Integration tests
```

---

## 🔒 Security

### API Keys
- API keys are stored only in browser's `localStorage`
- Never saved on the server
- Sent in `Authorization: Bearer {key}` headers

### Documents
- **Server**: Permanent, accessible to everyone
- **User**: Temporary, only in user's browser

### CORS
By default, the server accepts requests from any origin. For production, configure CORS in `src/api/app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # ← Change this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🛠️ Troubleshooting

### ❌ "Invalid API Key"
**Cause**: API key is invalid or has no credits  
**Solution**: Verify your API key in the provider's panel

### ❌ "Modal not found"
**Cause**: JavaScript didn't load correctly  
**Solution**: Open F12 → Console and look for errors, then reload (F5)

### ❌ Documents won't load
**Cause**: localStorage full or disabled  
**Solution**: Clear browser cache or enable localStorage

### ❌ Responses without colors
**Cause**: No documents in knowledge base  
**Solution**: Add `.txt` files to `src/rag/documents/` or upload from interface

### ❌ Server connection error
**Cause**: Server is not running  
**Solution**: 
```bash
cd SUBOTAI
python main.py
```

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific tests:
```bash
# API tests
pytest tests/test_api.py -v

# Integration tests
pytest tests/test_integration.py -v
```

Coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 📦 Main Dependencies

| Package | Version | Usage |
|---------|---------|-------|
| `fastapi` | 0.104.1 | Web framework |
| `uvicorn` | 0.24.0 | ASGI server |
| `httpx` | ≥0.25.0 | Async HTTP client |
| `pydantic` | 2.5.0 | Data validation |
| `python-dotenv` | 1.0.0 | Environment variables |
| `pytest` | ≥7.4.0 | Testing framework |
| `aiofiles` | ≥23.0.0 | Async file operations |

See `requirements.txt` for complete list.

---

## 🤝 Contributing

1. Fork the project
2. Create a branch: `git checkout -b feature/new-feature`
3. Commit: `git commit -am 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Open a Pull Request

---

## 📄 License

This project is under the MIT License. See `LICENSE` file for more details.

---

## 🔮 Roadmap

### In Development
- [ ] Document persistence with Supabase
- [ ] Vector embeddings for semantic search
- [ ] Support for more providers (Anthropic Claude, Gemini)
- [ ] Conversation history

### Future
- [ ] Multi-agent mode with debate
- [ ] Export conversations to PDF/Markdown
- [ ] Metrics and analytics dashboard
- [ ] Browser plugin

---

## 💬 Support

Questions or issues?

- **Issues**: [GitHub Issues](https://github.com/your-username/SUBOTAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/SUBOTAI/discussions)

---

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- OpenAI and DeepSeek for their APIs
- The open source community

---

**Built with ❤️ to verify information with confidence**

