class Transition:
    def __init__(self, id):
        self.id = id
        self.nextPlaces = []
    id = 0
    nextPlaces = []
    def getName(self):
        return "t{}".format(self.id)
    def printName(self):
        print(self.getName())
    def printNextNames(self):
        for place in self.nextPlaces:
            print(place.getName())
    
class Place:
    def __init__(self, id):
        self.id = id
        self.nextPlaces = []
    id = 0
    nextTransition = None
    marcado = 0
    def getName(self):
        return "p{}".format(self.id)
    def printName(self):
        print(self.getName())
    def printNextNames(self):
        print(self.nextTransition.getName())


if __name__ == "__main__":
    # Generando una lista de objetos Places() (Lugares) en una lista llamada 'p'
    p = []
    for i in range(6): # del 0 al 6
        p.append(Place(i)) # se le pasa i como argumento, que sera la id del Place()
    
    # Repitiendo el mismo proceso para generar los objetos tipo Transition() en la lista 't'
    t = []
    for i in range(5):
        t.append(Transition(i)) # se le pasa i como argumento, que sera la id del Transition()
    
    p[0].nextTransition = t[0]
    t[0].nextPlaces.append(p[1])
    p[1].nextTransition = t[1]
    t[1].nextPlaces.append(p[2])
    p[2].nextTransition = t[2]
    t[2].nextPlaces.append(p[0])
    
    p[3].nextTransition = t[0]
    t[0].nextPlaces.append(p[4])
    p[4].nextTransition = t[3]
    t[3].nextPlaces.append(p[5])
    p[5].nextTransition = t[4]
    t[4].nextPlaces.append(p[3])
    
    # print(p[0].getName())
    # print(p[0].nextTransition.getName())
    

    
    pointer = p[0]
    for i in range(10):
        print(pointer.getName(), '-> ', end='')
        if isinstance(pointer, Place) :
            pointer = pointer.nextTransition
        else:
            pointer = pointer.nextPlaces[-1]
            
"""
TODO: 
+ Setear estados iniciales
+ Cada Place puede tener mas de una marca
+ Generar matrices pre y post automaticamente a partir de la definicion con objetos nodo (es posible?)
+ Al definir con objetos la red programatically hallar la manera de poner la condicion de que  para que se efectue la transicion se necesiten mas de una marca
+ Recorrer la red segun las condiciones pre y post

"""