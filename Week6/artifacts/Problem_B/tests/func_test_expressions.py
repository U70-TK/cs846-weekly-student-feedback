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
    func_test_expressions(port=5000)