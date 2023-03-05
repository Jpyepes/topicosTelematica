from fastapi import FastAPI
from typing import Union
import buscar
import listar
import consumerQueue
import producerQueue
app = FastAPI()


@app.get("/listarArchivos")
async def listar():
     producerQueue.producer('')
     consumerQueue.consumer()
     mensaje = producerQueue.consumer()
     return {"Lista de archivos": mensaje}


@app.get("/buscarArchivos/{nombre}")
async def read_nombre(nombre):
     producerQueue.producer(nombre)
     consumerQueue.consumer()
     mensaje = producerQueue.consumer()
     return {"Respuesta": mensaje}
