from cmu_graphics import *
from PIL import Image, ImageGrab
import os, pathlib


# pieces
class Pawn:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whitePawn.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackPawn.png"))
        self.pastFirstMove = False
        self.name = "Pawn"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation, lastMove):
        if self.color == "white":
            if not self.pastFirstMove:
                if (
                    (currCol == newCol)
                    and (currRow - 2 == newRow)
                    and (pieceFormation[currRow - 1][currCol] == None)
                    and (pieceFormation[newRow][newCol] == None)
                ):
                    return True
            if (
                (currCol == newCol)
                and (currRow - 1 == newRow)
                and (pieceFormation[newRow][newCol] == None)
            ):
                return True
            if (
                (currRow - 1 == newRow)
                and ((newCol - 1 == currCol) or (newCol + 1 == currCol))
                and (pieceFormation[newRow][newCol] != None)
                and (pieceFormation[newRow][newCol].color == "black")
            ):
                return True
        elif self.color == "black":
            if not self.pastFirstMove:
                if (
                    (currCol == newCol)
                    and (currRow + 2 == newRow)
                    and (pieceFormation[currRow + 1][currCol] == None)
                    and (pieceFormation[newRow][newCol] == None)
                ):
                    return True
            if (
                (currCol == newCol)
                and (currRow + 1 == newRow)
                and (pieceFormation[newRow][newCol] == None)
            ):
                return True
            elif (
                (currRow + 1 == newRow)
                and ((newCol - 1 == currCol) or (newCol + 1 == currCol))
                and (pieceFormation[newRow][newCol] != None)
                and (pieceFormation[newRow][newCol].color == "white")
            ):
                return True
        if self.canCaptureEnPassant(
            currRow, currCol, newRow, newCol, lastMove, pieceFormation
        ):
            return True
        return False

    def canCaptureEnPassant(
        self, currRow, currCol, newRow, newCol, lastMove, pieceFormation
    ):
        if lastMove is None:
            return False

        if abs(lastMove["from"][0] - lastMove["to"][0]) == 2:
            direction = -1 if self.color == "white" else 1
            targetRow = currRow + direction
            enemyCol = lastMove["to"][1]
            if abs(currCol - enemyCol) == 1:
                if newRow == targetRow:
                    if newCol == lastMove["from"][1]:
                        return True
        return False


class Rook:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteRook.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackRook.png"))
        self.pastFirstMove = False
        self.name = "Rook"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
        if currRow != newRow and currCol != newCol:
            return False
        if currRow == newRow:
            startCol, endCol = sorted([currCol, newCol])
            for col in range(startCol + 1, endCol):
                if pieceFormation[currRow][col] != None:
                    return False
        elif currCol == newCol:
            startRow, endRow = sorted([currRow, newRow])
            for row in range(startRow + 1, endRow):
                if pieceFormation[row][currCol] != None:
                    return False
        endPiece = pieceFormation[newRow][newCol]
        if endPiece != None and endPiece.color == self.color:
            return False
        return True


class Knight:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteKnight.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackKnight.png"))
        self.name = "Knight"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
        if (pieceFormation[newRow][newCol] != None) and (
            pieceFormation[newRow][newCol].color == self.color
        ):
            return False
        if (
            ((currRow + 2 == newRow) and (currCol + 1 == newCol))
            or ((currRow - 2 == newRow) and (currCol + 1 == newCol))
            or ((currRow + 2 == newRow) and (currCol - 1 == newCol))
            or (
                (currRow - 2 == newRow)
                and (currCol - 1 == newCol)
                or ((currRow + 1 == newRow) and (currCol + 2 == newCol))
                or ((currRow + 1 == newRow) and (currCol - 2 == newCol))
                or ((currRow - 1 == newRow) and (currCol + 2 == newCol))
                or ((currRow - 1 == newRow) and (currCol - 2 == newCol))
            )
        ):
            return True
        return False


class Bishop:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteBishop.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackBishop.png"))
        self.name = "Bishop"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
        if (pieceFormation[newRow][newCol] != None) and (
            pieceFormation[newRow][newCol].color == self.color
        ):
            return False
        rowStep = 1 if newRow > currRow else -1
        colStep = 1 if newCol > currCol else -1
        checkRow, checkCol = currRow, currCol
        if abs(currRow - newRow) == abs(currCol - newCol):
            for _ in range(1, abs(currRow - newRow)):
                checkRow += rowStep
                checkCol += colStep
                if pieceFormation[checkRow][checkCol] != None:
                    return False
            return True
        return False


class Queen:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteQueen.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackQueen.png"))
        self.name = "Queen"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
        if (pieceFormation[newRow][newCol] != None) and (
            pieceFormation[newRow][newCol].color == self.color
        ):
            return False
        rowStep = 1 if newRow > currRow else -1
        colStep = 1 if newCol > currCol else -1
        checkRow, checkCol = currRow, currCol
        if abs(currRow - newRow) == abs(currCol - newCol):
            for _ in range(1, abs(currRow - newRow)):
                checkRow += rowStep
                checkCol += colStep
                if pieceFormation[checkRow][checkCol] != None:
                    return False
            return True
        elif currRow == newRow:
            startCol, endCol = sorted([currCol, newCol])
            for col in range(startCol + 1, endCol):
                if pieceFormation[currRow][col] != None:
                    return False
            return True
        elif currCol == newCol:
            startRow, endRow = sorted([currRow, newRow])
            for row in range(startRow + 1, endRow):
                if pieceFormation[row][currCol] != None:
                    return False
            return True
        return False


class King:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteKing.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackKing.png"))
        self.pastFirstMove = False
        self.name = "King"

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
        if (pieceFormation[newRow][newCol] != None) and (
            pieceFormation[newRow][newCol].color == self.color
        ):
            return False
        if (
            ((currRow + 1 == newRow) and (currCol == newCol))
            or ((currRow + 1 == newRow) and (currCol + 1 == newCol))
            or ((currRow + 1 == newRow) and (currCol - 1 == newCol))
            or ((currRow - 1 == newRow) and (currCol == newCol))
            or ((currRow - 1 == newRow) and (currCol + 1 == newCol))
            or ((currRow - 1 == newRow) and (currCol - 1 == newCol))
            or ((currRow == newRow) and (currCol + 1 == newCol))
            or ((currRow == newRow) and (currCol - 1 == newCol))
        ):
            return True
        # king-side castle legality
        if (
            (not self.pastFirstMove)
            and (currRow == newRow)
            and (currCol + 2 == newCol)
            and (pieceFormation[currRow][currCol + 1] == None)
            and (pieceFormation[currRow][currCol + 2] == None)
            and isinstance(pieceFormation[currRow][currCol + 3], Rook)
            and (not pieceFormation[currRow][currCol + 3].pastFirstMove)
        ):
            return True
        # queen-side castle legality
        elif (
            (not self.pastFirstMove)
            and (currRow == newRow)
            and (currCol - 2 == newCol)
            and (pieceFormation[currRow][currCol - 1] == None)
            and (pieceFormation[currRow][currCol - 2] == None)
            and (pieceFormation[currRow][currCol - 3] == None)
            and isinstance(pieceFormation[currRow][currCol - 4], Rook)
            and (not pieceFormation[currRow][currCol - 4].pastFirstMove)
        ):
            return True
        return False


# cells
class Cell:
    def __init__(self, color, xPos, yPos, size):
        self.color = color
        self.size = size
        self.xPos = xPos
        self.yPos = yPos


def getOpeningCellFormat(x, y, size):
    grid = []
    startColor = "white"
    xCoord = x
    yCoord = y
    for row in range(8):
        grid.append([])
        currColor = startColor
        for _ in range(8):
            grid[row].append(Cell(currColor, xCoord, yCoord, size))
            currColor = "black" if currColor == "white" else "white"
            xCoord += size
        startColor = "black" if startColor == "white" else "white"
        xCoord = x
        yCoord += size
    return grid


def getOpeningPieceFormat():
    return [
        [
            Rook("black"),
            Knight("black"),
            Bishop("black"),
            Queen("black"),
            King("black"),
            Bishop("black"),
            Knight("black"),
            Rook("black"),
        ],
        [Pawn("black") for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [Pawn("white") for _ in range(8)],
        [
            Rook("white"),
            Knight("white"),
            Bishop("white"),
            Queen("white"),
            King("white"),
            Bishop("white"),
            Knight("white"),
            Rook("white"),
        ],
    ]


# board
class Board:
    def __init__(self, x, y, size):
        self.topX = x
        self.topY = y
        self.size = size
        self.turn = "white"
        self.inCheckmate = False

        self.cellFormation = getOpeningCellFormat(self.topX, self.topY, size / 8)
        self.pieceFormation = getOpeningPieceFormat()

        self.cellSelected = False
        self.cellSelectedCoords = None
        self.cellSelectedCol = None

        self.whiteCaptured = []
        self.blackCaptured = []
        self.moves = {}
        self.moveCount = 1
        self.squareNames = [
            ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"],
            ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
            ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
            ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
            ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
            ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
            ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
            ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"],
        ]

        self.lastMove = None

    def draw(self):
        border = 10

        # draw background
        drawRect(
            self.topX - border,
            self.topY - border,
            self.size + 2 * border,
            self.size + 2 * border,
            fill="white",
            border="black",
            borderWidth=5,
        )
        # draw cells
        for row in range(len(self.cellFormation)):
            for col in range(len(self.cellFormation[row])):
                cell = self.cellFormation[row][col]
                drawRect(
                    cell.xPos,
                    cell.yPos,
                    cell.size,
                    cell.size,
                    fill=cell.color,
                )

    def drawPieces(self):
        lenOfCell = self.size / 8
        for row in range(len(self.pieceFormation)):
            for col in range(len(self.pieceFormation[row])):
                piece = self.pieceFormation[row][col]
                if piece:
                    x = self.topX + col * lenOfCell + lenOfCell / 2
                    y = self.topY + row * lenOfCell + lenOfCell / 2

                    drawImage(
                        piece.image,
                        x,
                        y,
                        width=lenOfCell * 0.75,
                        height=lenOfCell * 0.75,
                        align="center",
                    )


def move(app, newRow, newCol):
    currRow, currCol = app.testBoard.cellSelectedCoords
    if (0 <= currRow < 8 and 0 <= currCol < 8) and (
        0 <= newRow < 8 and 0 <= newCol < 8
    ):
        piece = app.testBoard.pieceFormation[currRow][currCol]
        legalMove = (
            piece.isLegalMove(
                currRow,
                currCol,
                newRow,
                newCol,
                app.testBoard.pieceFormation,
                app.testBoard.lastMove,
            )
            if isinstance(piece, Pawn)
            else piece.isLegalMove(
                currRow, currCol, newRow, newCol, app.testBoard.pieceFormation
            )
        )
        if piece and legalMove:
            if (
                piece.color == "white"
                and app.testBoard.pieceFormation[newRow][newCol] != None
            ):
                app.testBoard.blackCaptured.append(
                    app.testBoard.pieceFormation[newRow][newCol].name
                )
            elif (
                piece.color == "black"
                and app.testBoard.pieceFormation[newRow][newCol] != None
            ):
                app.testBoard.whiteCaptured.append(
                    app.testBoard.pieceFormation[newRow][newCol].name
                )
            app.testBoard.moves[
                f"{app.testBoard.moveCount}. {app.testBoard.pieceFormation[currRow][currCol].color} Move"
            ] = f"{app.testBoard.pieceFormation[currRow][currCol].name} moved from {app.testBoard.squareNames[currRow][currCol]} to {app.testBoard.squareNames[newRow][newCol]}"

            app.testBoard.pieceFormation[newRow][newCol] = piece
            app.testBoard.pieceFormation[currRow][currCol] = None

            # Check for en passant
            if isinstance(piece, Pawn):
                canCaptureEP = piece.canCaptureEnPassant(
                    currRow,
                    currCol,
                    newRow,
                    newCol,
                    app.testBoard.lastMove,
                    app.testBoard.pieceFormation,
                )
                if canCaptureEP:
                    if piece.color == "white":
                        captureRow = newRow + 1
                    else:
                        captureRow = newRow - 1
                    app.testBoard.pieceFormation[captureRow][newCol] = None
                    app.testBoard.pieceFormation[newRow][newCol] = piece
                    app.testBoard.pieceFormation[currRow][currCol] = None
                    piece.pastFirstMove = True

            if not isKingInCheck(
                app.testBoard.turn, app.testBoard.pieceFormation, app.testBoard.lastMove
            ):
                app.testBoard.turn = (
                    "black" if app.testBoard.turn == "white" else "white"
                )
                if isinstance(piece, Pawn) and not piece.pastFirstMove:
                    piece.pastFirstMove = True

                app.testBoard.lastMove = {
                    "piece": piece,
                    "from": (currRow, currCol),
                    "to": (newRow, newCol),
                }
            else:
                app.testBoard.pieceFormation[currRow][currCol] = piece
                app.testBoard.pieceFormation[newRow][newCol] = None

                if piece.color == "white" and app.testBoard.blackCaptured != []:
                    app.testBoard.blackCaptured.pop()
                elif piece.color == "black" and app.test.whiteCaptured != []:
                    app.testBoard.whiteCaptured.pop()
                app.testBoard.moves.pop(
                    f"{app.testBoard.moveCount}. {app.testBoard[currRow][currCol].color} Move"
                )
    app.testBoard.moveCount += 1
    print(f"Moves: {app.testBoard.moves}")


def getPieceColor(piece):
    if piece.startswith("white"):
        return "white"
    elif piece.startswith("black"):
        return "black"
    else:
        return None


def isKingInCheck(kingColor, pieceFormation, lastMove):
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (type(pieceFormation[i][j]) == King) and (
                pieceFormation[i][j].color == kingColor
            ):
                kingPos = (i, j)
    opponentColor = "black" if kingColor == "white" else "white"
    opponentMoves = getAllLegalMoves(opponentColor, pieceFormation, lastMove)
    return kingPos in opponentMoves


def getAllLegalMoves(playerColor, pieceFormation, lastMove):
    legalMoves = []
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (pieceFormation[i][j] != None) and (
                pieceFormation[i][j].color == playerColor
            ):
                for x in range(8):
                    for y in range(8):
                        if isinstance(pieceFormation[i][j], Pawn):
                            if pieceFormation[i][j].isLegalMove(
                                i, j, x, y, pieceFormation, lastMove
                            ):
                                legalMoves.append((x, y))
                        else:
                            if pieceFormation[i][j].isLegalMove(
                                i, j, x, y, pieceFormation
                            ):
                                legalMoves.append((x, y))
    return legalMoves


def getKingLegalMoves(kingColor, pieceFormation, lastMove):
    legalMoves = []
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            piece = pieceFormation[i][j]
            if isinstance(piece, King) and piece.color == kingColor:
                for x in range(8):
                    for y in range(8):
                        if piece.isLegalMove(
                            i, j, x, y, pieceFormation
                        ) and not resultsInCheck(kingColor, pieceFormation, i, j, x, y):
                            legalMoves.append((x, y))
    return legalMoves


def resultsInCheck(kingColor, pieceFormation, currRow, currCol, newRow, newCol):
    tempBoard = [row[:] for row in pieceFormation]
    tempBoard[newRow][newCol] = tempBoard[currRow][currCol]
    tempBoard[currRow][currCol] = None
    return isKingInCheck(kingColor, tempBoard, None)


def onAppStart(app):
    app.testBoard = Board(app.width / 1.5, app.height / 4, 800)


def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))


def onMousePress(app, mouseX, mouseY):
    for row in range(len(app.testBoard.cellFormation)):
        for col in range(len(app.testBoard.cellFormation[row])):
            cell = app.testBoard.cellFormation[row][col]
            if (cell.xPos <= mouseX <= cell.xPos + cell.size) and (
                cell.yPos <= mouseY <= cell.yPos + cell.size
            ):
                if app.testBoard.cellSelected:
                    if app.testBoard.cellSelectedCoords == (row, col):
                        cell.color = app.testBoard.cellSelectedCol
                        app.testBoard.cellSelected = False
                        app.testBoard.cellSelectedCoords = None
                    else:
                        prevRow, prevCol = app.testBoard.cellSelectedCoords
                        move(app, row, col)
                        app.testBoard.cellFormation[prevRow][
                            prevCol
                        ].color = app.testBoard.cellSelectedCol
                        app.testBoard.cellSelected = False
                        app.testBoard.cellSelectedCoords = None
                elif (app.testBoard.pieceFormation[row][col] != None) and (
                    app.testBoard.pieceFormation[row][col].color == app.testBoard.turn
                ):
                    app.testBoard.cellSelectedCol = cell.color
                    cell.color = "pink"
                    app.testBoard.cellSelected = True
                    app.testBoard.cellSelectedCoords = (row, col)


def onKeyPress(app, key):
    if key == "r":
        app.testBoard.pieceFormation = getOpeningPieceFormat()
        app.testBoard.turn = "white"
        app.testBoard.inCheckmate = False
        app.testBoard.blackCaptured = []
        app.testBoard.whiteCaptured = []


def redrawAll(app):
    app.testBoard.draw()
    app.testBoard.drawPieces()
    drawLabel("Press 'r' to reset game", app.width / 2, app.height * 0.95, bold=True)
    if app.testBoard.inCheckmate:
        drawLabel("Checkmate", app.width / 2, app.height / 12, bold=True)

    # Captured Pieces display
    drawRect(0, app.height * 0.1, app.width / 7, app.height * 0.85, fill="gray")
    drawLabel(
        "White's Captured Pieces:",
        app.width / 15,
        app.height * 0.12,
        fill="white",
        bold=True,
    )
    drawLabel(
        "Black's Captured Pieces:",
        app.width / 15,
        app.height * 0.53,
        fill="black",
        bold=True,
    )

    counter = 0.15
    for piece in app.testBoard.whiteCaptured:
        drawLabel(piece, app.width / 15, app.height * counter, fill="white")
        counter += 0.02
    counter = 0.55
    for piece in app.testBoard.blackCaptured:
        drawLabel(piece, app.width / 15, app.height * counter, fill="black")
        counter += 0.02


def main():
    runApp()


main()

# CITATIONS:
# chess pieces images sourced from:
# [1] “Category:PNG Chess Pieces/Standard Transparent,” Wikimedia Commons, https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent (accessed Nov. 27, 2023).
