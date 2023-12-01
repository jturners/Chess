from board import Board
from cmu_graphics import *
from utilities import getOpeningPieceFormat, isKingInCheck
from graphics import displayCapturedPieces, drawMovesMade
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


def onAppStart(app):
    boardWidthScalar = 1.5
    boardHeightScalar = 4
    boardSize = 800
    app.testBoard = Board(
        app.width / boardWidthScalar, app.height / boardHeightScalar, boardSize
    )


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


def redrawAll(app):
    app.testBoard.draw()
    app.testBoard.drawPieces()

    # reset game label
    resetGameLabelWidthScalar = 2
    resetGameLabelHeightScalar = 0.95
    drawLabel(
        "Press 'r' to reset game",
        app.width / resetGameLabelWidthScalar,
        app.height * resetGameLabelHeightScalar,
        bold=True,
    )

    # checkmate label
    if app.testBoard.inCheckmate:
        checkmateLabelWidthScalar = 2
        checkmateLabelHeightScalar = 12
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
            # check for promotion
            if isinstance(piece, Pawn):
                if piece.color == "white" and newRow == 0:
                    app.testBoard.pieceFormation[newRow][newCol] = Queen("white")
                elif piece.color == "black" and newRow == 7:
                    app.testBoard.pieceFormation[newRow][newCol] = Queen("black")

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
                app.testBoard.moves[
                    f"{app.testBoard.moveCount+1}. {piece.color} Move"
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
