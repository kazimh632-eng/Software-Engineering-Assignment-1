from flask import Flask, jsonify, request, g
from secrets import token_urlsafe
from functools import wraps

app = Flask(__name__)
# Demo-only accounts. Change these before sharing; never reuse real passwords.
USERS = {'employee': {'password': 'employee123', 'role': 'employee'},
         'admin': {'password': 'admin123', 'role': 'administrator'}}
TOKENS = {}
EMPLOYEES = {1: {'id': 1, 'name': 'Amina Khan', 'department': 'IT', 'email': 'amina@example.com'}}
NEXT_ID = 2

@app.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    user = USERS.get(data.get('username'))
    if not user or data.get('password') != user['password']:
        return jsonify(error='Invalid username or password'), 401
    token = token_urlsafe(32)
    TOKENS[token] = {'username': data['username'], 'role': user['role']}
    return jsonify(token=token, role=user['role'], message='Login successful')

def require_auth(admin=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').removeprefix('Bearer ').strip()
            identity = TOKENS.get(token)
            if not identity: return jsonify(error='Authentication required; use Bearer token'), 401
            if admin and identity['role'] != 'administrator': return jsonify(error='Administrator role required'), 403
            g.identity = identity
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.get('/employees')
@require_auth()
def list_employees(): return jsonify(list(EMPLOYEES.values()))

@app.post('/employees')
@require_auth(admin=True)
def add_employee():
    global NEXT_ID
    data=request.get_json(silent=True) or {}
    if not all(str(data.get(k,'')).strip() for k in ('name','department','email')):
        return jsonify(error='Required fields: name, department, email'), 400
    item={'id':NEXT_ID,'name':data['name'],'department':data['department'],'email':data['email']}
    EMPLOYEES[NEXT_ID]=item; NEXT_ID+=1
    return jsonify(item), 201

@app.put('/employees/<int:employee_id>')
@require_auth(admin=True)
def update_employee(employee_id):
    item=EMPLOYEES.get(employee_id)
    if not item: return jsonify(error='Employee not found'),404
    data=request.get_json(silent=True) or {}
    for key in ('name','department','email'):
        if key in data: item[key]=data[key]
    return jsonify(item)

@app.delete('/employees/<int:employee_id>')
@require_auth(admin=True)
def delete_employee(employee_id):
    if EMPLOYEES.pop(employee_id,None) is None: return jsonify(error='Employee not found'),404
    return jsonify(message='Employee deleted')

if __name__ == '__main__': app.run(debug=True, port=5003)
