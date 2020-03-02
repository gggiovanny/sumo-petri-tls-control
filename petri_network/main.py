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
    
    # Generando la matriz PRE (condiciones que tiene que cumplir cada transicion para efectuarse)
    # Debe quedar con las transiciones en el eje horizontal y los lugares en el eje vertical:
    #   t0 t1 t2
    # p0 1  0  0 
    # p1 0  1  0 
    # p2 1  0  1 
    # De momento se genera con los ejes inversos y recorre diferente al imprimirlo en pantalla
    pre = []
    for transition in t:
    	pre_col = []
    	for place in p:
    		if transition == place.nextTransition:
    			pre_col.append("1")
    		else:
    			pre_col.append("0")
    	pre.append(pre_col)
    	
    print("PRE MATRIX:")
    for i in range(len(pre[0])):
    	for j in range(len(pre)):
    		print(pre[j][i], end=' ')
    	print()
    	
    # Generando la matriz POS (condiciones que se cumplen luego de una transicion)
    pos = []
    for transition in t:
    	pos_col = []
    	for place in p:
    		if place in transition.nextPlaces:
    			pos_col.append("1")
    		else:
    			pos_col.append("0")
    	pos.append(pos_col)
    	
    print("POS MATRIX:")
    for i in range(len(pos[0])):
    	for j in range(len(pos)):
    		print(pos[j][i], end=' ')
    	print()
    
    pointer = p[0]
    for i in range(10):
        print(pointer.getName(), '-> ', end='')
        if isinstance(pointer, Place) :
            pointer = pointer.nextTransition
        else:
            pointer = pointer.nextPlaces[-1]

