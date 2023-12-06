#   ATLA Solitaire - Term project for 15-112

#   ATLA Solitaire is a game of Klondike solitaire themed after Avatar: The Last Airbender.

    Klondike Solitaire Rules:

    Klondike uses a 52-card deck. The goal is to arrange them by suit, starting with the Ace and ending with the King, on empty areas called the foundations.

    The cards are dealt into 7 piles on the tableau (the game area). All the cards are facing down, except for the upper one in each pile. To access and reveal 
    the bottom cards, the players have to build sequences and move them within the piles. Sequences on the tableau are built in descending order (from King to Ace) 
    and with alternating colors. Only Kings can be moved into empty spaces on the tableau. 

    The remaining cards that were not dealt into the piles are arranged in a stock pile. These can be called into play to help players build their sequences. 

    (Description taken from: [Solitaire 365](https://www.solitaire365.com/tips/types-of-solitaire-games))

#   To play, install the cmu_graphics library (https://academy.cs.cmu.edu/desktop) then run the main.py file (ctrl+b / cmd+b) 

#   Shorthand commands: N/A

#   Possible moves:

    Move the card from the stack to the foundation
    Move the card from the stack to the tableau
    Move the card from the foundation to the tableau
    Move the card between columns within the tableau
    Move a group of cards between columns within the tableau
    Get hint
    Undo move

#   Note: when moving cards within the tableau, make sure the mouse is placed on the upper half of the card