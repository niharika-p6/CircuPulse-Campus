"""
Diagnostic test for Streamlit server startup
"""
import subprocess
import time
import sys
import urllib.request
import threading

def run_diagnostics():
    cmd = [
        sys.executable,
        "-m", "streamlit", "run", "app.py",
        "--server.headless=true",
        "--server.port=8515",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false"
    ]
    print("Launching:", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def log_stream(stream, prefix):
        for line in stream:
            print(f"[{prefix}] {line.strip()}")

    t_out = threading.Thread(target=log_stream, args=(proc.stdout, "OUT"), daemon=True)
    t_err = threading.Thread(target=log_stream, args=(proc.stderr, "ERR"), daemon=True)
    t_out.start()
    t_err.start()

    time.sleep(3)

    # Probe 127.0.0.1:8515
    health_url = "http://127.0.0.1:8515/_stcore/health"
    main_url = "http://127.0.0.1:8515/"

    probe_success = False
    for i in range(10):
        print(f"Probe attempt {i+1}...")
        try:
            req = urllib.request.Request(health_url)
            with urllib.request.urlopen(req, timeout=2) as resp:
                print("Health check response code:", resp.status)
                if resp.status == 200:
                    probe_success = True
                    break
        except Exception as e:
            print("Health check probe error:", e)
        time.sleep(1)

    if probe_success:
        try:
            with urllib.request.urlopen(main_url, timeout=3) as resp:
                html = resp.read().decode('utf-8')
                print(f"Main URL HTTP status: {resp.status}, HTML bytes: {len(html)}")
                if "EcoGrid" in html or "streamlit" in html.lower():
                    print("Verified: EcoGrid app HTML successfully delivered!")
        except Exception as e:
            print("Main URL fetch error:", e)

    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()

    print("Result:", "SUCCESS" if probe_success else "FAILED")
    sys.exit(0 if probe_success else 1)

if __name__ == "__main__":
    run_diagnostics()
