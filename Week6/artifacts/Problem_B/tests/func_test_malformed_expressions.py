import requests

def func_test_malformed_expressions(port) -> bool:
    url = f"http://localhost:{port}/calculator"
    tasks = ["1 *", "30-"]

    for expression in tasks:
        r = requests.post(url=url, json={"expression": expression})
        if r.status_code != 400:
            print("POST '%s' not 400: %d %s" % (url, r.status_code, r.reason))
            return False
    print("test ok")
    return True

if __name__ == "__main__":
    func_test_malformed_expressions(port=5000)