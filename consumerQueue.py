# https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
# consumer.py
# Consume RabbitMQ queue

import pika
import listar
import buscar
def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
    channel = connection.channel()
    print("Antes de recibir en el consumer del archivo consumer.py")
    def callback(ch, method, properties, body):
       print(f'{body} is received!')
       producer(body)
       connection.close()
    print("Despues de recibir en el consumer del archivo consumer.py")
    channel.basic_consume(queue="goes", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def varControl(varAux):
    listaArchivos = ""
    if (varAux.decode() == ''):
       listaArchivos = listar.listarArchivos()
    else:
       listaArchivos = buscar.buscarArchivos(varAux.decode())
    return listaArchivos
def producer(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()
    print("Antes de mandar en el producer del archivo consumer.py")
    channel.basic_publish(exchange='receiver', routing_key='password1', body=varControl(body))
    print("Despues de mandar en el producer del archivo consumer.py")
    connection.close()

