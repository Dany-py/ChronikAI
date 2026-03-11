chronikai/
├─ README.md
├─ pyproject.toml
├─ .gitignore
├─ .env.example
│
├─ apps/                      # Applications finales (UI, services)
│   ├─ watcher/               # Daemon de capture
│   │   └─ main.py
│   │
│   ├─ studio/                # Interface Streamlit
│   │   └─ app.py
│   │
│   └─ cli/                   # (optionnel) CLI future
│
├─ core/                      # 🧠 CŒUR DU PRODUIT
│   ├─ brain/                 # Intelligence métier
│   │   ├─ sessionizer.py
│   │   ├─ context_engine.py
│   │   ├─ value_detector.py
│   │   └─ prompt_builder.py
│   │
│   ├─ memory/                # Mémoire long terme
│   │   ├─ models.py
│   │   ├─ repository.py
│   │   └─ schemas.py
│   │
│   └─ llm/                   # Abstraction LLM
│       ├─ base.py
│       ├─ ollama.py
│       └─ openai.py
│
├─ infrastructure/            # Techniques transverses
│   ├─ db/
│   │   ├─ sqlite.py
│   │   └─ migrations/
│   │
│   ├─ config/
│   │   └─ settings.py
│   │
│   └─ security/
│       └─ anonymizer.py
│
├─ shared/                    # Utilitaires partagés
│   ├─ logging.py
│   ├─ time_utils.py
│   └─ enums.py
│
├─ tests/
│   ├─ watcher/
│   ├─ brain/
│   └─ studio/
│
└─ docs/
    ├─ architecture.md
    ├─ data_model.md
    └─ roadmap.md
