from fastapi import FastAPI
from typing import Union
<<<<<<< HEAD
import grpc
import sys
from google.protobuf.json_format import MessageToDict
sys.path.insert(0, 'gRPC')
import mensaje_pb2
import mensaje_pb2_grpc
=======
import buscar
import listar
import consumerQueue
import producerQueue
>>>>>>> 02f554a (Comunicación MOM)
app = FastAPI()


@app.get("/listarArchivos")
<<<<<<< HEAD
async def read_root():
    channel = grpc.insecure_channel('localhost:50051')
    stub = mensaje_pb2_grpc.ProductServiceStub(channel)
    response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request="")))
    print(response)
    return {"Lista de archivos": response}
=======
async def listar():
     producerQueue.producer('')
     consumerQueue.consumer()
     mensaje = producerQueue.consumer()
     return {"Lista de archivos": mensaje}
>>>>>>> 02f554a (Comunicación MOM)


@app.get("/buscarArchivos/{nombre}")
async def read_nombre(nombre):
<<<<<<< HEAD
    channel = grpc.insecure_channel('localhost:50051')
    stub = mensaje_pb2_grpc.ProductServiceStub(channel)
    response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request=nombre)))
    print(response)
    return {"Respuesta": response}

=======
     producerQueue.producer(nombre)
     consumerQueue.consumer()
     mensaje = producerQueue.consumer()
     return {"Respuesta": mensaje}
>>>>>>> 02f554a (Comunicación MOM)
