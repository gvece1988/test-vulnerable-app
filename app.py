import bcrypt

@app.route('/hash')
def hash_password():
    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    # Generate salt and hash using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return jsonify({'hash': hashed.decode('utf-8')})

# VULNERABILITY 5: Path Traversal
@app.route('/read-file')
def read_file():
    """Vulnerable to path traversal"""
    filename = request.args.get('filename')
    # VULNERABLE: No path validation
    file_path = os.path.join('files', filename)
    # Validate that the filename does not contain path traversal characters
    if '..' in filename or '\..' in filename or '/..' in filename:
        return jsonify({'error': 'Path traversal attempt detected'}), 400
    try:
        with open(file_path, 'r') as f:
            return jsonify({'content': f.read()})
    except Exception as e:
        return jsonify({'error': str(e)}), 4