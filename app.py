from flask import Flask, jsonify, request
from secrets import token_urlsafe
import os

app = Flask(__name__)
# Classroom demo only: keys are generated at startup, held in memory and printed locally.
# Never commit or publicly share these values.
keys = {token_urlsafe(32): f'consumer-{i}' for i in range(1, 4)}
print('PRIVATE TEST KEYS (share securely with assigned testers; do not publish):')
for key, consumer in keys.items(): print(f'{consumer}: {key}')

@app.post('/process')
def process_text():
    key = request.headers.get('X-API-Key', '')
    if key not in keys:
        return jsonify(error='Invalid or missing API key'), 401
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if not isinstance(text, str): return jsonify(error="JSON field 'text' must be a string"), 400
    return jsonify(consumer=keys[key], processed_text=text.upper())

if __name__ == '__main__': app.run(debug=True, port=5002)
