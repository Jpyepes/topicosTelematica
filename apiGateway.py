from fastapi import FastAPI
from typing import Union
import grpc
import sys
from google.protobuf.json_format import MessageToDict
sys.path.insert(0, 'gRPC')
import mensaje_pb2
import mensaje_pb2_grpc
import buscar
import listar
import consumerQueue
import producerQueue
app = FastAPI()

roundRobin = 0
@app.get("/listarArchivos")
async def read_root():
    global roundRobin
    if roundRobin == 0:
        channel = grpc.insecure_channel('localhost:50051')
        stub = mensaje_pb2_grpc.ProductServiceStub(channel)
        response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request="")))
        print(response)
        roundRobin = 1
        return {"Lista de archivos": response}
    else:
        producerQueue.producer('')
        consumerQueue.consumer()
        mensaje = producerQueue.consumer()
        roundRobin = 0
        return {"Lista de archivos": mensaje}

@app.get("/buscarArchivos/{nombre}")
async def read_nombre(nombre):
    global roundRobin
    if roundRobin ==0:
        channel = grpc.insecure_channel('localhost:50051')
        stub = mensaje_pb2_grpc.ProductServiceStub(channel)
        response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request=nombre)))
        print(response)
        print(roundRobin)
        roundRobin = 1
        return {"Respuesta": response}
    else:
        producerQueue.producer(nombre)
        consumerQueue.consumer()
        mensaje = producerQueue.consumer()
        print(roundRobin)
        roundRobin = 0
        return {"Respuesta": mensaje}
