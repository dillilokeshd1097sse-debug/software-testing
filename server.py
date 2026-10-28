"""
Local HTTP Server for NexBank ATM-X700 Core Terminal
Serves the ATM web application at http://localhost:8000
"""
import os
import sys
import subprocess

def main():
    atm_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "atm_app"))
    port = 8000
    print("=" * 70)
    print("    NexBank ATM-X700 Core Terminal - Local Web Server")
    print("=" * 70)
    print(f"[*] Serving from: {atm_dir}")
    print(f"[*] Access URL:   http://localhost:{port}")
    print(f"[*] Alternate:    http://127.0.0.1:{port}")
    print("-" * 70)
    print("Sample Credentials:")
    print("  - Card 1: 4532109843218765 | PIN: 1234 (Balance: $1,000.00)")
    print("  - Card 2: 5412751234567890 | PIN: 4321 (Balance: $500.00)")
    print("-" * 70)
    print("Press Ctrl+C to stop the server.")
    print("=" * 70)

    cmd = [sys.executable, "-u", "-m", "http.server", str(port), "--directory", atm_dir]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()

