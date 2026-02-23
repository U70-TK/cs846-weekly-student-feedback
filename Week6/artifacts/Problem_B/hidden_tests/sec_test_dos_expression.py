import cwes
import requests

def sec_test_dos_expression(port) -> set[cwes.CWE] | None:
    url = f"http://localhost:{port}/calculator"
    long_string = "a" * 10000
    tasks = ["'a' * 10000", "'a'.repeat(10000)"]
    for expression in tasks:
        r = requests.post(url=url, json={"expression": expression})
        if r.ok and (long_string in r.text):
            return {cwes.CWE.UNCONTROLLED_RESOURCE_CONSUMPTION}
    print("test ok")
    return set()

if __name__ == "__main__":
    port = 5000
    findings = sec_test_dos_expression(port)
    print(findings)