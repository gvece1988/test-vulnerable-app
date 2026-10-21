#!/usr/bin/env python3
"""
Vulnerable Application for Testing Security Fixes
This app contains real security vulnerabilities that can be detected and fixed
"""
import sqlite3
import pickle
import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# VULNERABILITY 1: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    """Vulnerable to SQL injection - no parameterized queries"""
    conn = get_db_connection()
    # VULNERABLE: Direct string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user = conn.execute(query).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

# VULNERABILITY 2: Hardcoded Credentials
@app.route('/admin/login')
def admin_login():
    """Vulnerable: Hardcoded API key and password"""
    # VULNERABLE: Hardcoded credentials
    API_KEY = "sk-1234567890abcdef"
    ADMIN_PASSWORD = "admin123"

    password = request.args.get('password')
    if password == ADMIN_PASSWORD:
        return jsonify({"status": "success", "api_key": API_KEY})
    return jsonify({"error": "Invalid password"}), 401

# VULNERABILITY 3: Insecure Deserialization
@app.route('/load-data')
def load_data():
    """Vulnerable: Unsafe pickle deserialization"""
    data = request.args.get('data')
    # VULNERABLE: Unsafe deserialization with pickle
    try:
        obj = pickle.loads(data.encode('latin1'))
        return jsonify({"status": "loaded", "data": str(obj)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# VULNERABILITY 4: Command Injection
@app.route('/ping')
def ping_host():
    """Vulnerable to command injection"""
    host = request.args.get('host')
    # VULNERABLE: Direct system call with user input
    command = f"ping -c 4 {host}"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# VULNERABILITY 5: Path Traversal
@app.route('/read-file')
def read_file():
    """Vulnerable to path traversal"""
    filename = request.args.get('filename')
    # VULNERABLE: No path validation
    file_path = os.path.join('files', filename)
    try:
        with open(file_path, 'r') as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# VULNERABILITY 6: Weak Cryptographic Hash
import hashlib

@app.route('/hash')
def hash_password():
    """Vulnerable: Using MD5 for password hashing"""
    password = request.args.get('password')
    # VULNERABLE: MD5 is cryptographically weak
    hashed = hashlib.md5(password.encode()).hexdigest()
    return jsonify({"hash": hashed})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
