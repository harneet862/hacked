from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chrome_extension', methods=['POST'])
def handle_chrome_extension_data():
    data = request.get_json()
    # Process Chrome extension data
    print("Received data from Chrome extension:", data)
    return jsonify({"message": "Data from Chrome extension received successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)