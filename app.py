from flask import Flask, request, jsonify
from consul import Consul
import logging
app = Flask(__name__)
# consul = Consul()
# Fetch the conviguration:
# consul.apply_remote_config()
# # Register Consul service:
# consul.register_service(
#     name='my-web-app',
#     interval='10s',
#     tags=['webserver', ],
#     port=5000,
#     httpcheck='http://localhost:5000/healthcheck'
# )
logger = logging.Logger('logger')


@app.route('/healthcheck')
def health_check():
    return 'OK ', 200


@app.route('/get_value')
def get_value():
    key_name = request.query_string.decode("utf-8")
    c = Consul('consul-master')
    index, data = c.kv.get(key_name, index=None)
    print(data['Value'])
    return data['Value']



@app.route('/set_value')
def set_value():
    result = 'Success'
    try:
        qs = request.query_string.decode("utf-8")
        key, val = qs.split('=')
        c = Consul()
        response = c.kv.put(key, val)
        result = 'Success' if True == response else 'Fail'
    except Exception as e:
        logger.error("Fatal error in main loop", exc_info=True)
        result = 'Fail'
    finally:
        return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

