from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get("code", "")
    print(code)
    
    return jsonify({"output": "", "error": ""})

if __name__ == '__main__':
    app.run(debug=True)