import math
import pygame
import time
from random import randint

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def make_board():
    ret = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            ret[i][j] = randint(-1, 1)
    return ret


def valid(x, y):
    return x >= 0 and x < 3 and y >= 0 and y < 3


def minimizer(board, x, y, alpha, beta, rem, score, px, py):
    if rem == 0:
        return score
    pv = board[px][py]

    bestValue = math.inf
    for v in [-1, 0, 1]:
        board[px][py] = v
        bestValue = min(bestValue, maximizer(board, x, y, alpha, beta, rem, score)[0])
        beta = min(beta, bestValue)
        if beta <= alpha:
            break
    board[px][py] = pv
    return bestValue


def maximizer(board, x, y, alpha, beta, rem, score):
    if rem == 0:
        return score
    bestMove = (0, 0)
    bestValue = -math.inf
    for dx, dy in moves:
        nx = x + dx
        ny = y + dy
        if valid(nx, ny):
            if bestValue < score + board[nx][ny]:
                bestValue = score + board[nx][ny]
                bestMove = (dx, dy)

            minimizerValue = minimizer(board, nx, ny, alpha, beta, rem - 1, score + board[nx][ny], x, y)
            if bestValue < minimizerValue:
                bestValue = minimizerValue
                bestMove = (dx, dy)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
    return (bestValue, bestMove)


def game(board, x, y, rem, score, goal):
    # -------update GUI------
    drawBoard(board, score, rem, goal, x, y, None)
    pygame.display.update()
    time.sleep(1.0)
    # -------------------------
    if score >= goal:
        drawBoard(board, score, rem, goal, x, y, 'win')
        pygame.display.update()
        time.sleep(0.3)
        return
    if rem == 0:
        drawBoard(board, score, rem, goal, x, y, 'lose')
        pygame.display.update()
        time.sleep(0.3)
        return

    dx, dy = maximizer(board, x, y, -math.inf, math.inf, rem, board[x][y])[1]

    nx = x + dx
    ny = y + dy

    board[x][y] = randint(-1, 1)
    board[nx][ny] = score + board[nx][ny]

    return game(board, nx, ny, rem - 1, board[nx][ny], goal)


# ------------------------------------GUI----------------------------------------------------------

TILESIZE = 100
WINDOWWIDTH = 480
WINDOWHEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 50, 255)
TURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
RED = (255, 0, 0)
BGCOLOR = TURQUOISE
BORDERCOLOR = BLUE
XMARGIN = 89
YMARGIN = 89


def drawBoard(board, score, moves, goal, x, y, condition):
    Gamewin.fill(BGCOLOR)
    sc = "score:" + str(score) + " / " + str(goal)
    rm = "moves left:"+str(moves)
    addText(sc, WHITE, 5, 5)
    addText(rm, WHITE, 5, 30)
    if condition == 'win':
        addText("WIN!", GREEN, 212, 50)
    if condition == 'lose':
        addText("LOSE!", RED, 212, 50)
    for tilex in range(3):
        for tiley in range(3):
            if tilex == x and tiley == y:
                drawTile(tilex, tiley, board[tilex][tiley], True)
            else:
                drawTile(tilex, tiley, board[tilex][tiley], False)
    width = 3 * TILESIZE
    height = 3 * TILESIZE
    pygame.draw.rect(Gamewin, BORDERCOLOR, (XMARGIN - 5, YMARGIN - 5, width + 11, height + 11), 4)


def getXYOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def addText(text, color, top, left):
    textSurf = BASICFONT.render(text, True, color, BGCOLOR)
    Gamewin.blit(textSurf, (top, left))


def drawTile(tilex, tiley, num, currPlace):
    TILECOLOR = WHITE
    if currPlace:
        TILECOLOR = GREEN
    left, top = getXYOfTile(tilex, tiley)
    pygame.draw.rect(Gamewin, TILECOLOR, (left, top, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(num), True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2), top + int(TILESIZE / 2)
    Gamewin.blit(textSurf, textRect)


def main():
    maxMoves = int(input("Enter the maximum number of moves: "))
    goal = int(input("Enter the minimal score to win: "))
    global Gamewin, BASICFONT
    pygame.init()
    Gamewin = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('square game')
    BASICFONT = pygame.font.SysFont("monospace", 25)
    board = make_board()

    game(board, 0, 2, maxMoves, 0, goal)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    main()
