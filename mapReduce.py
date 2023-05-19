from mrjob.job import MRJob
import statistics

class MRpromedioSalarioSE(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #idemp,sececon,salary,year
        idemp,sececon,salary,year=line.split(",")
        yield sececon,int(salary)

    def reducer(self, key, values):
        yield key, statistics.mean(values)

class MRpromedioSalarioE(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #idemp,sececon,salary,year
        idemp,sececon,salary,year=line.split(",")
        yield idemp,int(salary)

    def reducer(self, key, values):
        yield key, statistics.mean(values)

class MRsectorEconomicoE(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #idemp,sececon,salary,year
        idemp,sececon,salary,year=line.split(",")
        yield idemp,1

    def reducer(self, key, values):
        yield key, sum(values)

#--------------------------------------------------------------------------------

class MRaccion(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #company,price,date
        company,price,date=line.split(",")
        yield company,[float(price),date]

    def reducer(self, key, values):
        temp = list(values)
        valorMenor = min(temp)
        valorMayor = max(temp)
        accion = f'Dia con menor valor {valorMenor[1]}, Dia con mayor valor {valorMayor[1]}'
        yield key, accion

class MRaccionMayorEstable(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #company,price,date
        company,price,date=line.split(",")
        yield company, float(price)

    def reducer(self, key, values):
        precioActual = 0
        estado = ''
        for price in values: 
            if price >= precioActual:
                estado = 'Se mantiene estable'
            else: 
                estado = 'No se mantiene estable'
            precioActual = price
        yield key,estado

class MRdiaNegro(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #company,price,date
        company,price,date=line.split(",")
        yield 1, (date, float(price))

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            fecha = valor[0]
            precio = valor[1]
            if fecha in valores:
                valores[fecha] += precio
            else:
                valores[fecha] = precio
        listaKeys = []
        listaValues = []
        resultado = ''
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        resultado = f'En el dia {listaKeys[listaValues.index(min(listaValues))]} la mayor cantidad de acciones tuvo el menor valor de accion'
        item = '' 
        yield resultado, item
if __name__ == '__main__':
    #MRpromedioSalarioE.run()
    #MRaccion.run()
    #MRaccionMayorEstable.run()
    MRdiaNegro.run()