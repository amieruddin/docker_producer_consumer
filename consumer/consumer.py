#----------------------------------------------------------
#1. Consumer
#   i   - connnect to raabbitmq
#   ii  - save data to csv     
#   iii - ack rmq
#----------------------------------------------------------


import os
import pika
import csv
import json
import socket


def proces_message(ch, method, properties, body):
    information = json.loads(body)
    print(information)

    #ii. save into csv
    header = ["device_id", "client_id", "created_at", "license_id", "image_frame", "prob", "tags"]
    rows = []
    for info in information['data']['preds']:
        row = [
            information["device_id"],
            information["client_id"],
            information["created_at"],
            information['data']["license_id"],
            info["image_frame"],
            info["prob"],
            ','.join(info["tags"])
        ]
        rows.append(row)

    data_csv = '/app/data/data.csv'
    try:
        with open(data_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not os.path.isfile(data_csv):
                writer.writerow(header)
            writer.writerows(rows)
    except:
        print('not save csv', flush=True)

    print(information , '\n', flush=True)

    #iii. acknowledge rmq
    ch.basic_ack(delivery_tag=method.delivery_tag)

#i. connect to rabbitmq
# host_IP = socket.gethostbyname_ex(socket.gethostname() + '.local')[-1][-1]
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='tapway_queue')
channel.basic_consume(queue='tapway_queue', on_message_callback=proces_message)

print('Start consuming...')
print('host_IP : ', connection)
channel.start_consuming()
