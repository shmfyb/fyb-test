from flask import Flask, request, jsonify
from consul import Consul
import logging
import sys
app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@app.route('/healthcheck')
def health_check():
    return 'OK ', 200


@app.route('/get_value')
def get_value():
    result = 'Error', 400
    try:
        key_name = request.query_string.decode("utf-8")
        logger.info(f"try to fetch key :{key_name}")
        c = Consul()
        index, data = c.kv.get(key_name, index=None)
        result = data['Value'], 200
    except Exception:
        logger.error(f"Fail to get key : {key_name}")
    finally:
        return result


@app.route('/set_value')
def set_value():
    try:
        qs = request.query_string.decode("utf-8")
        key, val = qs.split('=')
        c = Consul()
        response = c.kv.put(key, val)
        if response:
            result = 'Success', 200
        else:
            result = 'Fail', 400
    except Exception as e:
        logger.error(f"Fail to set key: {key}, with value: {val}")
        result = 'Fail', 400
    finally:
        return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

