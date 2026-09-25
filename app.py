from flask import Flask, render_template, request, jsonify
from polarion_service import PolarionService

app = Flask(__name__)
polarion_service = PolarionService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trace', methods=['POST'])
def query_trace():
    data = request.get_json() or {}
    requirement_input = data.get('requirement', '')

    if not requirement_input or not requirement_input.strip():
        return jsonify({
            "success": False,
            "error": "Please provide a functional requirement ID or requirement description."
        }), 400

    config = {
        "server_url": data.get("server_url", "https://polarion.example.com"),
        "project_id": data.get("project_id", "DRIVE_SYS"),
        "token": data.get("token", ""),
        "use_mock": data.get("use_mock", True)
    }

    result = polarion_service.get_trace(requirement_input, config)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "Polarion Trace Viewer API"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
