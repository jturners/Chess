import random
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from utilities import getAllLegalMoves


def aiMove(board, aiColor):
    maximizingPlayer = True
    depth = 4
    alpha = -float("inf")
    beta = float("inf")
    aiMove = miniMax(board, aiColor, maximizingPlayer, depth, alpha, beta)[0]
    return aiMove


def miniMax(board, maximizingColor, maximizingPlayer, depth, alpha, beta):
    if depth == 0 or board.inCheckmate:
        evalScore = evaluatePosition(board, maximizingColor)
        return None, evalScore
    moves = getAllLegalMoves(maximizingColor, board.pieceFormation, board.lastMove)
    if moves == []:
        evalScore = -float("inf") if maximizingPlayer else float("inf")
        return None, evalScore
    bestMove = moves[0]

    if maximizingPlayer:
        maxEval = -float("inf")
        for move in moves:
            originalRow, originalCol, testRow, testCol = move
            pieceAtOriginal = board.pieceFormation[originalRow][originalCol]
            pieceAtTest = board.pieceFormation[testRow][testCol]
            board.pieceFormation[testRow][testCol] = board.pieceFormation[originalRow][
                originalCol
            ]
            board.pieceFormation[originalRow][originalCol] = None

            currEval = miniMax(board, maximizingColor, False, depth - 1, alpha, beta)[1]

            board.pieceFormation[originalRow][originalCol] = pieceAtTest
            board.pieceFormation[testRow][testCol] = pieceAtOriginal

            if currEval > maxEval:
                maxEval = currEval
                bestMove = move
            alpha = max(alpha, currEval)
            if beta <= alpha:
                break
        return bestMove, maxEval

    else:
        minEval = float("inf")
        for move in moves:
            originalRow, originalCol, testRow, testCol = move
            pieceAtOriginal = board.pieceFormation[originalRow][originalCol]
            pieceAtTest = board.pieceFormation[testRow][testCol]
            board.pieceFormation[testRow][testCol] = board.pieceFormation[originalRow][
                originalCol
            ]
            board.pieceFormation[originalRow][originalCol] = None

            currEval = miniMax(board, maximizingColor, True, depth - 1, alpha, beta)[1]

            board.pieceFormation[originalRow][originalCol] = pieceAtTest
            board.pieceFormation[testRow][testCol] = pieceAtOriginal

            if currEval < minEval:
                minEval = currEval
                bestMove = move
            beta = max(beta, currEval)
            if beta <= alpha:
                break
        return bestMove, minEval


def evaluatePosition(board, maximizingColor):
    if maximizingColor == "white":
        pieceScore = board.whiteScore - board.blackScore
    else:
        pieceScore = board.blackScore - board.whiteScore

    opponentColor = "black" if maximizingColor == "white" else "white"
    myMoves = getAllLegalMoves(maximizingColor, board.pieceFormation, board.lastMove)
    opponentMoves = getAllLegalMoves(
        opponentColor, board.pieceFormation, board.lastMove
    )

    if opponentMoves == []:
        return -float("inf")

    positionScore, threatScore, centerControlScore, kingSafetyScore, capturingScore = (
        0,
        0,
        0,
        0,
        0,
    )

    for move in myMoves:
        _, _, toRow, toCol = move
        if (
            board.pieceFormation[toRow][toCol] != None
            and board.pieceFormation[toRow][toCol].color == opponentColor
        ):
            capturingScore += board.pieceFormation[toRow][toCol].weight

    for row in range(8):
        for col in range(8):
            piece = board.pieceFormation[row][col]
            if piece != None and piece.color == maximizingColor:
                if isinstance(piece, Pawn):
                    positionScore += pawnPositionScore(row, piece.color)
                elif isinstance(piece, Knight):
                    positionScore += knightPositionScore(row, col)
                if (row, col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                    centerControlScore += 0.5
                if isinstance(piece, King) and (col <= 2 or col >= 5):
                    kingSafetyScore += 1
            if (
                piece != None
                and piece.color != maximizingColor
                and (row, col) in opponentMoves
            ):
                threatScore += piece.weight * 0.5

    checkmateScore = 0
    if board.inCheckmate:
        checkmateScore = 1000 if board.turn != maximizingColor else -1000

    totalScore = (
        pieceScore
        + positionScore
        - threatScore
        + centerControlScore
        + kingSafetyScore
        + checkmateScore
        + capturingScore
    )
    return totalScore


def pawnPositionScore(row, color):
    if color == "white":
        return row
    else:
        return 7 - row


def knightPositionScore(row, col):
    centerSquares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    almostCenterSquares = [
        (2, 2),
        (2, 5),
        (5, 2),
        (5, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
    ]
    if (row, col) in centerSquares:
        return 3  # incentivising knight development to the center
    elif (row, col) in almostCenterSquares:
        return 1.5
    else:
        return 0
