# Task 2 — API key protected text processor

Install Flask (`pip install flask`) and run `python app.py`. At startup, three random keys appear in the local terminal. Treat them as secrets: send each tester only their key privately; do not put keys in GitHub, video, screenshots or this repository. Restarting the server creates new keys. For a tester:

```bash
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: PASTE_KEY_HERE" -d '{"text":"hello api"}'
```

Invalid/missing key should return HTTP 401. Avoid sharing the terminal showing real keys in a public demo; show a masked key or separate private testing. For classroom use only, keys live in memory and are not suitable for production.
