from cmu_graphics import *


def displayCapturedPieces(app):
    capturedPiecesRectYCoordScalar = 0.1
    capturedPiecesRectWidthScalar = 7
    capturedPiecesRectHeightScalar = 0.85
    drawRect(
        0,
        app.height * capturedPiecesRectYCoordScalar,
        app.width / capturedPiecesRectWidthScalar,
        app.height * capturedPiecesRectHeightScalar,
        fill="gray",
    )

    capturedPiecesLabelWidthScalar = 15
    whiteCapturedPiecesLabelHeightScalar = 0.12
    drawLabel(
        "White's Captured Pieces:",
        app.width / capturedPiecesLabelWidthScalar,
        app.height * whiteCapturedPiecesLabelHeightScalar,
        fill="white",
        bold=True,
    )

    blackCapturedPiecesLabelHeightScalar = 0.53
    drawLabel(
        "Black's Captured Pieces:",
        app.width / capturedPiecesLabelWidthScalar,
        app.height * blackCapturedPiecesLabelHeightScalar,
        fill="black",
        bold=True,
    )

    whiteCapturedPiecesLabelHeightCounter = 0.15
    for piece in app.testBoard.whiteCaptured:
        drawLabel(
            piece,
            app.width / capturedPiecesLabelWidthScalar,
            app.height * whiteCapturedPiecesLabelHeightCounter,
            fill="white",
        )
        whiteCapturedPiecesLabelHeightCounter += 0.02

    blackCapturedPiecesLabelHeightCounter = 0.55
    for piece in app.testBoard.blackCaptured:
        drawLabel(
            piece,
            app.width / capturedPiecesLabelWidthScalar,
            app.height * blackCapturedPiecesLabelHeightCounter,
            fill="black",
        )
        blackCapturedPiecesLabelHeightCounter += 0.02


def drawMovesMade(app):
    movesMadeRectXCoordScalar = 0.75
    movesMadeRectYCoordScalar = 0.1
    movesMadeRectWidthScalar = 5
    movesMadeRectHeightScalar = 0.85

    drawRect(
        app.width * movesMadeRectXCoordScalar,
        app.height * movesMadeRectYCoordScalar,
        app.width / movesMadeRectWidthScalar,
        app.height * movesMadeRectHeightScalar,
        fill="gray",
    )

    movesMadeLabelWidthScalar = 0.85
    movesMadeLabelHeightScalar = 0.12

    drawLabel(
        "Moves Made:",
        app.width * movesMadeLabelWidthScalar,
        app.height * movesMadeLabelHeightScalar,
        fill="white",
        bold=True,
    )

    movesMadeLabelHeightCounter = 0.15
    maxMovesDisplayed = 27
    moveDisplayed = 0

    for move in app.testBoard.moves:
        if moveDisplayed >= maxMovesDisplayed:
            drawRect(
                app.width * movesMadeRectXCoordScalar,
                app.height * movesMadeRectYCoordScalar,
                app.width / movesMadeRectWidthScalar,
                app.height * movesMadeRectHeightScalar,
                fill="gray",
            )
            drawLabel(
                "Moves Made:",
                app.width * movesMadeLabelWidthScalar,
                app.height * movesMadeLabelHeightScalar,
                fill="white",
                bold=True,
            )
            movesMadeLabelHeightCounter = 0.15
            moveDisplayed = 0

        drawLabel(
            move,
            app.width * movesMadeLabelWidthScalar,
            app.height * movesMadeLabelHeightCounter,
            fill="white",
        )
        movesMadeLabelHeightCounter += 0.01
        drawLabel(
            app.testBoard.moves[move],
            app.width * movesMadeLabelWidthScalar,
            app.height * movesMadeLabelHeightCounter,
            fill="white",
        )
        movesMadeLabelHeightCounter += 0.02
        moveDisplayed += 1
