'''
    Project: Graph
    Description: Implementation of Graph Structure
    Name: Julio Cesar de Carvalho Barros
    Email: jccb2@cin.ufpe.br
'''
from Heap import *

class Vertice:
    def __init__(self,identifier):
        ''' Class constructor '''
        self.id = identifier
        self.c = 'white'
        self.pi = None
        self.d = float('inf')
        self.f = float('inf')
        
    def __str__(self):
        ''' Default string returns '''
        return '({v.id}) '\
               'd: {v.d}, '\
               'f: {v.f}, '\
               'c: {v.c}, '\
               'pi: {v.pi}'.format(v = self)

    def __repr__(self):
        ''' Default representation method '''
        return '{}'.format(self.id)

    def __eq__(self, other):
        ''' Returns comparison x == y '''
        return self.id == other.id

class Graph:
    def __init__(self,args=[],weighted=False,directed=False):
        ''' Class constructor '''
        self.adjacents = {}
        self.vertices = {}
        self.directed = directed
        self.weighted = weighted
        self.time = 0
        self.lenVertices = 0
        self.lenEdges = 0
        #Adds in constructor
        if type(args) == type([]):
            for arg in args:
                self.addVertice(arg[0])
                self.addVertice(arg[1])
                if self.weighted:
                    self.addEdge(arg[0],arg[1],arg[2])
                else:
                    self.addEdge(arg[0],arg[1])
        if type(args) == type({}):
            for vertice, adjacents in args.items():
                self.addVertice(vertice)
                self.adjacents[vertice] = adjacents
                self.lenEdges += len(adjacents)
                self.lenVertices += 1
                
    def __str__(self):
        ''' Default string returns '''
        result = 'List of Adjacency\n'
        for vertice, adjacents in self.adjacents.items():
            result += '{} : {}\n'.format(vertice, adjacents)
        return result

    def __repr__(self):
        ''' Default representation method '''
        return '{}'.format(self.adjacents)

    def print(self):
        for v in self.vertices.values():
            print('({v.id}) ' \
                  'd: {v.d}, ' \
                  'f: {v.f}, ' \
                  'c: {v.c}, ' \
                  'pi: {v.pi}'.format(v = v))
    
    def addVertice(self,identifier):
        ''' Add new vertice '''
        if not identifier in self.vertices:
            self.vertices[identifier] = Vertice(identifier)
            self.adjacents[identifier] = []
            self.lenVertices += 1

    def addEdge(self,origin,destiny,weight=None):
        ''' Add edge between two vertices '''
        if self.weighted:
            if not (destiny,weight) in self.adjacents[origin]:
                self.adjacents[origin].append((destiny,weight))
                self.lenEdges += 1
            if not self.directed:
                self.adjacents[destiny].append((origin,weight))
                self.lenEdges += 1
        else:
            if not (destiny,weight) in self.adjacents[origin]:
                self.adjacents[origin].append(destiny)
                self.lenEdges += 1
            if not self.directed:
                self.adjacents[destiny].append(origin)
                self.lenEdges += 1
    
    def remVertice(self,identifier):
        ''' Rem vertice by identifier '''
        if identifier in self.vertices:
            del self.vertices[identifier]
            del self.adjacents[identifier]
            self.lenVertices -= 1
            for vertice in self.adjacents.values():
                i = 0
                while i < len(vertice):
                    if (self.weighted and vertice[i][0] == identifier) or (vertice[i] == identifier):
                        del vertice[i]
                    else:
                        i += 1
    
    def remEdge(self,origin,destiny,weight=None):
        ''' Rem edge by origin, destiny and weight '''
        i = 0
        while i < len(self.adjacents[origin]):
            if (self.weighted and self.adjacents[origin][i] == (destiny, weight)) or (self.adjacents[origin][i] == destiny):
                del self.adjacents[origin][i]
                self.lenEdges -= 1
            else:
                i += 1
        if not self.directed:
            i = 0
            while i < len(self.adjacents[destiny]):
                if (self.weighted and self.adjacents[destiny][i] == (origin, weight)) or (self.adjacents[destiny][i] == origin):
                    del self.adjacents[destiny][i]
                    self.lenEdges -= 1
                else:
                    i += 1

    def isLinked(self,identifier1,identifier2):
        ''' Returns if two vertices is linked '''
        linked = False
        i = 0
        while i < len(self.adjacents[identifier1]) and not linked:
            if (self.weighted and self.adjacents[identifier1][i][0] == identifier2) or (self.adjacents[identifier1][i] == identifier2):
                linked = True
            else:
                i+= 1
        return linked

    def getInputDegree(self,identifier):
        ''' Return input degree '''
        count = 0
        for vertice in self.adjacents.values():
            for edge in vertice:
                if (self.weighted and edge[0] == identifier) or edge == identifier:
                    count += 1
        return count

    def getOutputDegree(self,identifier):
        ''' Return output degree '''
        return len(self.adjacents[identifier])

    def getDegree(self,identifier):
        ''' Return degree '''
        if self.directed:
            return self.getInputDegree(identifier) + self.getOutputDegree(identifier)
        else:
            return self.getOutputDegree(identifier)

    def getAdjacents(self,vertice):
        ''' Return adjacents vertices'''
        return self.adjacents[vertice]
    
    def getSmallerEdge(self):
        ''' Return smallest weighteds edge '''
        weight = float('inf')
        smallers = []
        if self.weighted:
            for vertice, adjacents in self.adjacents.items():
                for edge in adjacents:
                    origin = self.vertices[vertice]
                    destiny = self.vertices[edge[0]]
                    if edge[1] == weight:
                        smallers.append((origin,destiny,edge[1]))
                    elif edge[1] < weight:
                        weight = edge[1]
                        smallers = [(origin,destiny,edge[1])]
            return smallers
        
    def getHigherEdge(self):
        ''' Return highest weighted edges '''
        weight = 0
        highers = []
        if self.weighted:
            for vertice, adjacents in self.adjacents.items():
                for edge in adjacents:
                    origin = self.vertices[vertice]
                    destiny = self.vertices[edge[0]]
                    if edge[1] == weight:
                        highers.append((origin,destiny,edge[1]))
                    elif edge[1] > weight:
                        weight = edge[1]
                        highers = [(origin,destiny,edge[1])]
            return highers

    def widthSearch(self,identifier):
        ''' Search for width in graph '''
        for v in self.vertices.values():
            v.c = 'white'
            v.d = float('inf')
            v.pi = None
        s = self.vertices[identifier]
        s.c = 'gray'
        s.d = 0
        s.pi = None
        Q = [s]
        while len(Q) > 0:
            u = Q.pop(0)
            for key in self.getAdjacents(u.id):
                v = self.vertices[key[0] if self.weighted else key]
                if v.c == 'white':
                    v.c = 'gray'
                    v.d = u.d + 1
                    v.pi = u.id
                    Q.append(v)
            u.c = 'black'

    def deepSearch(self):
        ''' Search for deep in graph and returns topological order'''
        L = []
        for v in self.vertices.values():
            v.c = 'white'
            v.pi = None
            v.d = float('inf')
            v.f = float('inf')
        self.time = 0
        for v in self.vertices.values():
            if v.c == 'white':
                self.__deepSearch(v, L)
        return L
                  
    def __deepSearch(self,u,L=[]):
        ''' Aux method for deepSearch'''
        self.time += 1
        u.d = self.time
        u.c = 'gray'
        for key in self.getAdjacents(u.id):
            v = self.vertices[key[0] if self.weighted else key]
            if v.c == 'white':
                v.pi = u.id
                self.__deepSearch(v,L)
        u.c = 'black'
        self.time += 1
        u.f = self.time
        L.insert(0,u.id)

    def getAllEdges(self):
        ''' Return all edges ordered by heapSort'''
        E = []
        for v in self.vertices.values():
            heapSort(self.getAdjacents(v.id),1)
            for e in self.getAdjacents(v.id):
                edge = (v.id,e[0],e[1]) if self.weighted else (v.id,e)
                if not edge in E:
                    E.append(edge)
        heapSort(E, 2)
        return E
        
    def kruskal(self):
        ''' Returns the minimum generating tree by the kruskal '''
        F = {}
        for v in self.vertices.values():
            v.c = 'white'
            v.pi = v.id
            v.d = float('inf')
            v.f = float('inf')
            F[v.pi] = set()
        Q = self.getAllEdges()
        A = []
        i = 0
        while len(Q) != 0 and i != len(self.vertices) - 1:
            u = Q.pop(0)
            if self.vertices[u[0]].pi != self.vertices[u[1]].pi:
                if self.vertices[u[0]].c == 'white' and self.vertices[u[1]].c == 'white':
                    self.vertices[u[0]].c = 'black'
                    self.vertices[u[1]].c = 'black'
                    self.vertices[u[0]].pi = u[0]
                    self.vertices[u[1]].pi = u[0]
                    F[u[0]].add(u[0])
                    F[u[0]].add(u[1])
                    A.append(u)
                    i += 1
                elif self.vertices[u[0]].c == 'white' and self.vertices[u[1]].c == 'black':
                    self.vertices[u[0]].c = 'black'
                    self.vertices[u[0]].pi = self.vertices[u[1]].pi
                    F[u[1]].add(u[0])
                    A.append(u)
                    i += 1
                elif self.vertices[u[0]].c == 'black' and self.vertices[u[1]].c == 'white':
                    self.vertices[u[1]].c = 'black'
                    self.vertices[u[1]].pi = self.vertices[u[0]].pi
                    F[u[0]].add(u[1])
                    A.append(u)
                    i += 1
                elif self.vertices[u[0]].c == 'black' and self.vertices[u[1]].c == 'black':
                    for v in F[u[1]]:
                        self.vertices[v].pi = self.vertices[u[0]].pi
                    A.append(u)
                    i += 1
        return A
    
    def prim(self,identifier):
        ''' Returns the minimum generating tree by the prim '''
        for v in self.vertices.values():
            v.c = 'white'
            v.pi = None
            v.d = float('inf')
            v.f = float('inf')
        self.vertices[identifier].d = 0     
        H = Heap([],True,True)
        for v in self.getAdjacents(identifier):
            edge = (identifier,) + v
            H.insert(HeapItem(edge[2], edge))
        while len(H) != 0:
            u = H.extract()
            dist = u[2]
            if dist < self.vertices[u[1]].d:
                self.vertices[u[1]].pi = u[0]
                self.vertices[u[1]].d = dist
                for v in self.getAdjacents(u[1]):
                    edge = (u[1],) + v
                    H.insert(HeapItem(edge[2], edge))
        P = []
        for v in self.vertices.values():
            if v.id != identifier:
                edge = (v.id,v.pi,v.d)
                P.append(edge)
        return P
    
            
    def dijkstra(self,identifier):
        ''' Calculates the smallest distance to a vertex starting from the vertex param '''
        for v in self.vertices.values():
            v.c = 'white'
            v.pi = None
            v.d = float('inf')
            v.f = float('inf')
        self.vertices[identifier].d = 0     
        H = Heap([],True,True)
        for v in self.getAdjacents(identifier):
            edge = (identifier,) + v
            H.insert(HeapItem(edge[2], edge))
        while len(H) != 0:
            u = H.extract()
            dist = u[2] if self.vertices[u[0]].pi is None else self.vertices[u[0]].d + u[2]
            if dist < self.vertices[u[1]].d:
                self.vertices[u[1]].pi = u[0]
                self.vertices[u[1]].d = dist
                for v in self.getAdjacents(u[1]):
                    edge = (u[1],) + v
                    H.insert(HeapItem(edge[2], edge))
                         
'''
    Debugger
'''
def printTitle(string):
    print('=' * 40 + '\n' + '{:^40}'.format(string) + '\n' + '=' * 40)

if __name__ == '__main__':
    g = Graph([('v','r',2),('r','s',4),('s','w',3),('w','t',6),('w','x',2),('t','x',4),('t','u',1),('x','u',3),('x','y',2),('u','y',4)],True,False)
    printTitle('GRAPH')
    print(
    '        (r)-4-(s)   (t)-1-(u)\n' \
    '         |     |   / |   / | \n' \
    '         2     3  6  4  3  4 \n' \
    '         |     | /   | /   | \n' \
    '        (v)   (w)-2-(x)-2-(y)\n' )
    print('Width Search')
    g.widthSearch('s')
    g.print()
    
    g = Graph([('u','v'),('x','u'),('v','y'),('w','y'),('w','z'),('z','y'),('z','z')],False,True)
    printTitle('GRAPH')
    print(
    '            (u)→(v) (w)\n' \
    '             ↑   ↓ ↙ ↓ \n' \
    '            (x) (y)←(z)\n' \
    '                     ↺\n' )
    print('Deep Search')
    g.deepSearch()
    g.print()

    g = Graph([(0,1),(0,2),(0,3),(1,3),(1,5),(1,6),(2,6),(3,5),(6,7),(4,7)],False,True)
    printTitle('GRAPH')
    print(
    '            (0)→(2)→(6)←(4) \n' \
    '             ↓ ↘  ↗ ↓ ↙    \n' \
    '            (3)←(1) (7)     \n' \
    '             ↓ ↙            \n' \
    '            (5)             \n ' )
    print('Topological Order')
    print(g.deepSearch())
    
    g = Graph([(0,2,9),(0,4,5),(0,3,1),(1,2,2),(1,3,2),(1,4,2),(2,4,3),(3,4,2)],True)
    print('=' * 40 + '\n' + '{:^40}'.format('GRAPH') + '\n' + '=' * 40)
    print(
    '             (0)---9---(2)\n' \
    '              | \\5   3/ | \n' \
    '              1  >(4)<  2 \n' \
    '              | /2   2\ | \n' \
    '             (3)---2---(1)\n' )
    print('Prim')
    print(g.prim(0))
    print('Kruskal')
    print(g.kruskal())
    print('Dijkstra')
    g.dijkstra(0)
    g.print()
