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
        self.selected = False
        self.prevCol = None
        self.col = 0

    def __repr__(self):
        return f'{self.number} {self.suite} {self.selected}'

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

    app.prevTableau = []
    app.testTableau = []
    app.prevFoundations = []
    app.testFoundations = []
    app.prevDrawnStack = []
    app.testDrawnStack = []

    app.cardGroup = None

    '''app.singleCardSelected = False # implement
    app.selectedCardInTableau = False # implement
    app.selectedCardInFoundation = False # implement'''

    app.hintLabel = ''
    app.score = 0
    app.timer = '00:00'
    app.moves = 0

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

def initialSetup(app): # set positions of initial tableau
    cardCount = 0
    startX = 0
    for cols in range(7): 
        colCards = []
        cardInd = 0
        for card in range(cols+1):
            app.initialTableau[cardCount].leftTopCornerX = (startX%1225)+150
            app.initialTableau[cardCount].leftTopCornerY = (cardInd*50)+265
            app.initialTableau[cardCount].col = cols
            colCards.append(app.initialTableau[cardCount])
            cardCount += 1
            cardInd += 1
        startX += 175
        app.tableau.append(colCards)   

    for card in app.stack:
        card.leftTopCornerX = 1200
        card.leftTopCornerY = 90 

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
    drawLabel(f'Time: {app.timer}', 720, 27, size=16, font='monospace', bold=True)
    drawLabel(f'Moves: {app.moves}', 1000, 27, size=16, font='monospace', bold=True)

    # bottom buttons
    drawRect(1360, 90, 50, 50, fill='lightSteelBlue', border='black', borderWidth=1)
    drawRect(1360, 165, 50, 50, fill='lightSteelBlue', border='black', borderWidth=1)
    drawLabel('Undo', 1385, 115, fill='black', size=14)
    drawLabel('Hint', 1385, 190, fill='black', size=14)

def redrawAll(app):
    drawImage('/Users/kellyzhou/atla-solitaire/backgrounds/bg.png', 0, 0)
    drawBoard(app)

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

def resetStack(app):
    for card in app.drawnStack:
        card.selected = False
        card.showBack = True
        card.leftTopCornerX = 1200
        card.leftTopCornerY = 90
        app.stack.insert(0, card)
    app.drawnStack = []

def deselectPrevCard(app):
    '''if app.cardGroup != None: 
        app.cardGroup = None
    else:
        for col in range(7):
            for card in app.tableau[col]:
                if card.selected:
                    card.selected = False
                    card.prevLeftTopCornerX = 0
                    card.prevLeftTopCornerY = 0

    if app.selectedCardInStack == True:
        app.selectedCardInStack = False
        for card in app.drawnStack:
            if card.selected == True:
                card.selected = False
                card.prevLeftTopCornerX = 0
                card.prevLeftTopCornerY = 0
    if app.selectedCardInOrderedStack == True:
        app.selectedCardInOrderedStack = False
        for col in range(4): 
            for card in app.orderedStacks[col]:
                if card.selected == True:
                    card.selected = False
                    card.prevLeftTopCornerX = 0
                    card.prevLeftTopCornerY = 0'''
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

def onMousePress(app, mouseX, mouseY):
    if mouseX >= 1360 and mouseX <= 1410 and mouseY >= 90 and mouseY <= 140:
        undoMove(app)
    if mouseX >= 1360 and mouseX <= 1410 and mouseY >= 165 and mouseY <= 215:
        print('hello')
        getHint(app)
    deselectPrevCard(app)
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

def onMouseRelease(app, mouseX, mouseY): # call deselect at the end?
    if app.cardGroup != None:
        cardGroupOnRelease(app, mouseX, mouseY)
    elif app.selectedCardInStack == True:
        stackCardsOnRelease(app, mouseX, mouseY)
    elif app.selectedCardInFoundation == True:
        foundationOnRelease(app, mouseX, mouseY)
    else:
        tableauOnRelease(app, mouseX, mouseY)

def cardGroupOnRelease(app, mouseX, mouseY):
    for col in range(7):
        for card in app.tableau[col]:
            if card == app.cardGroup.cards[0]:
                    colInd = 0
                    for (x1, x2) in app.colBounds:
                        if mouseX >= x1 and mouseX <= x2:
                            if checkGroupTableauLegality(app, app.cardGroup.cards, colInd) == True: 
                                for card in app.cardGroup.cards:
                                    app.tableau[col].pop()
                                    app.tableau[colInd].append(card)
                                    card.leftTopCornerX = x1
                                    card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 265 #magic nunbers?
                                return
                            else:
                                app.cardGroup.leftTopCornerX = app.cardGroup.prevLeftTopCornerX
                                app.cardGroup.leftTopCornerY = app.cardGroup.prevLeftTopCornerX 
                                for cd in app.cardGroup.cards:
                                    cd.leftTopCornerX = cd.prevLeftTopCornerX
                                    cd.leftTopCornerY = cd.prevLeftTopCornerY
                                return
                        colInd += 1

def stackCardsOnRelease(app, mouseX, mouseY):
    colInd = 0
    card = app.drawnStack[-1]
    for (x1, x2) in app.colBounds:
        if mouseX >= x1 and mouseX <= x2 and mouseY < 265 and colInd < 4: # move to 4 rects
            if checkFourRectsLegality(app, card, colInd):
                app.drawnStack.pop()
                app.foundations[colInd].append(card)
                card.leftTopCornerX = x1
                card.leftTopCornerY = 90
            else:
                card.leftTopCornerX = card.prevLeftTopCornerX
                card.leftTopCornerY = card.prevLeftTopCornerY
        elif mouseX >= x1 and mouseX <= x2 and mouseY >= 265: # move to tableau
            if checkSingleTableauLegality(app, card, colInd) == True:
                app.drawnStack.pop()
                app.tableau[colInd].append(card)
                card.leftTopCornerX = x1
                card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 265
            else:
                card.leftTopCornerX = card.prevLeftTopCornerX
                card.leftTopCornerY = card.prevLeftTopCornerY
        colInd += 1

def foundationOnRelease(app, mouseX, mouseY):
    card = None
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
                        card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 265
                    else:
                        card.leftTopCornerX = card.prevLeftTopCornerX
                        card.leftTopCornerY = card.prevLeftTopCornerY
                colInd += 1

def tableauOnRelease(app, mouseX, mouseY):
    for col in range(7):
        for card in app.tableau[col]:
            if card.selected == True:
                colInd = 0
                for (x1, x2) in app.colBounds:
                    if mouseX >= x1 and mouseX <= x2: # 4 rects 
                        if colInd < 4 and mouseY < 265:
                            if checkFourRectsLegality(app, card, colInd):
                                app.tableau[col].pop()
                                app.foundations[colInd].append(card)
                                card.leftTopCornerX = x1
                                card.leftTopCornerY = 90
                            else:
                                card.leftTopCornerX = card.prevLeftTopCornerX
                                card.leftTopCornerY = card.prevLeftTopCornerY
                            return
                        else: # tableau
                            if checkSingleTableauLegality(app, card, colInd) == True:
                                app.tableau[col].pop()
                                app.tableau[colInd].append(card)
                                card.leftTopCornerX = x1
                                card.leftTopCornerY = (len(app.tableau[colInd])-1)*50 + 265
                            else:
                                card.leftTopCornerX = card.prevLeftTopCornerX
                                card.leftTopCornerY = card.prevLeftTopCornerY
                            return
                    colInd += 1

def checkSingleTableauLegality(app, card, colInd):
    if len(app.tableau[colInd]) == 0:
        if card.number == 13:
            return True
        return False
    elif (app.tableau[colInd][-1].number == card.number and app.tableau[colInd][-1].suite == card.suite): # comment out
        return True
    elif (app.tableau[colInd][-1].color != card.color) and (app.tableau[colInd][-1].number == (card.number+1)):
        #print('true', app.tableau[colInd][-1], card)
        return True
    else:
        #print('false', app.tableau[colInd][-1], card)
        return False

def checkGroupTableauLegality(app, card, colInd):
    if len(app.tableau[colInd]) == 0:
        if card[0].number == 13:
            return True
        return False
    elif (app.tableau[colInd][-1].color != card[0].color) and (app.tableau[colInd][-1].number == (card[0].number+1)):
        #print('true', app.tableau[colInd][-1], card[0])
        return True
    else:
        #print('false', app.tableau[colInd][-1], card[0])
        return False

def checkFourRectsLegality(app, card, colInd):
    if len(app.foundations[colInd]) == 0:
        if card.number == 1:
            return True
        return False
    elif (app.foundations[colInd][-1].suite == card.suite and app.foundations[colInd][-1].number == (card.number-1)):
        return True
    else:
        return False

def getHint(app): # returns [] if nothing, draw card if stack not empty
    #maxNextMoves = 0
    #nextBestMove(app, maxNextMoves, bestMove)
    '''possMoveList = []
    hintStr = 'No possible next move'
    for col in range(7):
        cardInd = 0
        for card in app.tableau[col]: # add for tableau -> foundation and foundation -> tableau. If none, then draw. 
            if card.showBack == False:
                if cardInd != (len(app.tableau[col]) - 1): # group
                    possMove = findNextCol(app, card, col)
                    if possMove != None:
                        possMoveList.append(possMove)
                        hintStr = f'Move the {card.number} of {card.suite} group to col {possMove}'
                        print(hintStr)
                        return hintStr
                else: # single
                    possMove = findNextCol(app, card, col)
                    if possMove != None:
                        possMoveList.append(possMove)
                        hintStr = f'Move the {card.number} of {card.suite} to col {possMove}'
                        print(hintStr)
                        return hintStr
            cardInd += 1
    return hintStr'''
    possMoveList = []
    tableauHints = getTableauHints(app)
    stackHints = getStackHints(app)
    foundationHints = getFoundationHints(app)
    if tableauHints != []:
        possMoveList.extend(tableauHints)
    if stackHints != []:
        possMoveList.extend(stackHints)
    if foundationHints != []:
        possMoveList.extend(foundationHints)
    if possMoveList == [] and (len(app.stack) != 0 or len(app.drawnStack != 0)):
        possMoveList.append('Draw card')
    if possMoveList == [] and len(app.stack) == 0 and len(app.drawnStack == 0):
        possMoveList.append('No moves left')
    print(possMoveList)
    return possMoveList

def getTableauHints(app): 
    hints = []
    for col in range(7): # moves within tableau
        cardInd = 0
        for card in app.tableau[col]:  
            if (card.showBack == False) and (card.number != 13) and (card.number != 1):
                possMove = findTableauMove(app, card, col)
                if possMove != None:
                    #possMoveList.append(possMove)
                    if cardInd != (len(app.tableau[col]) - 1): # group
                        hintStr = f'Move the {card.number} of {card.suite} group in col {col} to col {possMove}'
                    else: # single
                        hintStr = f'Move the {card.number} of {card.suite} in col {col} to col {possMove}'
                    hints.append(hintStr)
                    if (cardInd > 0) and (app.tableau[possMove][-1].number == app.tableau[col][cardInd-1].number): # if move is redundant (Q, J -> Q, J)
                        print('redundant')
                        hints.pop()
            if (card.showBack == False) and (card.number == 13): # if king
                possMove = findEmptyCol(app)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to col {possMove}'
                    hints.append(hintStr)
            if (card.showBack == False) and (card.number == 1): # if ace
                possMove = findEmptyFoundation(app)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to foundation {possMove}'
                    hints.append(hintStr)
            if (card.showBack == False) and (card.number != 1): # move to foundation
                possMove = findFoundation(app, card)
                if possMove != None:
                    hintStr = f'Move the {card.number} of {card.suite} in col {col} to foundation {possMove}'
            cardInd += 1
    return hints

def getStackHints(app):
    hints = []
    if len(app.drawnStack) != 0:
        card = app.drawnStack[-1]
        possMove = findFoundation(app, card)
        if possMove != None:
            hintStr = f'Move the {card.number} of {card.suite} from the stack to foundation {possMove}'
            hints.append(hintStr)
        possMove = findTableauMove(app, card, -1)
        if possMove != None:
            hintStr = f'Move the {card.number} of {card.suite} from the stack to col {possMove}'
            hints.append(hintStr)
    return hints

def getFoundationHints(app):
    hints = []
    for col in range(4):
        if len(app.foundations[col]) > 0:
            card = app.foundations[col][-1]
            possMove = findTableauMove(app, card, -1)
            if possMove != None:
                hintStr = f'Move the {card.number} of {card.suite} from foundation {col} to col {possMove}'
                hints.append(hintStr)
    return hints

def findTableauMove(app, card, cardCol):
    for col in range(7): # within tableau
        if col == cardCol:
            continue
        cardInd = 0
        for cd in app.tableau[col]:
            if ((cd.showBack == False) and (cd.color != card.color) and 
                (cd.number == (card.number+1)) and cardInd == len(app.tableau[col])-1):
                return col
            cardInd += 1
    return None

def findEmptyCol(app):
    for col in range(7):
        if len(app.tableau[col]) == 0:
            return col

def findEmptyFoundation(app):
    for col in range(4):
        if len(app.foundations[col]) == 0:
            return col

def findFoundation(app, card):
    for col in range(4):
        if (len(app.foundations[col]) != 0 and app.foundations[col][-1].number == card.number-1 and 
            app.foundations[col][-1].suite == card.suite):
            return col

def nextBestMove(app, maxNextMoves, bestMove, level=0):
    if level == 2:
        return bestMove
    else:
        hints = getHint(app)
        for hint in hints:
            tryMove(app, hint)
            next = nextBestMove(app, maxNextMoves, bestMove, level+1)
            if next != None:
                pass

        # get hint list
        # loop through list
        # test each hint (modify the board to reflect each hint)
        # recurse nextBestMove
        # if nextBestMove != None
        #   if not level = 0, see if list length > maxNextMoves
        #   return nextBestMove
        # revert to last state
        # return None

# Move the {card.number} of {card.suite} from foundation {col} to col {possMove} 11 done
# Move the {card.number} of {card.suite} in col {col} to foundation {possMove} 11 done
# Move the {card.number} of {card.suite} in col {col} to col {possMove} 11 done

# Move the {card.number} of {card.suite} from the stack to col {possMove} 11 done
# Move the {card.number} of {card.suite} from the stack to foundation {possMove} 11
# Move the {card.number} of {card.suite} group in col {col} to col {possMove} 12 done

def tryMove(app, hint):
    hintList = list(hint)
    if len(hintList) == 12:
        moveCardGroup(app, hintList)
    else:
        if hintList[6] == 'foundation':
            moveFoundationToCol(app, hintList)
        elif hintList[6] == 'col' and hintList[9] == 'foundation':
            moveColToFoundation(app, hintList)
        elif hintList[6] == 'col' and hintList[9] == 'col':
            moveColToCol(app, hintList)
        elif hintList[7] == 'stack' and hintList[9] == 'col':
            moveStackToCol(app, hintList)
        elif hintList[6] == 'stack' and hintList[9] == 'foundation':
            moveStackToFoundation(app, hintList)

def moveCardGroup(app, hintList):
    app.prevTableau = app.tableau
    cardNum = hintList[2]
    cardSuite = hintList[4]
    cardGroupCol = hintList[8]
    newCol = hintList[11]
    cardInd = 0
    for card in app.tableau[cardGroupCol]:
        if cardNum == card.number and cardSuite == card.suite:
            cardGroup = app.tableau[cardGroupCol][cardInd:]
            for cd in cardGroup:
                app.tableau[cardGroupCol].pop()
                app.tableau[newCol].append(cd)
        cardInd += 1

def moveFoundationToCol(app, hintList):
    app.prevTableau = app.tableau
    app.prevFoundations = app.foundations
    app.testTableau = app.tableau
    app.testFoundations = app.foundations
    cardNum = hintList[2]
    cardSuite = hintList[4]
    foundCol = hintList[7]
    newCol = hintList[10]
    for card in app.testFoundations[foundCol]:
        if cardNum == card.number and cardSuite == card.suite:
            app.testFoundations[foundCol].pop()
            app.testTableau[newCol].append(card)

def moveColToFoundation(app, hintList):
    app.prevTableau = app.tableau
    app.prevFoundations = app.foundations
    app.testTableau = app.tableau
    app.testFoundations = app.foundations
    cardNum = hintList[2]
    cardSuite = hintList[4]
    cardCol = hintList[7]
    foundCol = hintList[10]
    for card in app.testTableau[cardCol]:
        if cardNum == card.number and cardSuite == card.suite:
            app.testTableau[cardCol].pop()
            app.testFoundations[foundCol].append(card)

def moveColToCol(app, hintList):
    app.prevTableau = app.tableau
    app.testTableau = app.tableau
    cardNum = hintList[2]
    cardSuite = hintList[4]
    cardCol = hintList[7]
    newCol = hintList[10]
    for card in app.testTableau[cardCol]:
        if cardNum == card.number and cardSuite == card.suite:
            app.testTableau[cardCol].pop()
            app.testTableau[newCol].append(card)

def moveStackToCol(app, hintList):
    app.prevDrawnStack = app.drawnStack
    app.prevTableau = app.tableau
    app.testDrawnStack = app.drawnStack
    app.testTableau = app.tableau
    newCol = hintList[10]
    card = app.testDrawnStack[-1]
    app.testDrawnStack.pop()
    app.testTableau[newCol].append(card)

def moveStackToFoundation(app, hintList):
    app.prevDrawnStack = app.drawnStack
    app.prevFoundations = app.foundations
    app.testDrawnStack = app.drawnStack
    app.testFoundations = app.foundations
    foundCol = hintList[10]
    card = app.testDrawnStack[-1]
    app.testDrawnStack.pop()
    app.testFoundations[foundCol].append(card)

def undoMove(app):
    pass

def main():
    runApp(width=2880, height=1800)

main()