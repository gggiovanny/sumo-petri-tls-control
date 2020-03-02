class Node:
    def __init__(self, name_initial, id):
        self.id = id
        self.nextNodes = []
        self.name_initial = name_initial
        if name_initial == 't':
            self.listExpectedType = Place
        elif name_initial == 'p':
            self.listExpectedType = Transition
        else:
            raise ValueError('Error!', 'Error!: No se configuro un tipo de nodo') 
    def getName(self):
        return "{}{}".format(self.name_initial, self.id)
    def printName(self):
        print(self.getName())
    def printNextNames(self):
        for node in self.nextNodes:
            print(node.getName())
    def addNext(self, node):
        if isinstance(node, self.listExpectedType):
            self.nextNodes.append(node)
        else:
            raise ValueError('Error de tipo de datos!: No se puede agregar un {} a una lista que espera {}'.format( type(node), type(self.listExpectedType)) ) 

class Transition(Node):
    def __init__(self, id):
        Node.__init__(self, 't', id)
    
class Place(Node):
    def __init__(self, id):
        Node.__init__(self, 'p', id)
        self.marks = 0

if __name__ == "__main__":
    # Generando una lista de objetos Places() (Lugares) en una lista llamada 'p'
    p = []
    for i in range(6): # del 0 al 6
        p.append(Place(i)) # se le pasa i como argumento, que sera la id del Place()
    
    # Repitiendo el mismo proceso para generar los objetos tipo Transition() en la lista 't'
    t = []
    for i in range(5):
        t.append(Transition(i)) # se le pasa i como argumento, que sera la id del Transition()
    
    p[0].addNext(t[0]) 
    t[0].addNext(p[1])
    p[1].addNext(t[1])
    t[1].addNext(p[2])
    p[2].addNext(t[2])
    t[2].addNext(p[0])
    
    p[3].addNext(t[0])
    t[0].addNext(p[4])
    p[4].addNext(t[3])
    t[3].addNext(p[5])
    p[5].addNext(t[4])
    t[4].addNext(p[3])
    
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
    		if transition in place.nextNodes:
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
    		if place in transition.nextNodes:
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
        pointer = pointer.nextNodes[-1]
