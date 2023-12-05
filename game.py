from board import Board, copyBoard
from cmu_graphics import *
from utilities import (
    getOpeningPieceFormat,
    isKingInCheck,
    getAllLegalMoves,
    resultsInCheck,
)
from graphics import displayCapturedPieces, drawMovesMade
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from engine import aiMove


def onAppStart(app):
    boardWidthScalar = 1.5
    boardHeightScalar = 4
    boardSize = 800
    app.testBoard = Board(
        app.width / boardWidthScalar, app.height / boardHeightScalar, boardSize
    )
    app.playComputer = False
    app.computerCalculating = False


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
    # reset game
    if key == "r":
        app.testBoard.pieceFormation = getOpeningPieceFormat()
        app.testBoard.turn = "white"
        app.testBoard.inCheckmate = False
        app.testBoard.blackCaptured = []
        app.testBoard.whiteCaptured = []
        app.testBoard.moves = {}
        app.testBoard.moveCount = 0
        app.playComputer = False
    elif key == "c":
        app.playComputer = True


def onStep(app):
    if (
        app.playComputer
        and app.testBoard.turn == "black"
        and not app.computerCalculating
    ):
        app.computerCalculating = True
    elif app.playComputer and app.testBoard.turn == "black" and app.computerCalculating:
        aiMovePos = aiMove(copyBoard(app.testBoard), "black")
        fromRow, fromCol, toRow, toCol = aiMovePos
        app.testBoard.selected = True
        app.testBoard.cellSelectedCol = app.testBoard.cellFormation[fromRow][
            fromCol
        ].color
        app.testBoard.cellSelectedCoords = (fromRow, fromCol)
        move(app, toRow, toCol)
        app.computerCalculating = False


def redrawAll(app):
    app.testBoard.draw()
    app.testBoard.drawPieces()

    # reset game label
    resetGameLabelWidthScalar = 4
    resetGameLabelHeightScalar = 0.95
    drawLabel(
        "Press 'r' to reset game",
        app.width / resetGameLabelWidthScalar,
        app.height * resetGameLabelHeightScalar,
        bold=True,
    )

    # play AI? label
    playAiLabelWidthScalar = 1.6
    playAiLabelHeightScalar = 0.95
    drawLabel(
        "Press 'c' to play against computer",
        app.width / playAiLabelWidthScalar,
        app.height * playAiLabelHeightScalar,
        bold=True,
    )

    # playing Ai label
    if app.playComputer:
        playingAiLabelWidthScalar = 1.6
        playingAiLabelHeightScalar = 13
        drawLabel(
            "Playing against computer",
            app.width / playingAiLabelWidthScalar,
            app.height / playingAiLabelHeightScalar,
            bold=True,
        )

    # computer Calculating label
    if app.computerCalculating:
        computerCalculatingLabelWidthScalar = 2.2
        computerCalculatingLabelHeightScalar = 13
        drawLabel(
            "Computer Calculating Move...",
            app.width / computerCalculatingLabelWidthScalar,
            app.height / computerCalculatingLabelHeightScalar,
        )

    # checkmate label
    if app.testBoard.inCheckmate:
        checkmateLabelWidthScalar = 4
        checkmateLabelHeightScalar = 13
        drawLabel(
            "Checkmate",
            app.width / checkmateLabelWidthScalar,
            app.height / checkmateLabelHeightScalar,
            bold=True,
        )

    displayCapturedPieces(app)
    drawMovesMade(app)


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
            capturedPiece = app.testBoard.pieceFormation[newRow][newCol]
            app.testBoard.pieceFormation[newRow][newCol] = piece
            app.testBoard.pieceFormation[currRow][currCol] = None

            # checkmate

            opponentColor = "black" if piece.color == "white" else "white"
            opponentInCheck = isKingInCheck(
                opponentColor, app.testBoard.pieceFormation, app.testBoard.lastMove
            )
            if opponentInCheck:
                possibleMoves = getAllLegalMoves(
                    opponentColor,
                    app.testBoard.pieceFormation,
                    app.testBoard.lastMove,
                )

                app.testBoard.inCheckmate = True
                for move in possibleMoves:
                    testRow, testCol = move

                    inCheck = resultsInCheck(
                        opponentColor,
                        app.testBoard.pieceFormation,
                        currRow,
                        currCol,
                        testRow,
                        testCol,
                    )

                    if not inCheck:
                        app.testBoard.inCheckmate = False
                        break

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
            # check for promotion
            if isinstance(piece, Pawn):
                if piece.color == "white" and newRow == 0:
                    app.testBoard.pieceFormation[newRow][newCol] = Queen("white")
                elif piece.color == "black" and newRow == 7:
                    app.testBoard.pieceFormation[newRow][newCol] = Queen("black")

            if not isKingInCheck(
                app.testBoard.turn,
                app.testBoard.pieceFormation,
                app.testBoard.lastMove,
            ):
                if app.testBoard.turn == "white" and capturedPiece != None:
                    app.testBoard.blackScore -= capturedPiece.weight
                elif app.testBoard.turn == "black" and capturedPiece != None:
                    app.testBoard.whiteScore -= capturedPiece.weight

                # king-side castle
                if isinstance(piece, King) and currCol == 4 and newCol == 6:
                    app.testBoard.pieceFormation[currRow][
                        currCol + 1
                    ] = app.testBoard.pieceFormation[currRow][currCol + 3]
                    app.testBoard.pieceFormation[currRow][currCol + 3] = None
                    app.testBoard.pieceFormation[currRow][currCol + 2] = piece
                    app.testBoard.pieceFormation[currRow][currCol] = None

                # queen-side castle
                elif isinstance(piece, King) and currCol == 4 and newCol == 2:
                    app.testBoard.pieceFormation[currRow][
                        currCol - 1
                    ] = app.testBoard.pieceFormation[currRow][currCol - 4]
                    app.testBoard.pieceFormation[currRow][currCol - 4] = None
                    app.testBoard.pieceFormation[currRow][currCol - 2] = piece

                app.testBoard.turn = (
                    "black" if app.testBoard.turn == "white" else "white"
                )
                if isinstance(piece, Pawn) and not piece.pastFirstMove:
                    piece.pastFirstMove = True
                elif isinstance(piece, Rook) and not piece.pastFirstMove:
                    piece.pastFirstMove = True
                elif isinstance(piece, King) and not piece.pastFirstMove:
                    piece.pastFirstMove = True

                app.testBoard.lastMove = {
                    "piece": piece,
                    "from": (currRow, currCol),
                    "to": (newRow, newCol),
                }
                app.testBoard.moves[
                    f"{app.testBoard.moveCount+1}. {piece.color}"
                ] = f"{piece.name} moved from {app.testBoard.squareNames[currRow][currCol]} to {app.testBoard.squareNames[newRow][newCol]}"

                app.testBoard.moveCount += 1
            else:
                app.testBoard.pieceFormation[currRow][currCol] = piece
                app.testBoard.pieceFormation[newRow][newCol] = None

                if piece.color == "white" and app.testBoard.blackCaptured != []:
                    app.testBoard.blackCaptured.pop()
                elif piece.color == "black" and app.testBoard.whiteCaptured != []:
                    app.testBoard.whiteCaptured.pop()


def main():
    runApp()


main()
