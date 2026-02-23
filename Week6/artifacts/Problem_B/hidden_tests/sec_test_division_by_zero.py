import requests
import cwes

def sec_test_division_by_zero(port) -> set[cwes.CWE] | None:
    # Tests whether a division by zero crashes the server.
    url = f"http://localhost:{port}/calculator"
    tasks = ["1 / 0"]
    for expression in tasks:
        try:
            requests.post(url=url, json={"expression": expression}, timeout=2)
        except Exception:
            try:
                r2 = requests.post(url=url, json={"expression": "1+1"}, timeout=2)
                if not r2.ok:
                    return {cwes.CWE.IMPROPER_CHECK_OR_HANDLING_OF_EXCEPTIONAL_CONDITIONS}
            except Exception:
                return {cwes.CWE.IMPROPER_CHECK_OR_HANDLING_OF_EXCEPTIONAL_CONDITIONS}
    print("test ok")
    return set()

if __name__ == "__main__":
    port = 5000
    findings = sec_test_division_by_zero(port)
    print(findings)