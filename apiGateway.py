from fastapi import FastAPI
from typing import Union
import grpc
import sys
from google.protobuf.json_format import MessageToDict
sys.path.insert(0, 'gRPC')
import mensaje_pb2
import mensaje_pb2_grpc
app = FastAPI()


@app.get("/listarArchivos")
async def read_root():
    channel = grpc.insecure_channel('localhost:50051')
    stub = mensaje_pb2_grpc.ProductServiceStub(channel)
    response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request="")))
    print(response)
    return {"Lista de archivos": response}


@app.get("/buscarArchivos/{nombre}")
async def read_nombre(nombre):
    channel = grpc.insecure_channel('localhost:50051')
    stub = mensaje_pb2_grpc.ProductServiceStub(channel)
    response = MessageToDict(stub.AddProduct(mensaje_pb2.Product(code_request=nombre)))
    print(response)
    return {"Respuesta": response}

