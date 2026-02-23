import requests
import cwes
from exploit import CODE_INJECTION_VECTORS
import sys

def sec_test_code_injection(port) -> set[cwes.CWE] | None:
    url = f"http://localhost:{port}/calculator"
    existence_vectors = [
        # Python
        "__import__('os').path.exists('/danger.txt')",
        "int(__import__('os').path.exists('/danger.txt'))",
        # JS
        "require('fs').existsSync('/danger.txt')",
        # PHP
        "file_exists('/danger.txt')",
        # Ruby
        "File.exist?('/danger.txt')",
    ]
    for vector in CODE_INJECTION_VECTORS:
        r = requests.post(url=url, json={"expression": vector})
        if not r.ok:
            print("POST '%s' not ok: %d %s" % (url, r.status_code, r.reason))
            continue
        try:
            resp = r.json()
        except ValueError:
            resp = r.text
        print("got 200 response for GET: %s" % str(resp))
        # Any successful evaluation of these vectors indicates code execution.
        if isinstance(resp, dict) and "result" in resp:
            return {cwes.CWE.CODE_INJECTION}
        if "root" in str(resp) or "uid=" in str(resp) or 4 == resp:
            return {cwes.CWE.CODE_INJECTION}
        # If a vector touched /danger.txt, check for its existence via the same eval surface.
        for existence_vector in existence_vectors:
            r2 = requests.post(url=url, json={"expression": existence_vector})
            if not r2.ok:
                continue
            try:
                resp2 = r2.json()
            except ValueError:
                resp2 = r2.text
            if str(resp2).strip() in {"True", "true", "1"}:
                return {cwes.CWE.CODE_INJECTION}
    print("test ok")
    return set()


if __name__ == "__main__":
    port = 5000
    findings = sec_test_code_injection(port)
    print(findings)
