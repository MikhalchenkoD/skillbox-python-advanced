from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/get_example', methods=['GET'])
def get_example():
    data = {'message': 'This is a GET request example'}
    return jsonify(data)


@app.route('/post_example', methods=['POST'])
def post_example():
    data = {'message': 'This is a POST request example'}
    return jsonify(data)


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://go.skillbox.ru'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-My-Fancy-Header'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
