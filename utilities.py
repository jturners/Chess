from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from cell import Cell


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


def isKingInCheck(kingColor, pieceFormation, lastMove):
    print(f"Checking if {kingColor} king is in check...")
    kingPos = None

    # Find the king's position
    for i in range(len(pieceFormation)):
        for j in range(len(pieceFormation[i])):
            if (
                isinstance(pieceFormation[i][j], King)
                and pieceFormation[i][j].color == kingColor
            ):
                kingPos = (i, j)
                break
    opponentColor = "black" if kingColor == "white" else "white"
    return kingPos in getAllLegalMoves(opponentColor, pieceFormation, lastMove)


def getAllLegalMoves(playerColor, pieceFormation, lastMove):
    print(f"Getting all legal moves for {playerColor}")

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


def resultsInCheck(kingColor, pieceFormation, currRow, currCol, newRow, newCol):
    # Simulate the move
    movedPiece = pieceFormation[currRow][currCol]
    capturedPiece = pieceFormation[newRow][newCol]

    pieceFormation[newRow][newCol] = movedPiece
    pieceFormation[currRow][currCol] = None

    # Check if the king is in check after the move
    inCheck = isKingInCheck(kingColor, pieceFormation, None)

    if not inCheck:
        print(f"stupid piece is {pieceFormation[newRow][newCol]}")
    # Undo the move
    pieceFormation[currRow][currCol] = movedPiece
    pieceFormation[newRow][newCol] = capturedPiece

    return inCheck
