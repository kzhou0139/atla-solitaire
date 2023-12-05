from cmu_graphics import *
import random
import copy

# make winning screen

# class for individual cards
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
        self.selected = False
        self.prevCol = None
        self.col = 0

    def __repr__(self):
        return f'{self.number} {self.suite} {self.selected}'

# class for card groups
class CardGroup:
    def __init__(self, cards):
        self.cards = cards
        self.selected = False
        self.leftTopCornerX = 0
        self.leftTopCornerY = 0
        self.prevLeftTopCornerX = 0
        self.prevLeftTopCornerY = 0
    
    def __repr__(self):
        return f'{self.cards}'

# initializes all app values
def onAppStart(app):
    app.cardDeck = []
    file = open('cards.txt', 'r')
    app.cardDeck = getCardDeck(app, file)

    random.shuffle(app.cardDeck) 
    app.initialTableau = app.cardDeck[:28]
    app.stack = app.cardDeck[28:]
    app.drawnStack = []
    app.selectedCardInStack = False
    app.colBounds = [(150, 246), (325, 421), (500, 596), (675, 771), (850, 946), (1025, 1121), (1200, 1296)]
    
    app.foundations = [ [] for i in range(4) ]

    app.tableau = []
    initialSetup(app)

    app.testTableau = []
    app.testFoundations = []
    app.testStack = []
    app.testDrawnStack = []
    app.possCards = []

    app.prevMoves = []

    app.selectedCardInStack = False
    app.selectedCardInFoundation = False
    app.cardGroup = None

    app.hintLabel = ''
    app.score = 0
    app.counter = 30
    app.timerLabel = '30 seconds'
    app.stepsPerSecond = 1
    app.timerActive = False
    app.moves = 0

# initializes all 52 cards from cards.txt
def getCardDeck(app, file):
    app.deck = []
    for line in file.readlines():
        parCount = 0
        for attr in line.split(', '):
            if parCount == 0:
                number = int(attr)
            elif parCount == 1:
                suite = attr
            elif parCount == 2:
                color = attr
            elif parCount == 3:
                frontImg = attr
            elif parCount == 4:
                backImg = attr
            parCount += 1
        card = Card(number, suite, color, frontImg, backImg)
        app.deck.append(card)
    return app.deck

# sets positions of initial tableau and stack
def initialSetup(app): 
    cardCount = 0
    startX = 0
    for cols in range(7): 
        colCards = []
        cardInd = 0
        for card in range(cols+1):
            app.initialTableau[cardCount].leftTopCornerX = (startX%1225)+150
            app.initialTableau[cardCount].leftTopCornerY = (cardInd*50)+275
            app.initialTableau[cardCount].prevLeftTopCornerX = (startX%1225)+150
            app.initialTableau[cardCount].prevLeftTopCornerY = (cardInd*50)+275
            app.initialTableau[cardCount].col = cols
            colCards.append(app.initialTableau[cardCount])
            cardCount += 1
            cardInd += 1
        startX += 175
        app.tableau.append(colCards)   

    for card in app.stack:
        card.leftTopCornerX = 1200
        card.leftTopCornerY = 90 

# draws tableau, foundation, stack, drawn stack, top banner, side buttons, and labels
def drawBoard(app):
    startX = 0
    for col in range(7):
        drawLabel(f'{col}', app.colBounds[col][0]+48, 265, bold=True, fill='black')
        if col < 4:
            drawLabel(f'{col}', app.colBounds[col][0]+48, 230, bold=True, fill='black')
        for cardInd in range(len(app.tableau[col])):
            if cardInd == len(app.tableau[col]) - 1:
                app.tableau[col][cardInd].showBack = False
            if app.tableau[col][cardInd].showBack == True:
                drawImage(app.tableau[col][cardInd].back, app.tableau[col][cardInd].leftTopCornerX, app.tableau[col][cardInd].leftTopCornerY)
            else:
                drawImage(app.tableau[col][cardInd].image, app.tableau[col][cardInd].leftTopCornerX, app.tableau[col][cardInd].leftTopCornerY)
                if app.tableau[col][cardInd].selected == True:
                    drawRect(app.tableau[col][cardInd].leftTopCornerX, app.tableau[col][cardInd].leftTopCornerY, 96, 131, border='yellow', fill=None)
        startX += 175
    
    # four rectangles
    xLoc = 150
    for i in range(4):
        drawRect(xLoc, 90, 96, 131, fill=None, border='black', borderWidth=1.5)
        xLoc += 175
    xLoc = 150
    for stack in range(4):
        for card in app.foundations[stack]:
            drawImage(card.image, card.leftTopCornerX, card.leftTopCornerY)
            if card.selected == True:
                drawRect(card.leftTopCornerX, card.leftTopCornerY, 96, 131, border='yellow', fill=None)
        xLoc += 175

    # stack
    drawRect(1025, 90, 96, 131, fill=None, border='black', borderWidth=1.5)
    drawRect(1200, 90, 96, 131, fill=None, border='black', borderWidth=1.5)
    for card in app.stack:
        drawImage(card.back, 1200, 90)
    for card in app.drawnStack:
        drawImage(card.image, card.leftTopCornerX, card.leftTopCornerY)
        if card.selected == True:
            drawRect(card.leftTopCornerX, card.leftTopCornerY, 96, 131, border='yellow', fill=None)

    # banner
    drawRect(0, 0, 2880, 55, fill='navy', opacity=20)
    drawLabel(f'Score: {app.score}', 400, 27, size=16, font='monospace', bold=True)
    if app.timerActive == True:
        drawLabel(f'Time: {app.timerLabel}', 720, 27, size=16, font='monospace', bold=True, fill='red')
    else:
        drawLabel(f'Time: {app.timerLabel}', 720, 27, size=16, font='monospace', bold=True, fill='green')
    drawLabel(f'Moves: {app.moves}', 1000, 27, size=16, font='monospace', bold=True)

    # side buttons
    if len(app.prevMoves) == 0:
        drawRect(1360, 90, 50, 50, fill='steelBlue', border='black', borderWidth=1)
    else:
        drawRect(1360, 90, 50, 50, fill='lightSteelBlue', border='black', borderWidth=1)
    if app.timerActive == True:
        drawRect(1360, 165, 50, 50, fill='steelBlue', border='black', borderWidth=1)
    else:
        drawRect(1360, 165, 50, 50, fill='lightSteelBlue', border='black', borderWidth=1)
    drawLabel('Undo', 1385, 115, fill='black', size=14)
    drawLabel('Hint', 1385, 190, fill='black', size=14)

    # hint label
    drawRect(500, 60, 450, 20, border='yellow', borderWidth=1, fill=None)
    drawLabel(f'{app.hintLabel}', 725, 70, size=14)

# redraws background and entire board
def redrawAll(app):
    drawImage('/Users/kellyzhou/atla-solitaire/backgrounds/bg.png', 0, 0)
    drawBoard(app)

# gets the current card / card group that is selected
def getCard(app, mouseX, mouseY):
    for col in range(7): # tableau
        cardInd = 0
        for card in app.tableau[col]:
            if card.showBack == False:
                startX = card.leftTopCornerX 
                startY = card.leftTopCornerY
                endX = card.leftTopCornerX + 96
                endY = card.leftTopCornerY + 50
                if mouseX >= startX and mouseX <= endX and mouseY >= startY and mouseY <= endY:
                    if cardInd+1 == len(app.tableau[col]): # single card
                        return card
                    else: # card group
                        app.cardGroup = CardGroup(app.tableau[col][cardInd:])
                        app.cardGroup.leftTopCornerX = app.tableau[col][cardInd].leftTopCornerX
                        app.cardGroup.leftTopCornerY = app.tableau[col][cardInd].leftTopCornerY
                        return app.cardGroup
            cardInd += 1

    colInd = 0 # four rects
    for (x1, x2) in app.colBounds:
        if mouseX >= x1 and mouseX <= x2 and colInd < 4:
            if len(app.foundations[colInd]) != 0:
                app.selectedCardInFoundation = True
                card = app.foundations[colInd][-1]
                card.selected = True
                return card
        colInd += 1

    if (mouseX >= 1200 and mouseX <= 1296 and mouseY >= 90 and mouseY <= 231): # stack
        if len(app.stack) == 0:
            resetStack(app)
        else:
            app.selectedCardInStack = True
            return app.stack[-1]
    if (mouseX >= 1025 and mouseX <= 1121 and mouseY >= 90 and mouseY <= 231): # drawn stack
        if len(app.drawnStack) != 0:
            app.selectedCardInStack = True
            return app.drawnStack[-1]
    return None

# resets the stack if it is empty
def resetStack(app):
    for card in app.drawnStack:
        card.selected = False
        card.showBack = True
        card.leftTopCornerX = 1200
        card.leftTopCornerY = 90
        app.stack.insert(0, card)
    app.drawnStack = []

# deselects the previously selected card / card group
def deselectPrevCard(app):
    app.cardGroup = None
    app.selectedCardInStack = False
    app.selectedCardInFoundation = False
    for col in range(7):
            for card in app.tableau[col]:
                if card.selected:
                    card.selected = False
                    card.prevLeftTopCornerX = 0
                    card.prevLeftTopCornerY = 0
    for card in app.drawnStack:
            if card.selected == True:
                card.selected = False
                card.prevLeftTopCornerX = 0
                card.prevLeftTopCornerY = 0
    for col in range(4): 
            for card in app.foundations[col]:
                if card.selected == True:
                    card.selected = False
                    card.prevLeftTopCornerX = 0
                    card.prevLeftTopCornerY = 0

# performs the countdown on the hint timer
def onStep(app):
    if app.timerActive == True:
        app.counter -= 1
        app.timerLabel = f'{app.counter} seconds'
    if app.counter == 0:
        app.timerActive = False

# updates variables and performs actions when a card / button is pressed
def onMousePress(app, mouseX, mouseY):
    deselectPrevCard(app)
    if mouseX >= 1360 and mouseX <= 1410 and mouseY >= 90 and mouseY <= 140:
        if len(app.prevMoves) != 0:
            undoBoard(app, app.prevMoves[-1], 'real') 
            app.prevMoves.pop()
            app.moves += 1
    if mouseX >= 1360 and mouseX <= 1410 and mouseY >= 165 and mouseY <= 215:
        if app.timerActive == False:
            nextBestMove(app)
            app.counter = 30
            app.timerActive = True
    else: 
        card = getCard(app, mouseX, mouseY)
        if card != None:
            card.selected = True
            card.prevLeftTopCornerX = card.leftTopCornerX
            card.prevLeftTopCornerY = card.leftTopCornerY
        if app.cardGroup != None:
            for cd in card.cards:
                cd.selected = True
                cd.prevLeftTopCornerX = cd.leftTopCornerX
                cd.prevLeftTopCornerY = cd.leftTopCornerY
        if card in app.stack:
            card.leftTopCornerX = 1025
            card.leftTopCornerY = 90
            card.prevLeftTopCornerX = 1025
            card.prevLeftTopCornerY = 90
            card.showBack = False
            app.drawnStack.append(card)
            app.stack.pop()
            move = 'Draw card'
            app.prevMoves.append(move)
            app.moves += 1
    return

# moves card / card group around when mouse is dragged
def onMouseDrag(app, mouseX, mouseY): 
    if app.cardGroup != None:
        cardInd = 0
        for card in app.cardGroup.cards:
            if cardInd == 0:
                app.cardGroup.leftTopCornerX = mouseX - 48
                app.cardGroup.leftTopCornerY = mouseY + (cardInd*50)
            card.leftTopCornerX = mouseX - 48
            card.leftTopCornerY = mouseY + (cardInd*50)
            cardInd += 1
    elif app.selectedCardInStack == True:
        app.drawnStack[-1].leftTopCornerX = mouseX - 48
        app.drawnStack[-1].leftTopCornerY = mouseY - 65.5
    elif app.selectedCardInFoundation == True:
        for stack in range(4):
            for card in app.foundations[stack]:
                if card.selected == True:
                    card.leftTopCornerX = mouseX - 48
                    card.leftTopCornerY = mouseY - 65.5
    else:
        for col in range(7):
            for card in app.tableau[col]:
                if card.selected:
                    card.leftTopCornerX = mouseX - 48
                    card.leftTopCornerY = mouseY - 65.5

# actions when the mouse is released
def onMouseRelease(app, mouseX, mouseY): 
    if app.cardGroup != None:
        cardGroupOnRelease(app, mouseX, mouseY)
    elif app.selectedCardInStack == True:
        stackCardsOnRelease(app, mouseX, mouseY)
    elif app.selectedCardInFoundation == True:
        foundationOnRelease(app, mouseX, mouseY)
    else:
        tableauOnRelease(app, mouseX, mouseY)

# helper function of onMouseRelease(). Legality checks and variable updates when a card group is released (user move)
def cardGroupOnRelease(app, mouseX, mouseY):
    changed = False
    for col in range(7):
        for card in app.tableau[col]:
            if card == app.cardGroup.cards[0]:
                colInd = 0
                for (x1, x2) in app.colBounds:
                    if mouseX >= x1 and mouseX <= x2:
                        if checkGroupTableauLegality(app, app.cardGroup.cards, colInd) == True: 
                            for cd in app.cardGroup.cards:
                                app.tableau[col].pop()
                                app.tableau[colInd].append(cd)
                                cd.leftTopCornerX = x1
                                cd.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 275 
                            move = f'Move the {card.number} of {card.suite} group in col {col} to col {colInd}'
                            app.prevMoves.append(move)
                            changed = True
                            app.moves += 1
                            return
                        else:
                            app.cardGroup.leftTopCornerX = app.cardGroup.prevLeftTopCornerX
                            app.cardGroup.leftTopCornerY = app.cardGroup.prevLeftTopCornerX 
                            for cd in app.cardGroup.cards:
                                cd.leftTopCornerX = cd.prevLeftTopCornerX
                                cd.leftTopCornerY = cd.prevLeftTopCornerY
                            changed = True
                            app.moves += 1
                            return
                    colInd += 1
    if changed == False:
        app.cardGroup.leftTopCornerX = app.cardGroup.prevLeftTopCornerX
        app.cardGroup.leftTopCornerY = app.cardGroup.prevLeftTopCornerX 
        for cd in app.cardGroup.cards:
            cd.leftTopCornerX = cd.prevLeftTopCornerX
            cd.leftTopCornerY = cd.prevLeftTopCornerY

# helper function of onMouseRelease(). Legality checks and variable updates when a card from the stack is released (user move)
def stackCardsOnRelease(app, mouseX, mouseY):
    colInd = 0
    changed = False
    if len(app.drawnStack) > 0:
        card = app.drawnStack[-1]
        for (x1, x2) in app.colBounds:
            if mouseX >= x1 and mouseX <= x2 and mouseY < 265 and colInd < 4: # move to 4 rects # MAYBE FIX
                if checkFoundationLegality(app, card, colInd):
                    app.drawnStack.pop()
                    app.foundations[colInd].append(card)
                    card.leftTopCornerX = x1
                    card.leftTopCornerY = 90
                    move = f'Move the {card.number} of {card.suite} from the stack to foundation {colInd}'
                    app.prevMoves.append(move)
                else:
                    card.leftTopCornerX = card.prevLeftTopCornerX
                    card.leftTopCornerY = card.prevLeftTopCornerY
                changed = True
                app.moves += 1
            elif mouseX >= x1 and mouseX <= x2 and mouseY >= 265: # move to tableau
                if checkSingleTableauLegality(app, card, colInd) == True:
                    app.drawnStack.pop()
                    app.tableau[colInd].append(card)
                    card.leftTopCornerX = x1
                    card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 275
                    move = f'Move the {card.number} of {card.suite} from the stack to col {colInd}'
                    app.prevMoves.append(move)
                else:
                    card.leftTopCornerX = card.prevLeftTopCornerX
                    card.leftTopCornerY = card.prevLeftTopCornerY
                changed = True
                app.moves += 1
            colInd += 1
        if changed == False:
            card.leftTopCornerX = card.prevLeftTopCornerX
            card.leftTopCornerY = card.prevLeftTopCornerY

# helper function of onMouseRelease(). Legality checks and variable updates when a card from the foundation is released (user move)
def foundationOnRelease(app, mouseX, mouseY):
    card = None
    changed = False
    for stack in range(4):
        if len(app.foundations[stack]) != 0 and app.foundations[stack][-1].selected == True:
            card = app.foundations[stack][-1]
            colInd = 0
            for (x1, x2) in app.colBounds:
                if mouseX >= x1 and mouseX <= x2:
                    if checkSingleTableauLegality(app, card, colInd) == True:
                        app.foundations[stack].pop()
                        app.tableau[colInd].append(card)
                        card.leftTopCornerX = x1
                        card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 275
                        move = f'Move the {card.number} of {card.suite} from foundation {stack} to col {colInd}'
                        app.prevMoves.append(move)
                    else:
                        card.leftTopCornerX = card.prevLeftTopCornerX
                        card.leftTopCornerY = card.prevLeftTopCornerY
                    changed = True
                    app.moves += 1
                colInd += 1
    if changed == False:
        card.leftTopCornerX = card.prevLeftTopCornerX
        card.leftTopCornerY = card.prevLeftTopCornerY

# helper function of onMouseRelease(). Legality checks and variable updates when a card from the tableau is released (user move)
def tableauOnRelease(app, mouseX, mouseY):
    # Move the {card.number} of {card.suite} in col {col} to col {possMove}
    changed = False
    cd = None
    for col in range(7):
        for card in app.tableau[col]:
            if card.selected == True:
                cd = card
                colInd = 0
                for (x1, x2) in app.colBounds:
                    if mouseX >= x1 and mouseX <= x2: # 4 rects 
                        if colInd < 4 and mouseY < 265:
                            if checkFoundationLegality(app, card, colInd):
                                app.tableau[col].pop()
                                app.foundations[colInd].append(card)
                                card.leftTopCornerX = x1
                                card.leftTopCornerY = 90
                                move = f'Move the {card.number} of {card.suite} in col {col} to foundation {colInd}'
                                app.prevMoves.append(move)
                            else:
                                card.leftTopCornerX = card.prevLeftTopCornerX
                                card.leftTopCornerY = card.prevLeftTopCornerY
                            changed = True
                            app.moves += 1
                            return
                        else: # tableau
                            if checkSingleTableauLegality(app, card, colInd) == True:
                                app.tableau[col].pop()
                                app.tableau[colInd].append(card)
                                card.leftTopCornerX = x1
                                card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 275
                                move = f'Move the {card.number} of {card.suite} in col {col} to col {colInd}'
                                app.prevMoves.append(move)
                            else:
                                card.leftTopCornerX = card.prevLeftTopCornerX
                                card.leftTopCornerY = card.prevLeftTopCornerY
                            changed = True
                            app.moves += 1
                            return
                    colInd += 1
    if changed == False and cd != None:
        cd.leftTopCornerX = cd.prevLeftTopCornerX
        cd.leftTopCornerY = cd.prevLeftTopCornerY

# checks if moving a single card to the tableau / within the tableau is legal (user move)
def checkSingleTableauLegality(app, card, colInd):
    if len(app.tableau[colInd]) == 0:
        if card.number == 13:
            return True
        return False
    elif (app.tableau[colInd][-1].number == card.number and app.tableau[colInd][-1].suite == card.suite): # comment out
        return True
    elif (app.tableau[colInd][-1].color != card.color) and (app.tableau[colInd][-1].number == (card.number+1)):
        return True
    else:
        return False

# checks if moving a card group within the tableau is legal (user move)
def checkGroupTableauLegality(app, card, colInd):
    if len(app.tableau[colInd]) == 0:
        if card[0].number == 13:
            return True
        return False
    elif (app.tableau[colInd][-1].color != card[0].color) and (app.tableau[colInd][-1].number == (card[0].number+1)):
        return True
    else:
        return False

# checks if moving a single card to a foundation is legal 
def checkFoundationLegality(app, card, colInd):
    if len(app.foundations[colInd]) == 0:
        if card.number == 1:
            return True
        return False
    elif (app.foundations[colInd][-1].suite == card.suite and app.foundations[colInd][-1].number == (card.number-1)):
        return True
    else:
        return False

# checks the tableau, stack, and foundatino for possible moves
def getHint(app): 
    possMoveList = []
    app.possCards = []
    tableauHints = getTableauHints(app)
    stackHints = getStackHints(app)
    foundationHints = getFoundationHints(app)
    if tableauHints != []:
        possMoveList.extend(tableauHints)
    if stackHints != []:
        possMoveList.extend(stackHints)
    if (len(app.testStack) != 0) or (len(app.testDrawnStack) != 0):
        possMoveList.append('Draw card') # maybe remove possMoveList == [] as condition
    if possMoveList != [] and foundationHints != []:
        #possMoveList.extend(foundationHints)
        pass
    if possMoveList == []:
        possMoveList.append('No moves left')
    return possMoveList

# helper function of getHint(). gets possible moves from the tableau
def getTableauHints(app): 
    hints = []
    for col in range(7): # moves within tableau
        cardInd = 0
        for card in app.testTableau[col]:  
            if (card.showBack == False) and (card.number != 13) and (card.number != 1):
                possMove = findTableauMove(app, card, col)
                if possMove != None:
                    if cardInd != (len(app.testTableau[col]) - 1): # group
                        hintStr = f'Move the {card.number} of {card.suite} group in col {col} to col {possMove}'
                    else: # single
                        hintStr = f'Move the {card.number} of {card.suite} in col {col} to col {possMove}'
                    hints.append(hintStr)
                    app.possCards.append(card)
                    if ((cardInd > 0) and (app.testTableau[col][cardInd-1].showBack == False) and 
                        (app.testTableau[possMove][-1].number == app.testTableau[col][cardInd-1].number)): # if move is redundant (Q, J -> Q, J)
                        hints.pop()
                        app.possCards.pop()
            if (card.showBack == False) and (card.number == 13) and (card == app.testTableau[col][-1]): # if king single
                possMove = findEmptyCol(app)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to col {possMove}'
                    hints.append(hintStr)
                    app.possCards.append(card)
                    if ((cardInd == 0) and (len(app.testTableau[possMove]) == 0)): # if move is redundant (K -> K)
                        hints.pop()
                        app.possCards.pop()
            if (card.showBack == False) and (card.number == 13) and (cardInd != (len(app.testTableau[col]) - 1)): # if king group
                if checkIsGroup(app, col, cardInd): # write
                    possMove = findEmptyCol(app)
                    if possMove != None:
                        hintStr = f'Move the {card.number} of {card.suite} group in col {col} to col {possMove}' 
                        hints.append(hintStr)
                        app.possCards.append(card)
                        if ((cardInd == 0) and (len(app.testTableau[possMove]) == 0)): # if move is redundant (K -> K)
                            hints.pop()
                            app.possCards.pop()
            if (card.showBack == False) and (card.number == 1) and (card == app.testTableau[col][-1]): # if ace
                possMove = findEmptyFoundation(app)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to foundation {possMove}'
                    hints.append(hintStr)
                    app.possCards.append(card)
            if (card.showBack == False) and (card.number != 1) and (card == app.testTableau[col][-1]): # move to foundation
                possMove = findFoundation(app, card)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to foundation {possMove}'
                    hints.append(hintStr)
                    app.possCards.append(card)
            cardInd += 1
    return hints

# helper function of getHint(). gets possible moves from the top card in the drawn stack
def getStackHints(app):
    hints = []
    if len(app.testDrawnStack) != 0:
        card = app.testDrawnStack[-1]
        possMove = findFoundation(app, card)
        if possMove != None:
            hintStr = f'Move the {card.number} of {card.suite} from the stack to foundation {possMove}'
            hints.append(hintStr)
            if card.number == 1:
                return hints
        if card.number != 1:
            possMove = findTableauMove(app, card, -1)
            if possMove != None:
                hintStr = f'Move the {card.number} of {card.suite} from the stack to col {possMove}'
                hints.append(hintStr)
        if card.number == 13:
            possMove = findEmptyCol(app)
            if possMove != None:
                hintStr = f'Move the {card.number} of {card.suite} from the stack to col {possMove}'
                hints.append(hintStr)
    return hints

# helper function of getHint(). gets possible moves from the cards in the foundation
def getFoundationHints(app):
    hints = []
    for col in range(4):
        if len(app.testFoundations[col]) > 0:
            card = app.testFoundations[col][-1]
            if card.number != 1:
                possMove = findTableauMove(app, card, -1)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} from foundation {col} to col {possMove}'
                    if card not in app.possCards:
                        hints.append(hintStr)
    return hints

# finds possible moves within the tableau
def findTableauMove(app, card, cardCol):
    for col in range(7): # within tableau
        if col == cardCol:
            continue
        if len(app.testTableau[col]) > 0:
            cd = app.testTableau[col][-1]
            if ((cd.showBack == False) and (cd.color != card.color) and 
                (cd.number == (card.number+1))):
                return col
    return None

# finds an empty column in the tableau
def findEmptyCol(app):
    for col in range(7):
        if len(app.testTableau[col]) == 0:
            return col
    return None

# finds an empty foundation column
def findEmptyFoundation(app):
    for col in range(4):
        if len(app.testFoundations[col]) == 0:
            return col
    return None

# finds a possible move to the foundations
def findFoundation(app, card):
    for col in range(4):
        if card.number == 1 and len(app.testFoundations[col]) == 0:
            return col
        if (len(app.testFoundations[col]) != 0 and app.testFoundations[col][-1].number == card.number-1 and 
            app.testFoundations[col][-1].suite == card.suite):
            return col
    return None

# checks if there's a card group
def checkIsGroup(app, col, cardInd):
    cardGroup = app.testTableau[col][cardInd:]
    for card in range(len(cardGroup)):
        if card != 0:
            if (cardGroup[card].number != cardGroup[card-1].number-1) or (cardGroup[card].color == cardGroup[card-1].color):
                return False
    return True

# simulates a card being moved based on hint (computer move)
def tryMove(app, hint):
    hintList = list(hint.split(' '))
    if len(hintList) == 2: # draw card
        if len(app.testStack) == 0:
            resetTestStack(app)
        card = app.testStack[-1]
        card.showBack = False
        app.testStack.pop()
        app.testDrawnStack.append(card)
    elif len(hintList) == 3:
        pass
    elif len(hintList) == 12:
        moveCardGroup(app, hintList)
    else:
        if hintList[6] == 'foundation':
            moveFoundationToCol(app, hintList)
        elif hintList[6] == 'col' and hintList[9] == 'foundation':
            moveColToFoundation(app, hintList)
        elif hintList[6] == 'col' and hintList[9] == 'col':
            moveColToCol(app, hintList)
        elif hintList[7] == 'stack' and hintList[9] == 'col':
            if len(app.testStack) == 0:
                resetTestStack(app)
            card = app.testStack[-1]
            app.testStack.pop()
            card.showBack = False
            app.testDrawnStack.append(card)
            moveStackToCol(app, hintList)
        elif hintList[7] == 'stack' and hintList[9] == 'foundation':
            if len(app.testStack) == 0:
                resetTestStack(app)
            card = app.testStack[-1]
            app.testStack.pop()
            card.showBack = False
            app.testDrawnStack.append(card)
            moveStackToFoundation(app, hintList)

# helper function of tryMove(). simulates a card group being moved within the tableau (computer move)
def moveCardGroup(app, hintList):
    cardNum = int(hintList[2])
    cardSuite = hintList[4]
    cardGroupCol = int(hintList[8])
    newCol = int(hintList[11])
    cardInd = 0
    for card in app.testTableau[cardGroupCol]:
        if cardNum == card.number and cardSuite == card.suite:
            cardGroup = app.testTableau[cardGroupCol][cardInd:]
            for cd in cardGroup:
                app.testTableau[cardGroupCol].pop()
                app.testTableau[newCol].append(cd)
            if len(app.testTableau[cardGroupCol]) != 0:
                app.testTableau[cardGroupCol][-1].showBack = False
        cardInd += 1

# helper function of tryMove(). simulates a card being moved from a foundation to the tableau (computer move)
def moveFoundationToCol(app, hintList):
    foundCol = int(hintList[7])
    newCol = int(hintList[10])
    card = app.testFoundations[foundCol][-1]
    app.testFoundations[foundCol].pop()
    app.testTableau[newCol].append(card)

# helper function of tryMove(). simulates a card being moved from the tableau to a foundation (computer move)
def moveColToFoundation(app, hintList):
    cardCol = int(hintList[7])
    foundCol = int(hintList[10])
    card = app.testTableau[cardCol][-1]
    app.testTableau[cardCol].pop()
    app.testFoundations[foundCol].append(card)
    if len(app.testTableau[cardCol]) != 0:
        app.testTableau[cardCol][-1].showBack = False

# helper function of tryMove(). simulates a card being moved within the tableau (computer move)
def moveColToCol(app, hintList):
    cardCol = int(hintList[7])
    newCol = int(hintList[10])
    card = app.testTableau[cardCol][-1]
    app.testTableau[cardCol].pop()
    app.testTableau[newCol].append(card)
    if len(app.testTableau[cardCol]) != 0:
        app.testTableau[cardCol][-1].showBack = False

# helper function of tryMove(). simulates a card being moved from the stack to the tableau (computer move)
def moveStackToCol(app, hintList):
    newCol = int(hintList[10])
    card = app.testDrawnStack[-1]
    app.testDrawnStack.pop()
    app.testTableau[newCol].append(card)

# helper function of tryMove(). simulates a card being moved from the stack to a foundation (computer move)
def moveStackToFoundation(app, hintList):
    foundCol = int(hintList[10])
    card = app.testDrawnStack[-1]
    app.testDrawnStack.pop()
    app.testFoundations[foundCol].append(card)

# returns the best hint
def nextBestMove(app):
    app.testTableau = copy.deepcopy(app.tableau)
    app.testFoundations = copy.deepcopy(app.foundations) 
    app.testDrawnStack = copy.copy(app.drawnStack) 
    app.testStack = copy.copy(app.stack)
    hints = getHint(app)
    print('ORIG HINTS: ', hints)
    solvable, bestHint = nextBestMoveHelper(app, hints, hints[0], 0, -1, None)
    app.hintLabel = f'{bestHint}'
    print('BEST MOVE:', bestHint)
    return bestHint

# helper function of nextBestMove()
# backtracking algorithm to find the best move. best meaning the move that leads to the most number of next possible moves
def nextBestMoveHelper(app, hints, currHint, drawCardCount, maxLevel, bestHint, level=0): 
    solvable = True
    if allFront(app):
        return True, bestHint
    else:
        for hint in hints:
            if level == 0:
                currHint = hint
            if hint == 'No moves left':
                solvable = False
            if len(hints) == 1 and hint == 'Draw card':
                drawCardCount += 1
                if drawCardCount >= len(app.testStack) + len(app.testDrawnStack):
                    drawCardCount = 0
                    solvable = False
            if level > maxLevel:
                maxLevel = level
                bestHint = currHint
            tryMove(app, hint)
            newHints = getHint(app)
            print('LEVEL: ', level+1, ' HINTS: ', newHints)
            if solvable == -1:
                solvable, bestHint = nextBestMoveHelper(app, newHints, currHint, drawCardCount, maxLevel, bestHint, level+1)
            if solvable != False and solvable != -1:
                return solvable, bestHint
            undoBoard(app, hint, 'test')
            print('undo move')
        return False, bestHint

# resets the test stack if the stack is empty
def resetTestStack(app): 
    for card in app.testDrawnStack:
        card.showBack = True
        app.testStack.insert(0, card)
    app.testDrawnStack = []

# undoes the previous move (user + computer)
def undoBoard(app, hint, whichSet):  
    if whichSet == 'test': # computer, test variables
        tableau = app.testTableau
        foundations = app.testFoundations
        stack = app.testStack
        drawnStack = app.testDrawnStack
    else: # user, actual board
        tableau = app.tableau
        foundations = app.foundations
        stack = app.stack
        drawnStack = app.drawnStack
    hintList = list(hint.split(' '))
    if len(hintList) == 2: # draw card
        if len(drawnStack) != 0:
                card = drawnStack[-1]
                drawnStack.pop()
                stack.append(card)
    elif len(hintList) == 3:
        pass
    elif len(hintList) == 12:
        undoCardGroup(app, hintList, tableau)
    else:
        if hintList[6] == 'foundation': 
            undoFoundationToCol(app, hintList, tableau, foundations) 
        elif hintList[6] == 'col' and hintList[9] == 'foundation':
            undoColToFoundation(app, hintList, tableau, foundations)
        elif hintList[6] == 'col' and hintList[9] == 'col':
            undoColToCol(app, hintList, tableau)
        elif hintList[7] == 'stack' and hintList[9] == 'col':
            undoStackToCol(app, hintList, tableau, drawnStack)
        elif hintList[7] == 'stack' and hintList[9] == 'foundation':
            undoStackToFoundation(app, hintList, foundations, drawnStack)

# helper functino of undoBoard(). undoes a card group move within the tableau (user + computer)
def undoCardGroup(app, hintList, tableau):
    cardNum = int(hintList[2])
    cardSuite = hintList[4]
    if cardSuite == 'spades' or cardSuite == 'clubs':
        cardColor = 'black'
    else:
        cardColor = 'red'
    cardGroupCol = int(hintList[8])
    newCol = int(hintList[11])
    cardInd = 0
    for card in tableau[newCol]:
        if cardNum == card.number and cardSuite == card.suite:
            cardGroup = tableau[newCol][cardInd:]
            if ((len(tableau[cardGroupCol]) > 0) and 
                    (tableau[cardGroupCol][-1].number != cardNum+1 or 
                    tableau[cardGroupCol][-1].color == cardColor)):
                tableau[cardGroupCol][-1].showBack = True
            for cd in cardGroup:
                tableau[newCol].pop() 
                tableau[cardGroupCol].append(cd)
                cd.leftTopCornerX = app.colBounds[cardGroupCol][0]
                cd.leftTopCornerY = (len(tableau[cardGroupCol])-1)*50 + 275
        cardInd += 1

# helper functino of undoBoard(). undoes a single card move from a foundation to the tableau (user + computer)
def undoFoundationToCol(app, hintList, tableau, foundations):
    foundCol = int(hintList[7])
    newCol = int(hintList[10])
    card = tableau[newCol][-1]
    tableau[newCol].pop()
    foundations[foundCol].append(card)
    card.leftTopCornerX = app.colBounds[foundCol][0]
    card.leftTopCornerY = 90

# helper functino of undoBoard(). undoes a single card move from the tableau to a foundation (user + computer)
def undoColToFoundation(app, hintList, tableau, foundations):
    cardNum = int(hintList[2])
    cardSuite = hintList[4]
    if cardSuite == 'spades' or cardSuite == 'clubs':
        cardColor = 'black'
    else:
        cardColor = 'red'
    cardCol = int(hintList[7])
    foundCol = int(hintList[10]) 
    card = foundations[foundCol][-1]
    foundations[foundCol].pop()
    if ((len(tableau[cardCol]) > 0) and 
            (tableau[cardCol][-1].number != cardNum+1 or 
            tableau[cardCol][-1].color == cardColor)):
        tableau[cardCol][-1].showBack = True
    tableau[cardCol].append(card)
    card.leftTopCornerX = app.colBounds[cardCol][0]
    card.leftTopCornerY = (len(tableau[cardCol])-1)*50 + 275

# helper functino of undoBoard(). undoes a single card move within the tableau (user + computer)
def undoColToCol(app, hintList, tableau):
    cardNum = int(hintList[2])
    cardSuite = hintList[4]
    if cardSuite == 'spades' or cardSuite == 'clubs':
        cardColor = 'black'
    else:
        cardColor = 'red'
    cardCol = int(hintList[7])
    newCol = int(hintList[10])
    card = tableau[newCol][-1]
    tableau[newCol].pop()
    if ((len(tableau[cardCol]) > 0) and 
        (tableau[cardCol][-1].number != cardNum+1 or 
        tableau[cardCol][-1].color == cardColor)):
        tableau[cardCol][-1].showBack = True
    tableau[cardCol].append(card)
    card.leftTopCornerX = app.colBounds[cardCol][0]
    card.leftTopCornerY = (len(tableau[cardCol])-1)*50 + 275

# helper functino of undoBoard(). undoes a single card move from the stack to the tableau (user + computer)
def undoStackToCol(app, hintList, tableau, drawnStack):
    newCol = int(hintList[10])
    card = tableau[newCol][-1]
    tableau[newCol].pop()
    drawnStack.append(card)
    card.leftTopCornerX = 1025 
    card.leftTopCornerY = 90 

# helper functino of undoBoard(). undoes a single card move from the stack to a foundation (user + computer)
def undoStackToFoundation(app, hintList, foundations, drawnStack):
    foundCol = int(hintList[10])
    card = foundations[foundCol][-1]
    foundations[foundCol].pop()
    drawnStack.append(card)
    card.leftTopCornerX = 1025
    card.leftTopCornerY = 90

# checks if all cards in the tableau are front-facing
def allFront(app):
    for col in range(7):
        for card in app.testTableau[col]:
            if card.showBack == True:
                return False
    return True

# runs the program
def main():
    runApp(width=2880, height=1800)

main()