# Task 1 — Student API + Streamlit

Run in separate VS Code terminals from this folder:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate   | macOS/Linux: source .venv/bin/activate
pip install flask streamlit requests
python app.py
```

Second terminal, activate the same environment and run `streamlit run streamlit_app.py`. Open the URL Streamlit prints. API runs on port 5001; SQLite creates `students.db` automatically. Endpoints: GET/POST `/students`, GET/PUT/DELETE `/students/<id>`.
