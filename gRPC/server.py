from concurrent import futures

import os
import grpc
import mensaje_pb2
import mensaje_pb2_grpc
from google.protobuf.json_format import MessageToDict
HOST = '[::]:50051'

class ProductService(mensaje_pb2_grpc.ProductServiceServicer):
   def AddProduct(self, request, context):
        print(request)
        if str(request) == "":
          mensaje = os.listdir()
        else:
           contenido = os.listdir()
           pregunta = str(request)[15:-2]
           if pregunta.rstrip() in contenido:
               mensaje = [f"El archivo '{pregunta}' si está en el directorio"]
           else:
               mensaje = [f"El archivo '{pregunta}' no está en el directorio"]
        return mensaje_pb2.TransactionResponse(code=mensaje)
 
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  mensaje_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
  server.add_insecure_port(HOST)
  print("Service is running... ")
  server.start()
  server.wait_for_termination()

if __name__ == "__main__":
    serve()