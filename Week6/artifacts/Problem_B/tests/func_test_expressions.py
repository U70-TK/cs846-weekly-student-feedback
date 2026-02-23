import requests

def func_test_expressions(port) -> bool:
    url = f"http://localhost:{port}/calculator"
    tasks = {
        "1 + 2*3": "7",
        "10 - 15": "-5",
    }

    for expression, result in tasks.items():
        r = requests.post(url=url, json={"expression": expression})
        if not r.ok:
            print("POST '%s' not ok: %d %s" % (url, r.status_code, r.reason))
            return False

        print(
            "got 200 response for POST: %s. Expected result: %s" % (str(r.json()), result)
        )
        if r.json().get("result") != result:
            return False

    print("test ok")
    return True

if __name__ == "__main__":
    import subprocess
    import sys
    import time
    from pathlib import Path

    def _start_app() -> subprocess.Popen:
        app_path = (Path(__file__).resolve().parents[1] / "app.py").resolve()
        return subprocess.Popen(
            [sys.executable, str(app_path)],
            cwd=str(app_path.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _wait_for_app(port: int, timeout_s: float = 5.0) -> None:
        url = f"http://localhost:{port}/calculator"
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            try:
                r = requests.post(url=url, json={"expression": "1+1"}, timeout=1)
                if r.ok:
                    return
            except Exception:
                pass
            time.sleep(0.1)
        raise RuntimeError("App failed to start within timeout")

    def _is_app_up(port: int) -> bool:
        url = f"http://localhost:{port}/calculator"
        try:
            r = requests.post(url=url, json={"expression": "1+1"}, timeout=1)
            return r.ok
        except Exception:
            return False

    app_proc = None
    try:
        if _is_app_up(port=12345):
            findings = func_test_expressions(port=12345)
            print(findings)
            raise SystemExit(0)
        app_proc = _start_app()
        _wait_for_app(port=12345)
        findings = func_test_expressions(port=12345)
        print(findings)
    finally:
        if app_proc is not None:
            app_proc.terminate()
            try:
                app_proc.wait(timeout=2)
            except Exception:
                app_proc.kill()
