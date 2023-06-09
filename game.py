import pygame
import sys
from pygame.locals import *
import random
import time
from threading import Timer
import grafo as gf
import GrafoDic as gd

# Configurações do tabuleiro
square_size = 50
square_margin = 3
board_width = 8 * square_size + 9 * square_margin
board_height = 8 * square_size + 9 * square_margin
rows = 15
columns = 15
size = width, height = ((square_size + square_margin)
                        * rows, (square_size + square_margin)*columns)
# grafo para apartir do tabuleiro
graph = gf.Graph(rows*columns)
end = [int(i) for i in range(0, 14)]

#grafo com dicionario de adjacencia e pesos nas arestas
graphDic = gd.Graph(columns*rows)

# cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
gray = (128, 128, 128)
yellow = (255, 255, 30)
blue = (0, 0, 255)
pink = (255, 20, 147)
orange = (223, 118, 2)
lightOrange = (255, 195, 128)
lightBlue = '#5dc9ee'
secondary_pink = '#ff799b'
ciano = (0, 255, 255)

#macros dos quadrados
playerSquare = 10
finishBlue = 11
finishWhite = 12
startingLine = 6
hole = 7
deactivatedHole = 0
solidSquare = 1
waterSquare = 3
sandSquare = 2
trailSquare = 4
fireSquare = 5


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('TIP TOE') 
pygame.draw.rect(screen, green, (0, 0, width, height), 5)

# cria tabuleiro
def createBoard(row, column):

    board = []
    for i in range(row):
        board.append([])
        for j in range(column):
            board[i].append(solidSquare)
            if i>1:
                if i==2 and j%2 == 0:
                    board[i][j] = deactivatedHole
                elif i==4 and j%2 != 0:
                    board[i][j] = deactivatedHole
            if i < 2:  # duas primeiras linhas, que sao a linha de chegada
                board[i][j] = finishBlue
                if i == 0 and j % 2 == 0:
                    board[i][j] = finishWhite
                elif i == 1 and j % 2 != 0:
                    board[i][j] = finishWhite
            elif i == (row-1):
                board[i][j] = startingLine

    # cria obstaculos
    sort = [deactivatedHole, sandSquare, waterSquare, fireSquare]
    for i in range(4,rows-2):
        for j in range(0,columns-1):
            if board[i][j] == solidSquare:
                if random.randint(0,30) <10:
                    board[i][j] = random.choice(sort)
    

    return board

# Cria quadrado
def drawSquare(row, column, color):
    x = column * (square_size + square_margin) + square_margin
    y = row * (square_size + square_margin) + square_margin
    rect = pygame.Rect(x, y, square_size, square_size)
    pygame.draw.rect(screen, color, rect)


def centralizeImage(x,y):
    return (x * (square_size + square_margin) + square_margin + square_size/2, y * (square_size + square_margin) + square_margin + square_size/2)

def startPosition():
    return (random.randint(0,columns-1), rows-1)

# desenha tabuleiro
def drawBoard(board):

    for row in range(rows):
        for column in range(columns):
            # numero 1 indica que existe buraco
            if board[row][column] == solidSquare or board[row][column] == deactivatedHole:
                drawSquare(row, column, orange)
            elif board[row][column] == playerSquare:
                drawSquare(row, column, yellow)
                player_loc.center = centralizeImage(xPlayer,yPlayer)
            elif board[row][column] == trailSquare:
                drawSquare(row, column, lightOrange)
            elif board[row][column] == finishBlue:
                drawSquare(row, column, blue)
            elif board[row][column] == startingLine:
                drawSquare(row, column, pink)
            elif board[row][column] == hole:
                drawSquare(row, column, black)
            elif board[row][column] == sandSquare:
                #drawSquare(row, column, green)
                sand_loc.center = centralizeImage(column, row)
                screen.blit(sandIcon, sand_loc)
            elif board[row][column] == waterSquare:  
                #drawSquare(row, column, ciano)
                water_loc.center = centralizeImage(column,row)
                screen.blit(waterIcon, water_loc)
            elif board[row][column] == fireSquare:
                drawSquare(row, column, red)
                fire_loc.center = centralizeImage(column,row)
                screen.blit(fireIcon, fire_loc)

# define movimento do jogador
def movePlayer(direction, mode):
    global xPlayer, yPlayer, trail

    xPlayer += direction[0]
    yPlayer += direction[1]

    if recordMoviments() and mode == 'computer':
        return False
    else:
        return True
    
def recordMoviments():
    global xPlayer, yPlayer, trail

    if board[yPlayer][xPlayer] == hole or board[yPlayer][xPlayer] == deactivatedHole:  # caso ele passe em um buraco
        board[yPlayer][xPlayer] = hole
        index = graph.coordinatesToIndex([xPlayer, yPlayer], board)
        graph.removeBlock(index)
        graphDic.removeBlock(index)
        xPlayer, yPlayer = startPosition()
        board[yPlayer][xPlayer] = playerSquare
        cleanTrail()
        trail.append([xPlayer, yPlayer, trailSquare])
        return False
    
    elif yPlayer == 1:  # caso ele chegue ao final
        xPlayer, yPlayer = startPosition()
        board[yPlayer][xPlayer] = 2
        cleanTrail()
        trail.append([xPlayer, yPlayer, trailSquare])
        player_loc.center = centralizeImage(xPlayer,yPlayer)
        win()

    else:
        markTrail()
        trail.append([xPlayer, yPlayer, board[yPlayer][xPlayer]])
        if board[yPlayer][xPlayer] == sandSquare:
            pygame.event.set_blocked(pygame.KEYDOWN)
            time.sleep(1)
            pygame.event.set_allowed(pygame.KEYDOWN)
        elif board[yPlayer][xPlayer] == waterSquare:
            pygame.event.set_blocked(pygame.KEYDOWN)
            time.sleep(2)
            pygame.event.set_allowed(pygame.KEYDOWN)
        elif board[yPlayer][xPlayer] == fireSquare:
            pygame.event.set_blocked(pygame.KEYDOWN)
            time.sleep(2.5)
            pygame.event.set_allowed(pygame.KEYDOWN)
            
        board[yPlayer][xPlayer] = playerSquare
        return True

def markTrail():
    global trail
    for i in trail:
        X, Y, cor = i
        board[Y][X] = trailSquare

def cleanTrail():
    global trail
    for i in range(len(trail)):
        X, Y, cor = trail[i]
        board[Y][X] = cor
    trail = []

def win():
    screen.fill(lightBlue)
    global board
    board = createBoard(rows, columns)
    graph.matrixToGraph(board)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto do titulo

        WIN_TEXT = font.render("PARABÉNS ! VOCÊ VENCEU", True, white)
        WIN_RECT = WIN_TEXT.get_rect(center=(width/2, height * 0.15))

        
        # Definir os botões

        MENU_BUTTON = pygame.Rect((width/3), (height/3), 300, 50)
        MENU_TEXT = font.render("Voltar ao menu", True, white)
        MENU_TEXT_RECT = MENU_TEXT.get_rect(center=MENU_BUTTON.center)

        
        QUIT_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.10), 300, 50)
        QUIT_TEXT = font.render("Sair", True, white)
        QUIT_TEXT_RECT = QUIT_TEXT.get_rect(center=QUIT_BUTTON.center)

        pygame.draw.rect(screen, secondary_pink, MENU_BUTTON)
        pygame.draw.rect(screen, secondary_pink, QUIT_BUTTON)

        screen.blit(WIN_TEXT, WIN_RECT)
        screen.blit(MENU_TEXT, MENU_TEXT_RECT)
        screen.blit(QUIT_TEXT, QUIT_TEXT_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.collidepoint(MENU_MOUSE_POS):
                    main_menu()

                if QUIT_BUTTON.collidepoint(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# define movimento do computador
def playComputer():
    global xPlayer, yPlayer, board
    start = graph.coordinatesToIndex([xPlayer,yPlayer],board)
    path = graph.dijkstra(start, 15)
    graph.clearVisited()
    path = graph.pathToMoves(path, board)

    return path

#define movimento do computador plus
def playComputerPlus():
    global xPlayer, yPlayer, board
    start = graphDic.coordinatesToIndex([xPlayer,yPlayer],board)

    path = graphDic.getMoves(start, random.randint(15, 29), board)
    return path

board = createBoard(rows, columns)
graph.matrixToGraph(board)
graphDic.matrixToGraph(board)
player = xPlayer, yPlayer = startPosition()
trail = []
trail.append([xPlayer, yPlayer, board[yPlayer][xPlayer]])
board[yPlayer][xPlayer] = playerSquare

# carrega imagem do jogador
playerIcon = pygame.image.load('jujuba.png')
playerIcon = pygame.transform.scale(playerIcon, (square_size, square_size))
player_loc = playerIcon.get_rect()
player_loc.center = centralizeImage(xPlayer,yPlayer)

#carrega imagem fogo
fireIcon = pygame.image.load('fogo.jpg')
fireIcon = pygame.transform.scale(fireIcon, (square_size, square_size))
fire_loc = fireIcon.get_rect()

#carrega imagem agua
waterIcon = pygame.image.load('agua.jpg')
waterIcon = pygame.transform.scale(waterIcon, (square_size, square_size))
water_loc = waterIcon.get_rect()

#carrega imagem areia
sandIcon = pygame.image.load('areia.jpg')
sandIcon = pygame.transform.scale(sandIcon, (square_size, square_size))
sand_loc = sandIcon.get_rect()

# Definir as fontes
font = pygame.font.Font(None, 36)
fontFooter = pygame.font.SysFont('verdana', 20, italic=pygame.font.Font.italic)

# Definir o relógio
clock = pygame.time.Clock()

def computer_play():
    path = playComputer()
    while True:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if path != None and len(path) > 0:
            x, y = path.pop(0)
            if movePlayer([x, y], 'computer'):
                path = playComputer()

        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)
        pygame.display.update()
        time.sleep(0.5)

def computer_play_plus():
    path = playComputerPlus()
    while True:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if path != None and len(path) > 0:
            x, y = path.pop()
            if movePlayer([x, y], 'computer'):
                path = playComputerPlus()

        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)
        pygame.display.update()
        time.sleep(0.5)



def play():
    while True:

        screen.fill(white)
        drawBoard(board)
        screen.blit(playerIcon, player_loc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_LEFT, K_a]:
                    if xPlayer > 0:
                        movePlayer([-1, 0], 'player')
                if event.key in [K_RIGHT, K_d]:
                    if xPlayer < rows-1:
                        movePlayer([1, 0], 'player')
                if event.key in [K_UP, K_w]:
                    if yPlayer > 0:
                        movePlayer([0, -1], 'player')
                if event.key in [K_DOWN, K_s]:
                    if yPlayer < rows-1:
                        movePlayer([0, 1], 'player')

        pygame.display.update()

def main_menu():
    while True:
        screen.fill(lightBlue)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto do titulo

        MENU_TEXT = font.render("TIP TOE - FALL GUYS", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height * 0.2))

        # Texto do rodape

        FOOTER_TEXT = font.render(
            "Trabalho de Grafos 2 - @AntonioRangelC e @kessJhones", True, white)
        FOOTER_RECT = FOOTER_TEXT.get_rect(center=(width/2, height*0.9))

        # Definir os botões

        PLAY_BUTTON = pygame.Rect((width/3), (height/3), 300, 50)
        PLAY_TEXT = font.render("Jogador vs Máquina", True, white)
        PLAY_TEXT_RECT = PLAY_TEXT.get_rect(center=PLAY_BUTTON.center)

        COMPUTER_PLAY_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.15), 300, 50)
        COMPUTER_PLAY_TEXT = font.render("Máquina vs Máquina", True, white)
        COMPUTER_PLAY_TEXT_RECT = COMPUTER_PLAY_TEXT.get_rect(
            center=COMPUTER_PLAY_BUTTON.center)

        PLUS_BUTTON = pygame.Rect((width/3), (height/3) + (height * 0.30), 300, 50)
        PLUS_TEXT = font.render("Tip Toe Plus", True, white)
        PLUS_TEXT_RECT = PLUS_TEXT.get_rect(center=PLUS_BUTTON.center)
        
        QUIT_BUTTON = pygame.Rect(
            (width/3), (height/3) + (height * 0.45), 300, 50)
        QUIT_TEXT = font.render("Sair", True, white)
        QUIT_TEXT_RECT = QUIT_TEXT.get_rect(center=QUIT_BUTTON.center)

        pygame.draw.rect(screen, secondary_pink, PLAY_BUTTON)
        pygame.draw.rect(screen, secondary_pink, COMPUTER_PLAY_BUTTON)
        pygame.draw.rect(screen, secondary_pink, QUIT_BUTTON)
        pygame.draw.rect(screen, secondary_pink, PLUS_BUTTON)

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(PLAY_TEXT, PLAY_TEXT_RECT)
        screen.blit(COMPUTER_PLAY_TEXT, COMPUTER_PLAY_TEXT_RECT)
        screen.blit(PLUS_TEXT, PLUS_TEXT_RECT)
        screen.blit(QUIT_TEXT, QUIT_TEXT_RECT)
        screen.blit(FOOTER_TEXT, FOOTER_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.collidepoint(MENU_MOUSE_POS):
                    play()
                if COMPUTER_PLAY_BUTTON.collidepoint(MENU_MOUSE_POS):
                    computer_play()
                if QUIT_BUTTON.collidepoint(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if PLUS_BUTTON.collidepoint(MENU_MOUSE_POS):
                    # funcao do plus
                    computer_play_plus()

        pygame.display.update()

main_menu()
pygame.quit()
