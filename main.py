from cmu_graphics import *
import random

class Card:
    def __init__(self, number, suite, color, image, back):
        self.number = number
        self.suite = suite
        self.color = color
        self.image = image
        self.back = back
        self.showBack = True
        self.leftTopCornerX = 0
        self.leftTopCornerY = 0
        self.prevLeftTopCornerX = 0
        self.prevLeftTopCornerY = 0
        self.centerX = 0
        self.centerY = 0
        self.selected = False
        self.prevCol = None
        self.col = 0

    def __repr__(self):
        return f'{self.number} {self.suite} {self.selected}'

class CardGroup:
    def __init__(self, cards):
        self.cards = cards
        self.selected = False
    
    def __repr__(self):
        return f'{self.cards}'

def onAppStart(app):
    # spades
    app.aceSpades = Card(1, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/aceSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.twoSpades = Card(2, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/twoSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.threeSpades = Card(3, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/threeSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fourSpades = Card(4, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/fourSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fiveSpades = Card(5, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/fiveSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sixSpades = Card(6, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/sixSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sevenSpades = Card(7, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/sevenSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.eightSpades = Card(8, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/eightSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.nineSpades = Card(9, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/nineSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.tenSpades = Card(10, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/tenSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.jackSpades = Card(11, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/jackSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.queenSpades = Card(12, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/queenSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.kingSpades = Card(13, 'spades', 'black', '/Users/kellyzhou/atla-solitaire/cards/kingSpades.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    # clubs
    app.aceClubs = Card(1, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/aceClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.twoClubs = Card(2, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/twoClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.threeClubs = Card(3, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/threeClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fourClubs = Card(4, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/fourClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fiveClubs = Card(5, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/fiveClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sixClubs = Card(6, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/sixClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sevenClubs = Card(7, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/sevenClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.eightClubs = Card(8, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/eightClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.nineClubs = Card(9, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/nineClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.tenClubs = Card(10, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/tenClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.jackClubs = Card(11, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/jackClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.queenClubs = Card(12, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/queenClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.kingClubs = Card(13, 'clubs', 'black', '/Users/kellyzhou/atla-solitaire/cards/kingClubs.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    # hearts
    app.aceHearts = Card(1, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/aceHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.twoHearts = Card(2, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/twoHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.threeHearts = Card(3, 'hearts','red', '/Users/kellyzhou/atla-solitaire/cards/threeHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fourHearts = Card(4, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/fourHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fiveHearts = Card(5, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/fiveHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sixHearts = Card(6, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/sixHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sevenHearts = Card(7, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/sevenHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.eightHearts = Card(8, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/eightHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.nineHearts = Card(9, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/nineHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.tenHearts = Card(10, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/tenHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.jackHearts = Card(11, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/jackHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.queenHearts = Card(12, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/queenHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.kingHearts = Card(13, 'hearts', 'red', '/Users/kellyzhou/atla-solitaire/cards/kingHearts.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    # diamonds
    app.aceDiamonds = Card(1, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/aceDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.twoDiamonds = Card(2, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/twoDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.threeDiamonds = Card(3, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/threeDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fourDiamonds = Card(4, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/fourDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.fiveDiamonds = Card(5, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/fiveDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sixDiamonds = Card(6, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/sixDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.sevenDiamonds = Card(7, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/sevenDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.eightDiamonds = Card(8, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/eightDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.nineDiamonds = Card(9, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/nineDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.tenDiamonds = Card(10, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/tenDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.jackDiamonds = Card(11, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/jackDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.queenDiamonds = Card(12, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/queenDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')
    app.kingDiamonds = Card(13, 'diamonds', 'red', '/Users/kellyzhou/atla-solitaire/cards/kingDiamonds.png', '/Users/kellyzhou/atla-solitaire/cards/back.png')

    app.cardDeck = [app.aceSpades, app.twoSpades, app.threeSpades, app.fourSpades, app.fiveSpades, app.sixSpades,
                    app.sevenSpades, app.eightSpades, app.nineSpades, app.tenSpades, app.jackSpades, app.queenSpades,
                    app.kingSpades, app.aceClubs, app.twoClubs, app.threeClubs, app.fourClubs, app.fiveClubs, app.sixClubs,
                    app.sevenClubs, app.eightClubs, app.nineClubs, app.tenClubs, app.jackClubs, app.queenClubs, app.kingClubs,
                    app.aceHearts, app.twoHearts, app.threeHearts, app.fourHearts, app.fiveHearts, app.sixHearts, app.sevenHearts,
                    app.eightHearts, app.nineHearts, app.tenHearts, app.jackHearts, app.queenHearts, app.kingHearts, app.aceDiamonds,
                    app.twoDiamonds, app.threeDiamonds, app.fourDiamonds, app.fiveDiamonds, app.sixDiamonds, app.sevenDiamonds,
                    app.eightDiamonds, app.nineDiamonds, app.tenDiamonds, app.jackDiamonds, app.queenDiamonds, app.kingDiamonds]
    random.shuffle(app.cardDeck)
    app.initialTableau = app.cardDeck[:29]
    app.stack = app.cardDeck[29:]
    app.drawnStack = []
    app.colBounds = [(150, 246), (325, 421), (500, 596), (675, 771), (850, 946), (1025, 1121), (1200, 1296)]
    app.frontCards = []
    app.orderedStacks = [ [] for i in range(4) ]

    app.tableau = []
    initialSetup(app)

    app.cardGroup = None

    app.score = 0
    app.timer = '00:00'
    app.moves = 0

def initialSetup(app):
    cardCount = 0
    startX = 0
    for cols in range(7): # set positions of initial tableau
        colCards = []
        cardInd = 0
        for card in range(cols+1):
            app.initialTableau[cardCount].leftTopCornerX = (startX%1225)+150
            app.initialTableau[cardCount].leftTopCornerY = (cardInd*55)+285
            app.initialTableau[cardCount].centerX = app.initialTableau[cardCount].leftTopCornerX + 48
            app.initialTableau[cardCount].centerY = app.initialTableau[cardCount].leftTopCornerY + 65.5
            app.initialTableau[cardCount].col = cols
            colCards.append(app.initialTableau[cardCount])
            cardCount += 1
            cardInd += 1
        startX += 175
        app.tableau.append(colCards)    

def drawBoard(app):
    startX = 0
    for col in range(7):
        for cardInd in range(len(app.tableau[col])):
            if cardInd == len(app.tableau[col]) - 1:
                app.tableau[col][cardInd].showBack = False
            if app.tableau[col][cardInd].showBack == True:
                drawImage(app.tableau[col][cardInd].back, app.tableau[col][cardInd].leftTopCornerX, app.tableau[col][cardInd].leftTopCornerY)
            else:
                drawImage(app.tableau[col][cardInd].image, app.tableau[col][cardInd].leftTopCornerX, app.tableau[col][cardInd].leftTopCornerY)
        startX += 175
    
    # four rectangles
    xLoc = 150
    for i in range(4):
        drawRect(xLoc, 100, 96, 131, fill=None, border='black', borderWidth=1.5)
        xLoc += 175
    xLoc = 150
    for stack in range(4):
        for card in app.orderedStacks[stack]:
            drawImage(card.image, xLoc, 100)
        xLoc += 175

    # stack
    for card in app.stack:
        drawImage(card.back, 1200, 100)
    drawRect(1025, 100, 96, 131, fill=None, border='black', borderWidth=1.5)
    for card in app.drawnStack:
        drawImage(card.image, 1025, 100)

    # banner
    drawRect(0, 0, 2880, 60, fill='navy', opacity=20)
    drawLabel(f'Score: {app.score}', 400, 30, size=16, font='monospace', bold=True)
    drawLabel(f'Time: {app.timer}', 720, 30, size=16, font='monospace', bold=True)
    drawLabel(f'Moves: {app.moves}', 1000, 30, size=16, font='monospace', bold=True)

def redrawAll(app):
    drawImage('/Users/kellyzhou/atla-solitaire/backgrounds/3.png', 0, 0)
    drawBoard(app)

def getCard(app, mouseX, mouseY):
    for col in range(7):
        cardInd = 0
        for card in app.tableau[col]:
            if card.showBack == False:
                startX = card.leftTopCornerX 
                startY = card.leftTopCornerY
                endX = card.leftTopCornerX + 96
                endY = card.leftTopCornerY + 131
                if mouseX >= startX and mouseX <= endX and mouseY >= startY and mouseY <= endY:
                    if cardInd+1 == len(app.tableau[col]):
                        return card
                    else:
                        app.cardGroup = CardGroup(app.tableau[col][cardInd:]) 
                        return app.cardGroup
            cardInd += 1
    return None

def deselectPrevCard(app):
    if app.cardGroup != None:
        app.cardGroup = None
    else:
        for col in range(7):
            for card in app.tableau[col]:
                if card.selected:
                    card.selected = False

def onMousePress(app, mouseX, mouseY):
    deselectPrevCard(app)
    card = getCard(app, mouseX, mouseY)
    if card != None:
        card.selected = True

def onMouseDrag(app, mouseX, mouseY): 
    if app.cardGroup != None:
        midCard = len(app.cardGroup.cards) // 2
        cardInd = 0
        for card in app.cardGroup.cards:
            if cardInd <= midCard:
                card.leftTopCornerX = mouseX - 48
                card.leftTopCornerY = mouseY - (((midCard+1) - cardInd)*65.5)
            else:
                card.leftTopCornerX = mouseX - 48
                card.leftTopCornerY = mouseY + ((cardInd-(midCard+1))*65.5)
            cardInd += 1
    else:
        for col in range(7):
            for card in app.tableau[col]:
                if card.selected:
                    card.centerX = mouseX
                    card.centerY = mouseY
                    card.leftTopCornerX = card.centerX - 48
                    card.leftTopCornerY = card.centerY - 65.5

def onMouseRelease(app, mouseX, mouseY):
    if app.cardGroup != None:
        for col in range(7):
            for card in app.tableau[col]:
                if card == app.cardGroup.cards[0]:
                    for i in range(len(app.cardGroup.cards)):
                        app.tableau[col].pop()
        colInd = 0
        for (x1, x2) in app.colBounds:
            if mouseX >= x1 and mouseX <= x2:
                for card in app.cardGroup.cards:
                    app.tableau[colInd].append(card)
            colInd += 1
    else:
        for col in range(7):
            for card in app.tableau[col]:
                if card.selected == True:
                    app.tableau[col].pop()
                    colInd = 0
                    for (x1, x2) in app.colBounds:
                        if mouseX >= x1 and mouseX <= x2:
                            app.tableau[colInd].append(card)
                        colInd += 1
    # legality check

def main():
    runApp(width=2880, height=1800)

main()