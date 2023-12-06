from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from cell import Cell
from cmu_graphics import *


def getOpeningCellFormat(x, y, size):
    grid = []
    whiteColor = rgb(244, 238, 226)
    blackColor = rgb(35, 128, 49)
    startColor = whiteColor
    xCoord = x
    yCoord = y
    for row in range(8):
        grid.append([])
        currColor = startColor
        for _ in range(8):
            grid[row].append(Cell(currColor, xCoord, yCoord, size))
            currColor = blackColor if currColor == whiteColor else whiteColor
            xCoord += size
        startColor = blackColor if startColor == whiteColor else whiteColor
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


def isKingInCheck(kingColor, pieceFormation, lastMove):
    kingPos = None
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (
                isinstance(pieceFormation[i][j], King)
                and pieceFormation[i][j].color == kingColor
            ):
                kingPos = (i, j)
                break
    opponentColor = "black" if kingColor == "white" else "white"
    return kingPos in getAllPotentialMoves(opponentColor, pieceFormation, lastMove)


def getAllLegalMoves(playerColor, pieceFormation, lastMove):
    legalMoves = []
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            piece = pieceFormation[i][j]
            if piece != None and piece.color == playerColor:
                for x in range(8):
                    for y in range(8):
                        legalMove = (
                            piece.isLegalMove(i, j, x, y, pieceFormation, lastMove)
                            if isinstance(piece, Pawn)
                            else piece.isLegalMove(i, j, x, y, pieceFormation)
                        )
                        if legalMove:
                            originalPiece = pieceFormation[x][y]
                            pieceFormation[x][y] = piece
                            pieceFormation[i][j] = None

                            if not isKingInCheck(playerColor, pieceFormation, lastMove):
                                legalMoves.append((i, j, x, y))

                            pieceFormation[i][j] = piece
                            pieceFormation[x][y] = originalPiece
    return legalMoves


def resultsInCheck(kingColor, pieceFormation, currRow, currCol, newRow, newCol):
    movedPiece = pieceFormation[currRow][currCol]
    capturedPiece = pieceFormation[newRow][newCol]

    pieceFormation[newRow][newCol] = movedPiece
    pieceFormation[currRow][currCol] = None

    inCheck = isKingInCheck(kingColor, pieceFormation, None)

    pieceFormation[currRow][currCol] = movedPiece
    pieceFormation[newRow][newCol] = capturedPiece

    return inCheck


def getAllPotentialMoves(playerColor, pieceFormation, lastMove):
    potentialMoves = []
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            piece = pieceFormation[i][j]
            if piece is not None and piece.color == playerColor:
                for x in range(8):
                    for y in range(8):
                        if isinstance(piece, Pawn):
                            if piece.isLegalMove(i, j, x, y, pieceFormation, lastMove):
                                potentialMoves.append((x, y))
                        else:
                            if piece.isLegalMove(i, j, x, y, pieceFormation):
                                potentialMoves.append((x, y))
    return potentialMoves
