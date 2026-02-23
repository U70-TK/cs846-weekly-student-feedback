from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculator', methods=['POST'])
def calculate():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)