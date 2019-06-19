'''
    Project: Tic Tac Toe
    Description: Implementation of Tic Tac Toe
    Authors: Julio Cesar de Carvalho Barros (jccb2@cin.ufpe.br)
             Guilherme Guerra Campos (ggc3@cin.ufpe.br)
'''
from Graph import Graph
from Persistence import importGraph, exportGraph
import os, time, random

def clearTerminal():
    ''' Clears the characters in the terminal '''
    os.system('cls' if os.name == 'nt' else 'clear')

def inputValidInt(label):
    ''' Captures entries of valid integers '''
    try:
        result = int(input(label))
    except (KeyboardInterrupt, SystemExit):
        menu('Game interrupted!')
    except:
        result = False
    return result

def board2String(board):
    ''' Converts board in string '''
    result = ''
    for slot in board:
        result += '_' if slot == ' ' else slot
    return result

def string2Board(string):
    ''' Converts board in string '''
    result = []
    for char in string:
        result.append(' ' if char == '_' else char)
    return result

def printBoard(board):
    ''' Prints board'''
    result = '=============\n' \
             ' TIC TAC TOE \n' \
             '=============\n'
    i = 0
    for slot in board:
        result += ' [%s]' % slot
        i += 1
        result += '\n' if i % 3 == 0 else ''
    print(result)

def checkWinner(board):
    ''' Checks if any of the players won and returns boolean equivalent '''
    for i in range(3):
        col = (board[0 + i] == board[3 + i] == board[6 + i]) and board[0 + i] != ' '
        row = (board[0 + i*3] == board[1 + i*3] == board[2 + i*3]) and board[0 + i*3] != ' '
        ver = (board[0] == board[4] == board[8] or board[2] == board[4] == board[6]) and board[4] != ' '
        if(col or row or ver):
            return True
    return False

def startGame(mode=1,game_tree=Graph(), avaliable=[0,1,2,3,4,5,6,7,8]):
    ''' Initialize a new game and routines involved '''
    def verify(board, current, game_tree, enemy=False):
        board_weight = float('inf')
        if board in game_tree.vertices:
            watcher = game_tree.vertices[board]
            if not watcher.pi is None:
                board_weight = 0
                while not watcher.pi is None and watcher.pi != current:
                    #print(board, current, watcher)
                    board_weight += 1
                    if enemy and game_tree.vertices[watcher.pi].pi == current:
                        break
                    watcher = game_tree.vertices[watcher.pi]
                i = 0
                while i < 9:
                    if watcher.id[i] != current[i] and current[i] == '_' and watcher.id[i] == board[0]:
                        return board_weight, i
                    i += 1
        return board_weight, None
    
    def computerTurn(game_tree, board, avaliable, count):
        ''' Computer Turn '''
        if len(avaliable) == 9:
            print('RANDOM CHOICE')
            pos = random.choice(avaliable)
            return pos
        
        current = board2String(board);
        game_tree.dijkstra(current)
        #Symbol and Enemy set
        symbol = ('x' if count % 2 == 0 else 'o') * 9
        enemy = ('o' if count % 2 == 0 else 'x') * 9
        
        #Symbol verify
        symbol_weight, symbol_pos = verify(symbol, current, game_tree)
                    
        #Enemy verify
        enemy_weight, enemy_pos = verify(enemy, current, game_tree, True)
        
        #Draw verify
        draw_weight, draw_pos = verify('-' * 9, current, game_tree)
   
        #print('Symbol:', symbol_pos, 'Weight:', symbol_weight)
        #print('Enemy:', enemy_pos, 'Weight:', enemy_weight)
        #print('Draw:', draw_pos, 'Weight:', draw_weight)
        
        if symbol_weight != float('inf') or enemy_weight != float('inf'):
            if (enemy_weight < symbol_weight):
                #print('ENEMY CHOICE')
                return enemy_pos
            else:
                #print('SYMBOL CHOICE')
                return symbol_pos
        else:
            #print('RANDOM CHOICE')
            pos = random.choice(avaliable)
            return pos
    
    board = [' ', ' ', ' ',' ', ' ', ' ',' ', ' ', ' ']
    endgame = False
    count = 0
    message = ''
    
    while count <= 10:
        clearTerminal()
        printBoard(board)
        print(message)

        if endgame:
            time.sleep(5)
            return game_tree
        else:
            if count < 9:
                #Turn set
                if count % 2 == 0:
                    print('Player X is your turn!')
                else:
                    print('Player O is your turn!')
                if mode == 1 or (mode == 2 and count % 2 == 0) or (mode == 3 and count % 2 != 0):
                    pos = inputValidInt('Input a position (1~9): ') - 1
                elif mode == 4 or (mode == 2 and count % 2 != 0) or (mode == 3 and count % 2 == 0):
                    pos = computerTurn(game_tree, board, avaliable, count)
                    
                #Computing    
                if(0 <= pos < 9):
                    if(board[pos] == ' '):
                        after = board2String(board)
                        if(count % 2 == 0):
                            board[pos] = 'x'
                        else:
                            board[pos] = 'o'
                        avaliable.remove(pos)
                        count += 1
                        before = board2String(board)

                        #Manual learning
                        game_tree.addVertice(after)
                        game_tree.addVertice(before)
                        game_tree.addEdge(after,before,1)
                        
                        #Verify
                        if checkWinner(board):
                            if (count - 1) % 2 == 0:
                                message = 'Player X won!'
                                #Learning X win
                                game_tree.addVertice('xxxxxxxxx')
                                game_tree.addEdge(before,'xxxxxxxxx',1)
                            else:
                                message = 'Player O won!'
                                #Learning O win
                                game_tree.addVertice('ooooooooo')
                                game_tree.addEdge(before,'ooooooooo',1)
                            endgame = True
                    else:
                        message = 'Already have an piece here!'
                else:
                    message = 'Invalid position!'
            else:
                message = 'Game Over!'
                endgame = True
                #Learning Draw
                before = board2String(board)
                game_tree.addEdge(before,'---------',1)


def deepSearch(graph,Q=[]):
    ''' Search for deep in graph and returns topological order'''
    def seePossibilites(board, graph):
        ''' Add edges to other possibilites '''
        clearTerminal()
        printBoard(board)
        print('Vertices: ', graph.lenVertices,'\tEdges:', graph.lenEdges)
        current = board2String(board)
        if not checkWinner(board):
            if current.count('_') != 0:
                for i in range(len(board)):
                    if board[i] == ' ':
                        board_next = board[:]
                        board_next[i] = 'x' if current.count('x') == current.count('o') else 'o'
                        played = board2String(board_next)
                        graph.addVertice(current)
                        graph.addVertice(played)
                        graph.addEdge(current,played,1)
            else:
                graph.addVertice('-'*9)
                graph.addEdge(current,'-'*9,1)
        elif not(current == 'x'*9 or current == 'o'*9 or current == '-'*9):
            if current.count('x') != current.count('o'):
                graph.addVertice('x'*9)
                graph.addEdge(current,'x'*9,1)
            else:
                graph.addVertice('o'*9)
                graph.addEdge(current,'o'*9,1)
        exportGraph(graph, 'game-tree-tictactoe.txt')
        
    def deepSearchEx(graph,u):
        ''' Aux method for deepSearch'''
        graph.time += 1
        u.d = graph.time
        u.c = 'gray'
        #
        board = string2Board(u.id)
        seePossibilites(board, graph)
        # 
        for key in graph.getAdjacents(u.id):
            v = graph.vertices[key[0] if graph.weighted else key]
            if v.c == 'white':
                v.pi = u.id
                deepSearchEx(graph,v)
        u.c = 'black'
        graph.time += 1
        u.f = graph.time
                
    #Main
    for v in graph.vertices.values():
        v.c = 'white'
        v.pi = None
        v.d = float('inf')
        v.f = float('inf')
    graph.time = 1
    L = []
    board = [' '] * 9
    seePossibilites(board, graph)
    for key, weight in graph.getAdjacents('_'*9):
        v = graph.vertices[key]
        if v.c == 'white':
            deepSearchEx(graph,v)

def menu(game_tree=None, message=''):
    ''' Display the game menu'''
    if game_tree is None:
        game_tree = importGraph('game-tree-tictactoe.txt')
    clearTerminal()
    print('=============\n' \
          ' TIC TAC TOE \n' \
          '=============\n'\
          '1 - Play P2P\n' \
          '2 - Play P2C\n' \
          '3 - Play C2P\n' \
          '4 - Play C2C\n' \
          '5 - Game Tree Gen\n' \
          '6 - Exit' \
          + message)
    print('Vertices: ', game_tree.lenVertices,'\tEdges:', game_tree.lenEdges)
    option = inputValidInt('Input a option: ')
    clearTerminal()
    if  0 < option < 4:
        game_tree = startGame(option, game_tree,[0,1,2,3,4,5,6,7,8])
    elif option == 4:
        number = inputValidInt('Repeat how many times? ')
        for i in range(number):
            game_tree = startGame(option, game_tree,[0,1,2,3,4,5,6,7,8])
    elif option == 5:
        deepSearch(game_tree)
    elif option == 6:
        exportGraph(game_tree, 'game-tree-tictactoe.txt')
        exit()
    menu(game_tree)

if __name__ == '__main__':
    menu()
