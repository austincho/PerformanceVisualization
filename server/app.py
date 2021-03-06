import time
from flask import Flask
from flask import jsonify, request, make_response

from server import regression, profileclient
from server.profileclient import Profiler


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
    inputVal = int(json_data['inputValue'])
    predictionVal = int(json_data['predictionValue'])
    fn_code = int(json_data['functionSelected'])
    # profiling_data = profileclient.Profiler().testProfile(fn_code, inputVal)

    p = Profiler()
    p.getNRuntimes(fn_code, inputVal, predictionVal)
    data_obj = regression.predict(fn_code, inputVal, predictionVal)

    return_obj = {
        "graphSelected": json_data['graphSelected'],
        "prediction": data_obj["predictions"],
        "actual": data_obj["actual"],
        "n": inputVal,
        "m": predictionVal
    }
    return jsonify(status=200, data=return_obj)

if __name__ == '__main__':
    app.run()
