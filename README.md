# Task 3 — Authentication and authorization

Demo accounts (change before any sharing): employee / `employee123`; admin / `admin123`. Install Flask and run `python app.py` (port 5003). Login:

```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d '{"username":"employee","password":"employee123"}'
```

Copy the returned token and use `-H "Authorization: Bearer TOKEN"` for `GET /employees`. Employee token gets 403 for POST/PUT/DELETE; admin token can do CRUD. `POST /employees` JSON example: `{"name":"Sara Ali","department":"HR","email":"sara@example.com"}`. Invalid login or missing token returns 401. This is a small classroom demo using in-memory tokens/data and plain demo passwords; not production authentication.
