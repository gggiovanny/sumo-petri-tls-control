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
            raise ValueError('Error!', 'No se configuro un tipo de nodo') 
    def getName(self):
        return "{}{}".format(self.name_initial, self.id)
    def printName(self):
        print(self.getName(), '-> ', end='')
    def printNextNames(self):
        for node in self.nextNodes:
            print(node.getName())
    def addNext(self, node):
        if isinstance(node, self.listExpectedType):
            self.nextNodes.append(node)
        else:
            raise ValueError('Error de tipo de datos!', "No se puede agregar un {} a una lista que espera {}".format( node.__class__.__name__, self.listExpectedType.__name__) ) 

class Transition(Node):
    def __init__(self, id):
        Node.__init__(self, 't', id)
        self.preconditions = []
        self.waitTime = 15
        self.action = self.printName # default action
        
    def runAction(self):
        self.action()
    
class Place(Node):
    def __init__(self, id):
        Node.__init__(self, 'p', id)
        self.marks = 0

class PetriNetwork:
    def __init__(self, places_list, transitions_list, initial_state_list = []):
        self.p = places_list
        self.t = transitions_list
        self.configurePreconditions()
        self.setInitialState(initial_state_list)
        self.time_waited = 0
    def setInitialState(self, initial_state_list):
        if initial_state_list:
            if len(initial_state_list) == len(self.p):
                for i in range(len(self.p)):
                    self.p[i].marks = initial_state_list[i]
            else:
                raise ValueError('Error!', 'Error en el numero de elementos en initial_state_list: se esperaban {} elementos y se recibieron {}.'.format(len(self.p), len(initial_state_list))) 
    def configurePreconditions(self):
        for transition in self.t:
            for place in self.p:
                if transition in place.nextNodes:
                    transition.preconditions.append(place)
    def nextStep(self):
        # print(self.time_waited)
        for transition in self.t:
            all_conditions_marked = True
            if self.time_waited == 0: # solo checar las precondiciones si no se esta esperando ya, pues cuando ya se esta esperando quiere decir que ya se cumplieron en un ciclo previo
                for place in self.p:
                    if place in transition.preconditions and place.marks == 0: #! TODO: hacer que se puedan configurar multiples marcas
                        all_conditions_marked = False
            if all_conditions_marked:
                if self.time_waited == transition.waitTime:
                    transition.runAction()
                    self.time_waited = 0
                    # quitando las marcas de las precondiciones
                    for place in self.p:
                        if place in transition.preconditions:
                            place.marks = 0
                    # poniendoselas a los Place() siguientes
                    for place in self.p:
                        if place in transition.nextNodes:
                            place.marks = 0
        else:
            self.time_waited += 1

    def print(self, firstElements = True):
        pointer = self.p[0]
        for _ in range(len(self.p) + len(self.t)):
            print(pointer.getName(), '-> ', end='')
            if firstElements:
                pointer = pointer.nextNodes[0]
            else:
                pointer = pointer.nextNodes[-1]
    def printPreMatrix(self):
        # Generando la matriz PRE (condiciones que tiene que cumplir cada transicion para efectuarse)
        # Debe quedar con las transiciones en el eje horizontal y los lugares en el eje vertical:
        #   t0 t1 t2
        # p0 1  0  0 
        # p1 0  1  0 
        # p2 1  0  1 
        # De momento se genera con los ejes inversos y recorre diferente al imprimirlo en pantalla
        pre = []
        for transition in self.t:
            pre_col = []
            for place in self.p:
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
    def printPosMatrix(self):
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

if __name__ == "__main__":
    # Generando una lista de objetos Places() (Lugares) en una lista llamada 'p'
    p = []
    for i in range(6): # del 0 al 6
        p.append(Place(i)) # se le pasa i como argumento, que sera la id del Place()
    
    # Repitiendo el mismo proceso para generar los objetos tipo Transition() en la lista 't'
    t = []
    for i in range(5):
        t.append(Transition(i)) # se le pasa i como argumento, que sera la id del Transition()
    
    # Estableciendo las relaciones entre Places y Transitions
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
    
    initial_state = [1,0,0,1,0,0]
    petri = PetriNetwork(p, t, initial_state)
    # petri.printPreMatrix()
    # petri.printPosMatrix()
    
    for i in range(90):
        petri.nextStep()

    # for place in petri.p:
        # print(place.getName(), place.marks)