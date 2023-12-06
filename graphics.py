from cmu_graphics import *


def displayCapturedPieces(app):
    capturedPiecesRectYCoordScalar = 0.1
    capturedPiecesRectWidthScalar = 7
    capturedPiecesRectHeightScalar = 0.85
    cerulian = rgb(67, 127, 151)
    drawRect(
        0,
        app.height * capturedPiecesRectYCoordScalar,
        app.width / capturedPiecesRectWidthScalar,
        app.height * capturedPiecesRectHeightScalar,
        fill=cerulian,
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

    whiteCapturedPiecesLabelHeightCounter = 0.14
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


def displaySquareNames(app):
    numWidthScalar = 6.3
    numHeightCounter = 0.16
    for num in range(8, 0, -1):
        drawLabel(
            num, app.width / numWidthScalar, app.height * numHeightCounter, bold=True
        )
        numHeightCounter += 0.1

    letterWidthCounter = 0.21
    letterHeightScalar = 0.94
    for letter in range(65, 73):
        drawLabel(
            chr(letter),
            app.width * letterWidthCounter,
            app.height * letterHeightScalar,
            bold=True,
        )
        letterWidthCounter += 0.065


def displayMovesMade(app):
    movesMadeRectXCoordScalar = 0.75
    movesMadeRectYCoordScalar = 0.1
    movesMadeRectWidthScalar = 5
    movesMadeRectHeightScalar = 0.85
    cerulian = rgb(67, 127, 151)

    drawRect(
        app.width * movesMadeRectXCoordScalar,
        app.height * movesMadeRectYCoordScalar,
        app.width / movesMadeRectWidthScalar,
        app.height * movesMadeRectHeightScalar,
        fill=cerulian,
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
    maxMovesDisplayed = 40
    moveDisplayed = 0

    for move in app.testBoard.moves:
        if moveDisplayed >= maxMovesDisplayed:
            drawRect(
                app.width * movesMadeRectXCoordScalar,
                app.height * movesMadeRectYCoordScalar,
                app.width / movesMadeRectWidthScalar,
                app.height * movesMadeRectHeightScalar,
                fill=cerulian,
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
            f"{move} {app.testBoard.moves[move]}",
            app.width * movesMadeLabelWidthScalar,
            app.height * movesMadeLabelHeightCounter,
            fill="white",
        )
        movesMadeLabelHeightCounter += 0.02
        moveDisplayed += 1


def displayLabels(app):
    # reset game label
    resetGameLabelWidthScalar = 4
    resetGameLabelHeightScalar = 0.97
    drawLabel(
        "Press 'r' to reset game",
        app.width / resetGameLabelWidthScalar,
        app.height * resetGameLabelHeightScalar,
        bold=True,
    )

    # play AI? label
    playAiLabelWidthScalar = 1.6
    playAiAsWhiteLabelHeightScalar = 0.96
    drawLabel(
        "Press 'w' to play white against computer",
        app.width / playAiLabelWidthScalar,
        app.height * playAiAsWhiteLabelHeightScalar,
        bold=True,
    )
    playAiAsBlackLabelHeightScalar = 0.98
    drawLabel(
        "Press 'b' to play black against computer",
        app.width / playAiLabelWidthScalar,
        app.height * playAiAsBlackLabelHeightScalar,
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

    # hint? label
    wantHintLabelWidthScalar = 2.4
    wantHintLabelHeightScalar = 0.96
    drawLabel(
        "Press 'h' for hint",
        app.width / wantHintLabelWidthScalar,
        app.height * wantHintLabelHeightScalar,
        bold=True,
    )
    onlyOnTurnHeightScalar = wantHintLabelHeightScalar + 0.02
    drawLabel(
        "(only on your turn)",
        app.width / wantHintLabelWidthScalar,
        app.height * onlyOnTurnHeightScalar,
    )

    # display hint label
    displayHintWidthScalar = 2.3
    displayHintHeightScalar = 18
    if app.wantsHint and app.aiHint != None:
        drawLabel(
            app.aiHint,
            app.width / displayHintWidthScalar,
            app.height / displayHintHeightScalar,
        )
