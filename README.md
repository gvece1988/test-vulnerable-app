# Test Vulnerable Application

This is a deliberately vulnerable Flask application for testing the vulnerability remediation system.

## Vulnerabilities

### Code Vulnerabilities

1. **SQL Injection** (Critical) - Line 20
   - Direct string concatenation in SQL query
   - File: `app.py`, route: `/user/<username>`

2. **Hardcoded Credentials** (Critical) - Line 32
   - API key and password hardcoded in source
   - File: `app.py`, route: `/admin/login`

3. **Insecure Deserialization** (Critical) - Line 44
   - Unsafe pickle deserialization
   - File: `app.py`, route: `/load-data`

4. **Command Injection** (Critical) - Line 54
   - Direct system call with user input
   - File: `app.py`, route: `/ping`

5. **Path Traversal** (High) - Line 66
   - No path validation
   - File: `app.py`, route: `/read-file`

6. **Weak Cryptographic Hash** (Medium) - Line 77
   - Using MD5 for password hashing
   - File: `app.py`, route: `/hash`

### Dependency Vulnerabilities

1. **Flask 1.1.4** - Known vulnerabilities
2. **Werkzeug 1.0.1** - Known vulnerabilities
3. **Requests 2.6.0** - Known vulnerabilities
4. **Urllib3 1.25.0** - Known vulnerabilities

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Testing

```bash
# Test SQL injection
curl "http://localhost:5000/user/' OR '1'='1"

# Test hardcoded credentials
curl "http://localhost:5000/admin/login?password=admin123"

# Test command injection
curl "http://localhost:5000/ping?host=8.8.8.8; whoami"

# Test path traversal
curl "http://localhost:5000/read-file?filename=../../etc/passwd"
```

## Purpose

This application is intentionally vulnerable for:
- Testing security scanners
- Demonstrating vulnerability remediation
- Educational purposes only

**DO NOT deploy to production.**
