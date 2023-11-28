from cmu_graphics import *
from PIL import Image
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

    def isLegalMove(self, currRow, currCol, newRow, newCol, pieceFormation):
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
        return False


class Rook:
    def __init__(self, color):
        self.color = color
        if self.color == "white":
            self.image = CMUImage(openImage("whiteRook.png"))
        elif self.color == "black":
            self.image = CMUImage(openImage("blackRook.png"))
        self.pastFirstMove = False

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

        self.cellFormation = getOpeningCellFormat(self.topX, self.topY, size / 8)
        self.pieceFormation = getOpeningPieceFormat()

        self.cellSelected = False
        self.cellSelectedCoords = None
        self.cellSelectedCol = None

        self.whiteCaptured = []
        self.blackCaptured = []

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

        # draw pieces w words
        # x = self.topX
        # y = self.topY
        # for row in range(len(self.pieceFormation)):
        #     for col in range(len(self.pieceFormation[row])):
        #         piece = self.pieceFormation[row][col]
        #         if piece:
        #             drawLabel(piece, x + lenOfCell / 2, y + lenOfCell / 2)
        #         x += lenOfCell
        #     y += lenOfCell
        #     x = self.topX

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
    print("here")
    currRow, currCol = app.testBoard.cellSelectedCoords
    if (0 <= currRow < 8 and 0 <= currCol < 8) and (
        0 <= newRow < 8 and 0 <= newCol < 8
    ):
        print(
            f"Attempting to move pice from ({currRow}, {currCol}) to ({newRow}, {newCol})"
        )
        piece = app.testBoard.pieceFormation[currRow][currCol]
        if piece and piece.isLegalMove(
            currRow, currCol, newRow, newCol, app.testBoard.pieceFormation
        ):
            print(
                f"Move is legal. Moving piece: {piece.__class__.__name__}, Color: {piece.color}"
            )
            app.testBoard.pieceFormation[newRow][newCol] = piece
            app.testBoard.pieceFormation[currRow][currCol] = None
            if not isKingInCheck(app.testBoard.turn, app.testBoard.pieceFormation):
                app.testBoard.turn = (
                    "black" if app.testBoard.turn == "white" else "white"
                )

                if isinstance(piece, King) and currCol == 4 and newCol == 6:
                    app.testBoard.pieceFormation[currRow][
                        currCol + 1
                    ] = app.testBoard.pieceFormation[currRow][currCol + 3]
                    app.testBoard.pieceFormation[currRow][currCol + 3] = None
                    app.testBoard.pieceFormation[currRow][currCol + 2] = piece
                    app.testBoard.pieceFormation[currRow][currCol] = None
                elif isinstance(piece, King) and currCol == 4 and newCol == 2:
                    app.testBoard.pieceFormation[currRow][
                        currCol - 1
                    ] = app.testBoard.pieceFormation[currRow][currCol - 4]
                    app.testBoard.pieceFormation[currRow][currCol - 4] = None
                    app.testBoard.pieceFormation[currRow][currCol - 2] = piece
                    app.testBoard.pieceFormation[currRow][currCol] = None

                if isinstance(piece, Pawn) and not piece.pastFirstMove:
                    piece.pastFirstMove = True
                elif isinstance(piece, Rook) and not piece.pastFirstMove:
                    piece.pastFirstMove = True
                elif isinstance(piece, King) and not piece.pastFirstMove:
                    piece.pastFirstMove = True
            else:
                app.testBoard.pieceFormation[currRow][currCol] = piece
                app.testBoard.pieceFormation[newRow][newCol] = None


def getPieceColor(piece):
    if piece.startswith("white"):
        return "white"
    elif piece.startswith("black"):
        return "black"
    else:
        return None


def isKingInCheck(kingColor, pieceFormation):
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (type(pieceFormation[i][j]) == King) and (
                pieceFormation[i][j].color == kingColor
            ):
                kingPos = (i, j)
    playerColor = "black" if kingColor == "white" else "white"
    opponentMoves = getAllLegalMoves(playerColor, pieceFormation)
    return kingPos in opponentMoves


def getAllLegalMoves(playerColor, pieceFormation):
    legalMoves = []
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (pieceFormation[i][j] != None) and (
                pieceFormation[i][j].color == playerColor
            ):
                for x in range(8):
                    for y in range(8):
                        if pieceFormation[i][j].isLegalMove(i, j, x, y, pieceFormation):
                            legalMoves.append((x, y))
    return legalMoves


def onAppStart(app):
    app.testBoard = Board(app.width / 1.5, app.height / 4, 800)

    # # loading images
    # app.wPawn = CMUImage(openImage("whitePawn.png"))
    # app.bPawn = CMUImage(openImage("blackPawn.png"))
    # app.wRook = CMUImage(openImage("whiteRook.png"))
    # app.bRook = CMUImage(openImage("blackRook.png"))
    # app.wKnight = CMUImage(openImage("whiteKnight.png"))
    # app.bKnight = CMUImage(openImage("blackKnight.png"))
    # app.wBishop = CMUImage(openImage("whiteBishop.png"))
    # app.bBishop = CMUImage(openImage("blackBishop.png"))
    # app.wQueen = CMUImage(openImage("whiteQueen.png"))
    # app.bQueen = CMUImage(openImage("blackQueen.png"))
    # app.wKing = CMUImage(openImage("whiteKing.png"))
    # app.bKing = CMUImage(openImage("blackKing.png"))


def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))


def onMousePress(app, mouseX, mouseY):
    print(f"Mouse clicked at: ({mouseX}, {mouseY})")
    for row in range(len(app.testBoard.cellFormation)):
        for col in range(len(app.testBoard.cellFormation[row])):
            cell = app.testBoard.cellFormation[row][col]
            if (cell.xPos <= mouseX <= cell.xPos + cell.size) and (
                cell.yPos <= mouseY <= cell.yPos + cell.size
            ):
                print(f"Clicked cell: ({row}, {col})")

                # If a piece is already selected
                if app.testBoard.cellSelected:
                    # If clicking the same cell again, unselect it
                    if app.testBoard.cellSelectedCoords == (row, col):
                        cell.color = app.testBoard.cellSelectedCol
                        app.testBoard.cellSelected = False
                        app.testBoard.cellSelectedCoords = None
                    else:
                        # Attempt to move the selected piece to the new cell
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
                    # Selecting a new piece
                    print(
                        f"Piece at clicked cell: {app.testBoard.pieceFormation[row][col].__class__.__name__}, Color: {app.testBoard.pieceFormation[row][col].color}"
                    )
                    app.testBoard.cellSelectedCol = cell.color
                    cell.color = "pink"
                    app.testBoard.cellSelected = True
                    app.testBoard.cellSelectedCoords = (row, col)


def onKeyPress(app, key):
    if key == "r":
        app.testBoard.pieceFormation = getOpeningPieceFormat()
        app.testBoard.turn = "white"


def redrawAll(app):
    app.testBoard.draw()
    app.testBoard.drawPieces()
    drawLabel("Press 'r' to reset game", app.width / 2, app.height * 0.95, bold=True)


def main():
    runApp()


main()

# CITATIONS:
# chess pieces images sourced from:
# [1] “Category:PNG Chess Pieces/Standard Transparent,” Wikimedia Commons, https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent (accessed Nov. 27, 2023).
