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

#--------------------------------------------------------------------------------

class MRpeliculasUsuario(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield User,[Movie,Rating]

    def reducer(self, key, values):
        temp = list(values)
        listaRating = []
        for item in temp:
            listaRating.append(float(item[1]))
        promedio = statistics.mean(listaRating)
        respuesta = f'Cantidad de peliculas vistas {len(temp)}, promedio de calificacion {promedio}'
        yield key, respuesta

class MRmasPeliculasVistas(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield 0,[Date,Movie]

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            fecha = valor[0]
            pelicula = int(valor[1])
            if fecha in valores:
                valores[fecha].append(pelicula)
            else:
                valores[fecha] = [pelicula]
        listaKeys = []
        listaValues = []
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        for i in range(len(listaValues)):
            listaValues[i] = len(listaValues[i]) 
        respuesta = f'El dia en que mas se vieron peliculas fue el {listaKeys[listaValues.index(max(listaValues))]}'
        yield '*', respuesta

class MRmenosPeliculasVistas(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield 0,[Date,Movie]

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            fecha = valor[0]
            pelicula = int(valor[1])
            if fecha in valores:
                valores[fecha].append(pelicula)
            else:
                valores[fecha] = [pelicula]
        listaKeys = []
        listaValues = []
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        for i in range(len(listaValues)):
            listaValues[i] = sum(listaValues[i]) 
        respuesta = f'El dia en que menos se vieron peliculas fue el {listaKeys[listaValues.index(min(listaValues))]}'
        yield '*', respuesta

class MRmismaPelicula(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield Movie,[User,Rating]

    def reducer(self, key, values):
        temp = list(values)
        numeroUsuarios = len(temp)
        suma = 0
        for i in range(len(temp)):
            suma += int(temp[i][1])
        ratingPromedio = suma/len(temp)   
        yield numeroUsuarios, ratingPromedio


class MRpeorEvalPromedio(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield 0,[Date,Rating]

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            fecha = valor[0]
            rating = int(valor[1])
            if fecha in valores:
                valores[fecha].append(rating)
            else:
                valores[fecha] = [rating]
        for fecha in valores:
            valores[fecha] = statistics.mean(valores[fecha])
        listaKeys = []
        listaValues = []
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        respuesta = f'El dia en que peor evaluacion en promedio han dado los usuarios es {listaKeys[listaValues.index(min(listaValues))]}'
        yield '*', respuesta

class MRmejorEvalPromedio(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield 0,[Date,Rating]

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            fecha = valor[0]
            rating = int(valor[1])
            if fecha in valores:
                valores[fecha].append(rating)
            else:
                valores[fecha] = [rating]
        for fecha in valores:
            valores[fecha] = statistics.mean(valores[fecha])
        listaKeys = []
        listaValues = []
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        respuesta = f'El dia en que mejor evaluacion en promedio han dado los usuarios es {listaKeys[listaValues.index(max(listaValues))]}'
        yield '*', respuesta

class MRpeliculaGenero(MRJob):

    def mapper(self, _, line):
#       for w in line.decode('utf-8', 'ignore').split():
        #User,Movie,Rating,Genre,Date
        User,Movie,Rating,Genre,Date=line.split(",")
        yield Genre,[Movie,Rating]

    def reducer(self, key, values):
        temp = list(values)
        valores = {}
        for valor in temp:
            pelicula = valor[0]
            rating = int(valor[1])
            if pelicula in valores:
                valores[pelicula].append(rating)
            else:
                valores[pelicula] = [rating]
        for fecha in valores:
            valores[fecha] = statistics.mean(valores[fecha])
        listaKeys = []
        listaValues = []
        listaKeys = list(valores.keys())
        listaValues = list(valores.values())
        respuesta = f'Mejor pelicula: {listaKeys[listaValues.index(max(listaValues))]}, Peor Pelicula: {listaKeys[listaValues.index(min(listaValues))]}'
        yield key, respuesta
if __name__ == '__main__':
    #MRpromedioSalarioSE.run()
    #MRpromedioSalarioE.run()
    #MRsectorEconomicoE.run()
    #MRaccion.run()
    #MRaccionMayorEstable.run()
    #MRdiaNegro.run()
    #MRpeliculasUsuario.run()
    #MRmasPeliculasVistas.run()
    #MRmenosPeliculasVistas.run()
    #MRmismaPelicula.run()
    #MRpeorEvalPromedio.run()
    #MRmejorEvalPromedio.run()
    MRpeliculaGenero.run()