import random
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from utilities import getAllLegalMoves


def aiMove(board, aiColor):
    print(f"aiMove called with color: {aiColor}")
    maximizingPlayer = True
    depth = 4
    alpha = -float("inf")
    beta = float("inf")
    aiMove = miniMax(board, aiColor, maximizingPlayer, depth, alpha, beta)[0]
    print(f"aiMove returning: {aiMove}")
    return aiMove


def miniMax(board, maximizingColor, maximizingPlayer, depth, alpha, beta):
    print(
        f"miniMax called: color={maximizingColor}, player={maximizingPlayer}, depth={depth}"
    )
    if depth == 0 or board.inCheckmate:
        evalScore = evaluatePosition(board, maximizingColor)
        print(f"Base case reached: eval_score = {evalScore}")
        return None, evalScore
    moves = getAllLegalMovesFromPos(
        maximizingColor, board.pieceFormation, board.lastMove
    )
    bestMove = moves[0]

    if maximizingPlayer:
        maxEval = -float("inf")
        for move in moves:
            originalRow, originalCol, testRow, testCol = move
            board.pieceFormation[testRow][testCol] = board.pieceFormation[originalRow][
                originalCol
            ]
            board.pieceFormation[originalRow][originalCol] = None

            currEval = miniMax(board, maximizingColor, False, depth - 1, alpha, beta)[1]

            board.pieceFormation[originalRow][originalCol] = board.pieceFormation[
                testRow
            ][testCol]
            board.pieceFormation[testRow][testCol] = None

            if currEval > maxEval:
                maxEval = currEval
                bestMove = move
            alpha = max(alpha, currEval)
            if beta <= alpha:
                break
        print(f"MaximizingPlayer, bestMove = {bestMove}, maxEval = {maxEval}")
        return bestMove, maxEval

    else:
        minEval = float("inf")
        for move in moves:
            originalRow, originalCol, testRow, testCol = move
            board.pieceFormation[testRow][testCol] = board.pieceFormation[originalRow][
                originalCol
            ]
            board.pieceFormation[originalRow][originalCol] = None

            currEval = miniMax(board, maximizingColor, True, depth - 1, alpha, beta)[1]

            board.pieceFormation[originalRow][originalCol] = board.pieceFormation[
                testRow
            ][testCol]
            board.pieceFormation[testRow][testCol] = None

            if currEval < minEval:
                minEval = currEval
                bestMove = move
            beta = max(beta, currEval)
            if beta <= alpha:
                break
        print(f"MinimizingPlayer, bestMove = {bestMove}, minEval = {minEval}")
        return bestMove, minEval


def evaluatePosition(board, maximizingColor):
    if maximizingColor == "white":
        pieceScore = board.whiteScore - board.blackScore
    else:
        pieceScore = board.blackScore - board.whiteScore

    opponentColor = "black" if maximizingColor == "white" else "white"
    opponentMoves = getAllLegalMoves(
        opponentColor, board.pieceFormation, board.lastMove
    )

    positionScore = 0
    threatScore = 0
    mobilityScore = 0
    centerControlScore = 0
    kingSafetyScore = 0

    for row in range(8):
        for col in range(8):
            piece = board.pieceFormation[row][col]
            if piece != None:
                if piece.color == maximizingColor:
                    if isinstance(piece, Pawn):
                        positionScore += pawnPositionScore(row, piece.color)
                    elif isinstance(piece, Knight):
                        positionScore += knightPositionScore(row, col)
                    # mobilityScore += len(
                    #     getAllLegalMoves(
                    #         maximizingColor, board.pieceFormation, board.lastMove
                    #     )
                    # )
                    if (row, col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                        centerControlScore += 0.5
                    if isinstance(piece, King) and (col <= 2 or col >= 5):
                        kingSafetyScore += 1
                if (row, col) in opponentMoves:
                    threatScore += piece.weight * 0.5

    totalScore = (
        pieceScore
        + positionScore
        - threatScore
        + mobilityScore
        + centerControlScore
        + kingSafetyScore
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


def getAllLegalMovesFromPos(playerColor, pieceFormation, lastMove):
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
                                legalMoves.append((i, j, x, y))
                        else:
                            if pieceFormation[i][j].isLegalMove(
                                i, j, x, y, pieceFormation
                            ):
                                legalMoves.append((i, j, x, y))

    return legalMoves
