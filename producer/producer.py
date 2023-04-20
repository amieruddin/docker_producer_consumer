#----------------------------------------------------------
#1. Producer
#   i   - accept POST request 
#   ii  - validate body - using jsonschema library     
#   iii - parse var prob, tags
#   iv  - check prob value < 0.25, append low_prob in tags
#   v   - validate input
#   vi  - push message to rabbitmq as producer
#----------------------------------------------------------




import socket
import pika
import json
from flask import Flask, jsonify, request
from jsonschema import validate

app = Flask(__name__)

# v   - validate input
json_validation = {
        "type": "object",
        "properties":{
            "device_id": {"type": "string"},
            "client_id": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "data": {
                "type": "object",
                "properties":{
                    "license_id": {"type": "string"},
                    "preds": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties":{
                                "image_frame": {"type": "string"},
                                "prob": {"type": "number"},
                                "tags": {"type": "array", "items":{"type": "string"}}
                                },
                            "required": ["image_frame", "prob", "tags"]

                        }
                    }
                },
                "required": ["license_id", "preds"]
            }
        },
        "required": ["device_id", "client_id", "created_at", "data"]
    }


def push_to_rabbitmq(information_json):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='tapway_queue')
    channel.basic_publish(exchange='', routing_key='tapway_queue', body=information_json)
    connection.close()



@app.route('/tapway_task', methods=['POST'])
def index():

    if request.method == 'POST':
        content = request.get_json()       #i - accept POST request
        print(f'\n{content}\n', flush=True)


        # ii- validate body - using jsonschema library 
        try:
            validate(instance=content, schema=json_validation)
        except Exception as e:
            print(f'{str(e)}')
            return str(e), 400
        
        # iii - parse var prob, tags & update tags
        prob = content['data']['preds'][0]['prob']
        tags = content['data']['preds'][0]['tags']

        # iv - check prob value < 0.25, append low_prob in tags
        for i in content['data']['preds']:
            if i['prob'] < 0.25:
                i['tags'].append('low_prob')

        print(content)

        # vi - push message to rabbitmq
        information_json = json.dumps(content)
        push_to_rabbitmq(information_json)
        print('Successful send JSON to exchanger..')

        
        return jsonify(result={"status": 200})



if __name__ == "__main__":
    # host_IP = socket.gethostbyname_ex(socket.gethostname() + '.local')[-1][-1]
    # print('Host IP : ',host_IP)
    app.run(host='0.0.0.0', port=5000, debug=True)
