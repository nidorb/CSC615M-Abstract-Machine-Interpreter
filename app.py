from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get("code", "")
    try:
        result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=5)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)