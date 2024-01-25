from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

brightness = 0  # переменная для хранения значения яркости

@app.route('/brightness', methods=['GET'])
def get_brightness():
    return jsonify({'brightness': brightness})

@app.route('/brightness', methods=['POST'])
def set_brightness():
    global brightness
    data = request.json
    brightness = data['value']
    return jsonify({'message': f'Brightness set to {brightness}'})

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
