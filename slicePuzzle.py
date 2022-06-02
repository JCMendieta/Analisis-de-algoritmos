#JUAN CAMILO MENDIETA HERNANDEZ
#SAMY FELIPE CUESTAS MERCHAN
#CAMILO HERNANDEZ GUERRERO
import numpy
from itertools import permutations
import random
from copy import deepcopy
import math
import time

def gameWon(table, tableWon, n):
    result = True
    for row in range (n):
        for column in range(n):
            if table[row][column] != tableWon[row][column]:
                result = False
    return result

def moveUp(table, blankSpace):
    print("MOVES UP")
    if blankSpace[0] != 0 :
        aux = table[blankSpace[0]-1][blankSpace[1]]
        table [blankSpace[0]-1][blankSpace[1]] = " "
        table [blankSpace[0]][blankSpace[1]] = aux
        blankSpace = (blankSpace[0] - 1, blankSpace[1])
        return blankSpace
    else:
        print("No puede moverse arriba")
        return blankSpace

def moveDown(table, blankSpace):
    print("MOVES DOWN")
    print(blankSpace)
    if blankSpace[0] < len(table[0]) - 1:
        aux = table[blankSpace[0] + 1][blankSpace[1]]
        table [blankSpace[0] + 1][blankSpace[1]] = " "
        table [blankSpace[0]][blankSpace[1]] = aux
        blankSpace = (blankSpace[0] + 1, blankSpace[1])
        print(blankSpace)
        return blankSpace
    else :
        print("No puede moverse abajo")
        return blankSpace

def moveLeft(table, blankSpace):
    print("MOVES LEFT")
    if blankSpace[1] > 0:
        aux = table[blankSpace[0]][blankSpace[1]-1]
        table [blankSpace[0]][blankSpace[1]-1] = " "
        table [blankSpace[0]][blankSpace[1]] = aux
        blankSpace = (blankSpace[0] , blankSpace[1] - 1)
        return blankSpace
    else :
        print("No puede moverse a la izquierda")
        return blankSpace

def moveRight(table, blankSpace):
    print("MOVES RIGHT")
    if blankSpace[1] < len(table[0]) - 1:
        aux = table[blankSpace[0] ][blankSpace[1] + 1]
        table [blankSpace[0] ][blankSpace[1] + 1] = " "
        table [blankSpace[0]][blankSpace[1]] = aux
        blankSpace = (blankSpace[0] , blankSpace[1] + 1)
        return blankSpace
    else :
        print("No puede moverse a la derecha")
        return blankSpace

class Node:
    def __init__(self, currentPuzzleTable, previousPuzzleTable, numberOfMoves, distance, direction):
        self.currentPuzzleTable = currentPuzzleTable
        self.previousPuzzleTable = previousPuzzleTable
        self.numberOfMoves = numberOfMoves
        self.distance = distance
        self.direction = direction

    def euristic(self):
        return self.numberOfMoves + self.distance
    
    
def getElementPosition(currentPuzzleTable, element):
    n = len(currentPuzzleTable)
    for i in range(n):
        if element in currentPuzzleTable[i]:
            return (i, currentPuzzleTable[i].index(element))

def tableEuclidianDistance(currentPuzzleTable, tableWon):
    tableDistance = 0
    n = len(currentPuzzleTable)
    for i in range(n):
        for j in range(n):
            positionTableWon = getElementPosition(tableWon, currentPuzzleTable[i][j])
            tableDistance += abs(i - positionTableWon[0]) + abs(j - positionTableWon[1])
    return tableDistance


def getPossibleMoves(node, currentPuzzleTable, tableWon):
    listOfMoves = []
    blankCoordinates = getElementPosition(node.currentPuzzleTable, " ")

    sizeCurrentPuzzle = len(currentPuzzleTable)  

    #UP
    newPosition = (blankCoordinates[0] - 1, blankCoordinates[1])
    if 0 <= newPosition[0] < sizeCurrentPuzzle and 0 <= newPosition[1] < sizeCurrentPuzzle:
        newPuzzleTable = deepcopy(node.currentPuzzleTable)
        newPuzzleTable[blankCoordinates[0]][blankCoordinates[1]] = node.currentPuzzleTable[newPosition[0]][newPosition[1]] 
        newPuzzleTable[newPosition[0]][newPosition[1]] = " "
        listOfMoves.append(Node(newPuzzleTable, node.currentPuzzleTable, node.numberOfMoves + 1, tableEuclidianDistance(currentPuzzleTable, tableWon),"U"))
    
    
    #DOWN
    newPosition = (blankCoordinates[0] + 1, blankCoordinates[1])
    if 0 <= newPosition[0] < sizeCurrentPuzzle and 0 <= newPosition[1] < sizeCurrentPuzzle:
        newPuzzleTable = deepcopy(node.currentPuzzleTable)
        newPuzzleTable[blankCoordinates[0]][blankCoordinates[1]] = node.currentPuzzleTable[newPosition[0]][newPosition[1]] 
        newPuzzleTable[newPosition[0]][newPosition[1]] = " "
        listOfMoves.append(Node(newPuzzleTable, node.currentPuzzleTable, node.numberOfMoves + 1, tableEuclidianDistance(currentPuzzleTable, tableWon),"D"))
    
    #RIGHT
    newPosition = (blankCoordinates[0] , blankCoordinates[1] + 1)
    if 0 <= newPosition[0] < sizeCurrentPuzzle and 0 <= newPosition[1] < sizeCurrentPuzzle:
        newPuzzleTable = deepcopy(node.currentPuzzleTable)
        newPuzzleTable[blankCoordinates[0]][blankCoordinates[1]] = node.currentPuzzleTable[newPosition[0]][newPosition[1]] 
        newPuzzleTable[newPosition[0]][newPosition[1]] = " "
        listOfMoves.append(Node(newPuzzleTable, node.currentPuzzleTable, node.numberOfMoves + 1, tableEuclidianDistance(currentPuzzleTable, tableWon),"R"))
    
    #LEFT
    newPosition = (blankCoordinates[0] , blankCoordinates[1] - 1)
    if 0 <= newPosition[0] < sizeCurrentPuzzle and 0 <= newPosition[1] < sizeCurrentPuzzle:
        newPuzzleTable = deepcopy(node.currentPuzzleTable)
        newPuzzleTable[blankCoordinates[0]][blankCoordinates[1]] = node.currentPuzzleTable[newPosition[0]][newPosition[1]] 
        newPuzzleTable[newPosition[0]][newPosition[1]] = " "
        listOfMoves.append(Node(newPuzzleTable, node.currentPuzzleTable, node.numberOfMoves + 1, tableEuclidianDistance(currentPuzzleTable, tableWon),"L"))
    
    return listOfMoves


#BEST EURISTIC YA FUNCIONA
def getBestNode(dictionaryOfNodes):
    i = 0
    bestEuristic = math.inf
    for node in dictionaryOfNodes.values():
        if i == 0 or node.euristic() < bestEuristic:
            i += i + 1
            bestNode = node
            bestEuristic = bestNode.euristic()
    return bestNode


def movement(actualTable, tableWon):  
    
    moves = {str(actualTable): Node(actualTable, actualTable, 0, tableEuclidianDistance(actualTable, tableWon), "")}
    movesToWin = {}
  
    while True:
        
        
        testMove = getBestNode(moves)
       # print("TABLA GANADORA")
       # print(tableWon) #BIEN
       # print("MEJOR TABLA SELECCIONADA")
       # print(testMove.PuzzleTable) #INICIAL    
        
        movesToWin[str(testMove.currentPuzzleTable)] = testMove


        #YA ENTRA A LA CONDICION
        if testMove.currentPuzzleTable == tableWon:         
            auxNode = movesToWin[str(tableWon)]
            auxMoves = list()
            while auxNode.direction:
                auxMoves.append({
                        "direction":auxNode.direction,
                        "node":auxNode.currentPuzzleTable
                    })
                auxNode = movesToWin[str(auxNode.previousPuzzleTable)]
            auxMoves.reverse()
            return auxMoves
        
        possibleMoves = getPossibleMoves(testMove,actualTable, tableWon)
        #print("NODOS ADYACENTES:") #INICIALMENTE BIEN
        #for node in adj_node:
        #    print(node.currentPuzzleTable)

        for node in possibleMoves:
            if str(node.currentPuzzleTable) in movesToWin.keys() or str(node.currentPuzzleTable) in moves.keys() and moves[
                str(node.currentPuzzleTable)].euristic() < node.euristic():
                continue
            moves[str(node.currentPuzzleTable)] = node

        del moves[str(testMove.currentPuzzleTable)]
        
       
        #print("NUEVO______________________")
        #time.sleep(2)


def slicePuzzle ():
    
    ni = input("ingresar tam de los tableros:")
    n=int(ni)
    randomPuzzle = []
    puzzle = []
    puzzleWon = []
    numbersInOrder = range(n*n)
    numbersWithOutOrder = random.sample(range(n*n), n*n)
    #print(numbersInOrder)
    #print(numbersWithOutOrder)
    

    #filling matrix to play

    i = 0
    for numberA in range(n):
        aux = []
        for numberB in range(n):
            if(numbersWithOutOrder[i] != (n*n)-1 ):
                aux.append(str(numbersWithOutOrder[i]))
            else:
                aux.append(" ")
                blank = (numberA, numberB)
            i += 1
        randomPuzzle.append(aux)

    #filling matriz to win 
    i = 0
    for numberA in range(n):
        aux = []
        for numberB in range(n):
            if(numbersInOrder[i] != (n*n)-1 ):
                aux.append(str(numbersInOrder[i]))
            else:
                aux.append(" ")
            i += 1
        puzzleWon.append(aux)


    puzzle=[["5", "1", "7"],
            ["3", "6", "0"],
            [" ", "2", "4"]] #24 movimientos // 10:10
    
    puzzle2=[["0", "1", "2"],
             [" ", "4", "5"],
             ["3", "6", "7"]] #3 movs // Rapido 
    
    puzzle3 =[["2", "5", "4"],
              ["3", " ", "1"],
              ["6", "7", "0"]] #20 movs // Lo resuelve en 2:48
    
    puzzle4=[["1", "5", "6"],
             ["0", " ", "7"],
             ["4", "2", "3"]] # 18 movs // 0:32
    
   
    puzzle5 = [["4", " ", "1","3"],  #13 movs // 0:47
               ["8", "0", "2", "7"], #Inicializar n en 4
               ["12", "5", "6", "11"],
               ["13", "9", "10", "14"]]
    
    puzzle6=[["4", "1", " "],
             ["0", "6", "2"],
             ["7", "3", "5"]] # 12 movs // rapido
    
    puzzle7=[["3", "7", "0"],
             ["6", "4", "1"],
             [" ", "5", "2"]] # 14 movs // rapido
    
    puzzle8=[["1", "3", " "],
             ["2", "6", "0"],
             ["5", "4", "7"]] # 22 movs // 4:30
    
    print("Slice Puzzle")
    print("Para indicar que pieza mover en el espacio vacio ingresar U, D, L, R")
    print("U: El espacio vacio intercambia con su posicion con el elemento en el espacio de arriba. ")
    print("D: El espacio vacio intercambia con su posicion con el elemento en el espacio de abajo.")
    print("L: El espacio vacio intercambia con su posicion con el elemento en el espacio de la izquierda.")
    print("R: El espacio vacio intercambia con su posicion con el elemento en el espacio de la derecha.")
    
    
    blank = (0,0)
    entrada = input("1)Jugar manualmente\nResolver puzzles con algoritmo pueden tomar un tiempo\n2)Puzzle1 tarda 4 minutos 30 segundos.\n3)Puzzle2 rapido\n4)Puzzle3 tarda 2 minutos 48 segundos.\n5)Puzzle4 tarda 32 segundos.\n6)Puzzle5 tarda 47 segundos\n7)Puzzle6 rapido\n8)Puzzle7 rapido\n9)Puzzle aleatorio en la mayoria de casos va a tomar bastante tiempo\n ")
    print(entrada)
    if (entrada == "1"):
        puzzle = randomPuzzle
        blank=getElementPosition(puzzle, " ")
        print(numpy.matrix(puzzle))
        print("--------------------")
        while(gameWon(puzzle, puzzleWon, n) == False):
            print(" Donde se quiere mover")
            command = input()
            if command == "U":
                blank = moveUp(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "D":
                blank = moveDown(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "L":
                blank = moveLeft(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "R":
                blank = moveRight(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            else:
                print("No se puede")
    else:
        if(entrada == '2'):
            puzzle = puzzle8
        elif(entrada == '3'):
            puzzle = puzzle2
        elif(entrada == '4'):
            puzzle = puzzle3
        elif(entrada == '5'):
            puzzle = puzzle4
        elif(entrada == '6'):
            puzzle = puzzle5
        elif(entrada == '7'):
            puzzle = puzzle6
        elif(entrada == '8'):
            puzzle = puzzle7
        elif(entrada == '9'):
            puzzle = randomPuzzle
        blank=getElementPosition(puzzle, " ")
        print(numpy.matrix(puzzle))
        print("--------------------")
        movimientos = movement(puzzle, puzzleWon)
        #print(movimientos)
        turn = 0;
        while(gameWon(puzzle, puzzleWon, n) == False):
            command = movimientos[turn]["direction"]
            turn=turn+1
            print(command)
            if command == "U":
                blank = moveUp(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "D":
                blank = moveDown(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "L":
                blank = moveLeft(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            elif command == "R":
                blank = moveRight(puzzle,blank)
                print(numpy.matrix(puzzle))
                print("----------------")
            else:
                print("No se puede")
        print("Total movements:")
        print (turn)
    

    

slicePuzzle()