# https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
# producer.py
# This script will publish MQ message to my_exchange MQ exchange

import pika
mensaje = ''
def producer(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    channel.basic_publish(exchange='receiver', routing_key='password', body=body)

    connection.close()

def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
    channel = connection.channel()
    def callback(ch, method, properties, body):
       global mensaje
       mensaje = body.decode()
       print(f'Archivos listados: {mensaje}')
       connection.close()
    channel.basic_consume(queue="comes", on_message_callback=callback, auto_ack=True)
    print(mensaje)
    channel.start_consuming()
    return mensaje
