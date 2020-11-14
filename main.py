import numpy as np

global datos #= np.array((1,3))

def llenar():
  key = 0
  while(key == 0):
    n = int(input("\nCantidad de aspirantes: "))
    if(n > 0 and n <= 20):
      key = 1
    else:
      print("\nCantidad de aspirantes no permitido")
    
  cedula = [None] * n
  edad = [None] * n
  salario = [None] * n
    
  for i in range(n):
    print("\nAspirante "+str(i+1))
    cedula[i] = int(input("Numero cedula del aspirante " + str(i+1) + ": "))
    edad[i] = int(input("Edad del aspirante " + str(i+1) + ": "))
    salario[i] = int(input("Salario pretendido por el aspirante " + str(i+1) + ": "))
  bonos = np.zeros(n)
  datos = np.array((cedula, edad, salario, bonos))
  return datos
    
def darCantidadContratados(datos):
  total = 0
  filas, columnas = datos.shape
  for columna in range(columnas):
    if (datos[1][columna]<30 and (datos[2][columna]>=500000 and datos[2][columna]<=800000) ):
      total += 1
  return total

def crearTablaDeContratados(datos):
  cedulas = []
  edades = []
  salarios = []
  bonos = []
  filas, columnas = datos.shape
  for columna in range(columnas):
    if (datos[1][columna]<30 and (datos[2][columna]>=500000 and datos[2][columna]<=800000) ):
      cedulas.append(datos[0][columna])
      edades.append(datos[1][columna])
      salarios.append(datos[2][columna])
      bonos.append(datos[3][columna])
  reporte = np.array((cedulas, edades, salarios, bonos))
  return reporte
  
def calcularCantidadConBono(elegidos):
  cantidad = 0
  filas, columnas = elegidos.shape
  for columna in range(columnas):
    if(elegidos[2][columna] < 600000):
      elegidos[3][columna] = elegidos[2][columna]*0.05
      cantidad += 1
  return cantidad

def calcularTotalDeNomina(elegidos):
  nomina = 0
  filas, columnas = elegidos.shape
  for columna in range(columnas):
    nomina += elegidos[2][columna] + elegidos[3][columna]
  return nomina

def escogerMasViejos(elegidos):
  filas, columnas = elegidos.shape
  mayores = ordenarMenorAMayorPorEdad(elegidos, 0, columnas)
  losMayores = []
  for columna in range(columnas):
    if(mayores[1][columnas -1] == mayores[1][columna]):
      losMayores.append([mayores[0][columna]])
  return [losMayores, mayores[1][columnas -1]]

def escogerMasJovenes(elegidos, inicio, final):
  menores = ordenarMenorAMayorPorEdad(elegidos, inicio, final)
  losMenores = []
  for i in range(inicio, final +1):
    if(menores[1][inicio] == menores[1][i]):
      losMenores.append([menores[0][i]])
  return [losMenores, menores[1][inicio]]


def ordenarMenorAMayorPorCedula (elegidos, inicio, final):
  # var = 0 para cedula
  reporte = ordenarMenorAMayor(elegidos, inicio, final, 0)
  return reporte

def ordenarMenorAMayorPorEdad (elegidos, inicio, final):
  # var = 1 para edad
  reporte = ordenarMenorAMayor(elegidos, inicio, final, 1)
  return reporte

def ordenarMenorAMayorPorSalario (elegidos, inicio, final):
  # var = 2 para salario
  reporte = ordenarMenorAMayor(elegidos, inicio, final, 2)
  return reporte

def ordenarMenorAMayorPorBonificacion (elegidos, inicio, final):
  # var = 3 para bonos
  return ordenarMenorAMayor(elegidos, inicio, final, 3)


def ordenarMenorAMayor(elegidos, inicio, final, var):
  filas, columnas = elegidos.shape
  reporte = np.zeros((filas, columnas))
  elementos = []
  for columna in range(columnas):
    elementos.append([ elegidos[0][columna], elegidos[1][columna], elegidos[2][columna], elegidos[3][columna]])
  quick_sort(elementos, inicio, final, var)
  for i in range(len(elementos)):
    for j in range (0,4):
      reporte[j][i] = elementos[i][j]
  return reporte

def quick_sort(lista, inicio, fin, var):
  # Caso base
  if inicio >= fin:
    return
  # Caso recursivo
  menores = partition(lista, inicio, fin, var)
  quick_sort(lista, inicio, menores - 1, var)
  quick_sort(lista, menores + 1, fin, var)

def partition(lista, inicio, fin, var):
  pivote = lista[inicio][var]
  menores = inicio
  # Cambia de lugar los elementos
  for i in range(inicio+1, fin + 1):
    if lista[i][var] < pivote:
      menores += 1
      if i != menores:
        swap(lista, i, menores)
  # Pone el pivote al final de los menores
  if inicio != menores:
    swap(lista, inicio, menores)
  # Devuelve la posición del pivote
  return menores

def swap(lista, i, j):
  lista[j], lista[i] = lista[i], lista[j]


def mostrarDatos(elegidos):
  print ("Cedula \t Edad \t Salario \t Bono")
  filas, columnas = elegidos.shape
  texto = ""
  for columna in range(columnas):
    for fila in range(filas):
      texto +=  str(elegidos[fila][columna]) + " \t "
    texto += "\n"
  print (texto)     

def prueba(datos):
  numPosibles = darCantidadContratados(datos)
  print("De los contratados se puede contratar "+ str(numPosibles))

  elegidos = crearTablaDeContratados(datos)
  numConBono = calcularCantidadConBono(elegidos)
  print("De los contratables " + str(numConBono) + " tienen derecho a bono")
  
  totalNomina = calcularTotalDeNomina(elegidos)
  print("El valor de la nómina es de " + str(totalNomina))

  filas, columnas = elegidos.shape
  reporte = ordenarMenorAMayorPorCedula(elegidos, 0, columnas -1)

  print("\nINFORMACION DE LOS TRABAJADORES CONTRATABLES")
  mostrarDatos(reporte)

  print("\nDe los contratables los que tienen mayor edad son: ")
  losMayores = escogerMasViejos(elegidos, 0, columnas-1)
  for i in range(len(losMayores[0])):
    print(f"ced No. {losMayores[0][i]}")
  print (f"Con {losMayores[1]} años")


def main():
  datos = llenar()
  #cedula = [123,456,128,129,146]
  #edad = [25,25,36,19,24]
  #salario = [700000,800000,900000,550000,1000000]
  #bonos = [0,0,0,0,0]
  #datos = np.array((cedula, edad, salario, bonos))
  prueba(datos)
  
  
main()