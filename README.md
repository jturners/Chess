Made for 15-112 at Carnegie Mellon University by John L. Turner-Smith
_____________________________________________________________________

This is a fully functioning chess game including all features such as castling, en passant, and pawn promotion.
Additional AI feature utilizing a basic heuristic minimax artificial intelligence model with alpha-beta pruning.

NOTES BEFORE PLAYING:

-To start game, run from game.py

-3 gameplay modes: play against self, play against friend, play against AI.

-To play against self or against friend, simply start moving pieces (starting with White).

-To play against AI press 'w' if you want to play as white and then move white or press 'b' if you want to play as black and the AI will begin it's first move.
    *Note: AI model takes long to move due to time complexity of analyzing positions.*

-Press 'h' to display hint - this also takes long due to time complexity.

-To reset the game back to the original state press 'r'.

-When in checkmate, 'checkmate' will display at the top left hand side of the board, the game is then over and you have to reset.

-To move a piece simply select it and then select the square you wish to move to
    *Note: If piece does not move, this means the move you tried was not a legal one*

-If you wish to unselect a piece, press it again

