from cmu_graphics import CMUImage
from PIL import Image
import os, pathlib


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
            and (currCol + 3 < 8)
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
            and (currCol - 4 >= 0)
            and isinstance(pieceFormation[currRow][currCol - 4], Rook)
            and (not pieceFormation[currRow][currCol - 4].pastFirstMove)
        ):
            return True
        return False


def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent, fileName))
