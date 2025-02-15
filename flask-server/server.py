from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/api/chrome_extension', methods=['POST'])
def handle_chrome_extension_data():
    data = request.get_json()
    # here the data will be a python dict and the keys we have are 
    # date, start_time, end_time, title and description
    # Process Chrome extension data
    print("Received data from Chrome extension:", data)
    return jsonify({"message": "Data from Chrome extension received successfully"}), 200

@app.route('/api/frontend', methods=['POST'])
def handle_frontend_data():
    data = request.get_json()
    # Process frontend data
    print("Received data from frontend:", data)
    return jsonify({"message": "Data from frontend received successfully"}), 200

@app.route('/api', method=['GET'])
def send_data():
    
if __name__ == "__main__":
    app.run(debug=True)
