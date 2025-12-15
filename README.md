# Adaptive AI Second-Brain

An intelligent system designed to convert raw, unstructured thoughts into structured, actionable data. It uses LLMs to understand context, importance, and urgency, and Vector Search to enable semantic retrieval and "second brain" capabilities.

## 🚀 Features

- **Thought Structuring**: Converts messy text ("Buy milk and call John") into structured JSON objects (Tasks, Ideas, Goals, etc.).
- **Semantic Analysis**: Automatically assigns categories, urgency, importance, energy levels, and context tags.
- **Vector Memory**: Stores thoughts in a Vector Database (Qdrant) for semantic search and retrieval.
- **CLI Interface**: Simple command-line tools to capture and find information.

## 🛠️ Setup

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arslanaka/second-brain.git
   cd second-brain
   ```

2. **Set up Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and set your OPENAI_API_KEY
   ```

4. **Start Infrastructure (Vector DB)**
   ```bash
   docker-compose up -d
   ```

## 📖 Usage

### Capture a Thought
Capture, structure, and store a new thought.
```bash
python -m src.cli capture "I need to plan a trip to Japan next April"
```

### Search Thoughts
Semantically search your database (e.g., finding "travel plans" will return the "Japan trip" note).
```bash
python -m src.cli search "travel plans"
```

---

## 🗺️ Project Stages

### ✅ Stage 1: Input Capture & Structuring (MVP)
**Goal:** Convert raw inputs into structured objects.
- [x] Pydantic Data Models (Tasks, Ideas, etc.)
- [x] OpenAI Integration for text parsing
- [x] Basic CLI for capturing thoughts

### ✅ Stage 2: Semantic Categorization & Priority
**Goal:** advanced classification and memory.
- [x] Dockerized Qdrant Vector DB setup
- [x] Enhanced Data Models (Importance, Energy, Context)
- [x] Semantic Embeddings (OpenAI models)
- [x] Semantic Search functionality

### ⏳ Stage 3: Intelligent Scheduling & Workflow Generation
**Goal:** Convert items into a dynamic calendar plan.
- [ ] Auto-schedule tasks based on priority/energy
- [ ] Identify conflicts and suggest time slots
- [ ] Adapt plans autonomously

### ⏳ Stage 4: Active Reminders, Nudges & Daily Briefings
**Goal:** Proactive assistance.
- [ ] Morning briefings and evening summaries
- [ ] Context-aware nudges ("You have 20 mins free...")
- [ ] Integration with External Calendars (Google, Notion)

### ⏳ Stage 5: Continuous Learning & Personal Adaptation
**Goal:** The system learns your habits.
- [ ] Learn preferred working hours and energy patterns
- [ ] Predict needs based on history
- [ ] Personalized planning style adaptation
