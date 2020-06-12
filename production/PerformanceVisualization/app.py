import time
from flask import Flask
from flask import jsonify, request, make_response
import profileclient

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/submit', methods=['POST'])
def submit():
    # json_data is a dict with string key/val pairs
    # keys:     inputValue
    #           predictionValue
    #           graphSelected
    #           functionSelected
    json_data = request.get_json()
    # profiling_data = profileclient.Profiler().testProfile(int(json_data['functionSelected']), int(json_data['inputValue']))
    input = json_data['inputValue']
    prediction = json_data['predictionValue']
    mock_return_obj = {
        "points": [
            [1,1],
            [2,2],
            [3,3],
            [4,4],
            [5,5]
        ],
        "n": input,
        "m": prediction
    }
    return jsonify(status=200, data=mock_return_obj)

if __name__ == '__main__':
    app.run()
