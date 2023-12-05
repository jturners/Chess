from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from cell import Cell
from utilities import getOpeningCellFormat, getOpeningPieceFormat
from cmu_graphics import *


class Board:
    def __init__(self, x, y, size):
        self.topX = x
        self.topY = y
        self.size = size
        self.turn = "white"
        self.inCheckmate = False

        self.cellFormation = getOpeningCellFormat(
            self.topX, self.topY, self.size / 8
        )  # /8 because 8x8 grid
        self.pieceFormation = getOpeningPieceFormat()

        self.cellSelected = False
        self.cellSelectedCoords = None
        self.cellSelectedCol = None

        self.whiteCaptured = []
        self.blackCaptured = []
        self.moves = {}
        self.moveCount = 0
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

        self.whiteScore = 1290
        self.blackScore = 1290

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
        lenOfCell = self.size / 8  # /8 because 8x8 grid
        for row in range(len(self.pieceFormation)):
            for col in range(len(self.pieceFormation[row])):
                piece = self.pieceFormation[row][col]
                if piece:
                    x = self.topX + col * lenOfCell + lenOfCell / 2
                    y = self.topY + row * lenOfCell + lenOfCell / 2
                    imageReductionScalar = 0.75
                    drawImage(
                        piece.image,
                        x,
                        y,
                        width=lenOfCell * imageReductionScalar,
                        height=lenOfCell * imageReductionScalar,
                        align="center",
                    )


def copyBoard(originalBoard):
    boardCopy = Board(originalBoard.topX, originalBoard.topY, originalBoard.size)
    boardCopy.turn = originalBoard.turn
    boardCopy.moves = originalBoard.moves
    boardCopy.inCheckmate = originalBoard.inCheckmate
    boardCopy.cellSelected = originalBoard.cellSelected
    boardCopy.cellSelectedCol = originalBoard.cellSelectedCol
    boardCopy.cellSelectedCoords = originalBoard.cellSelectedCoords
    boardCopy.whiteCaptured = originalBoard.whiteCaptured
    boardCopy.blackCaptured = originalBoard.blackCaptured
    boardCopy.moveCount = originalBoard.moveCount
    boardCopy.lastMove = originalBoard.lastMove
    boardCopy.whiteScore = originalBoard.whiteScore
    boardCopy.blackScore = originalBoard.blackScore
    boardCopy.pieceFormation = []
    for row in originalBoard.pieceFormation:
        newRow = []
        for piece in row:
            if piece == None:
                newRow.append(None)
            else:
                pieceType = type(piece)
                newPiece = pieceType(piece.color)
                newRow.append(newPiece)
        boardCopy.pieceFormation.append(newRow)

    return boardCopy
