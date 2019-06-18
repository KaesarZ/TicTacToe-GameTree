'''
    Project: Persistence
    Description: Implementation of persistence routines
    Authors: Julio Cesar de Carvalho Barros (jccb2@cin.ufpe.br)
             Guilherme Guerra Campos (ggc3@cin.ufpe.br)
'''
from Graph import Graph

def data2Graph(data):
    ''' Converts data to graph '''
    array = []
    edge = ()
    attr = ''
    for char in data:
        if char == '\n':
            edge += (int(attr),)
            array.append(edge)
            edge = ()
            attr = ''
        elif char == '\t':
            edge += (attr,)
            attr = ''
        else:
            attr += char
    return Graph(array, True, True)
    

def graph2Data(graph):
    ''' Converts graph to data '''
    data = ''
    for vertice, adjacents in graph.adjacents.items():
        for attr in adjacents:
            data += '%s' %  vertice
            if type(attr) == type(tuple()):
                for i in attr:
                    data += '\t%s' % i
            else:
                data += '\t%s' % attr
            data += '\n'
    return data

def importGraph(file='game-tree.txt'):
    ''' Import data from file path '''
    try:
        file = open(file, 'r')
        data = file.read()
        file.close()
        return data2Graph(data)
    except:
        print('Error: cannot be import data to {}!'.format(file))
        return Graph([], True, True)

def exportGraph(graph, file='game-tree.txt'):
    ''' Export data from file path '''
    data = graph2Data(graph)
    try:
        file = open(file, 'w')
        file.write(data)
        file.close()
    except:
        print('Error: cannot be export data to {}!'.format(file)) 
