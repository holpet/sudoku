# SUDOKU SOLVER
Sudoku is a game, in which a player is asked to fill in numbers on a 9x9 board by adhering to specific rules - number can't be repeated both horizontally and vertically and in a 3x3 board square. Since such a game can be hard to solve by humans 
(especially with decreasing number of clues - the least being 17 for a human to successfully solve the puzzle), an artificial solver can help.<br />

Project was written in python using the pygame library.<br/>

• The user will be able to generate a random sudoku game or insert their own one by hand (which will be automatically validated and ready to play once the implemented algorithm confirms the game is solvable).<br />
• The player moves on the board by mouse clicking and using keyboard.<br />
• Failed attemps to insert numbers are being counted and a timer keeps track of how long it took for the player to solve the game.<br />
• Hints can be displayed to help the player come up with a proper solution.<br />
• If player can't solve the game themselves, they have the option to click on <b>SOLVE GAME</b> that does it automatically. The solution then is either displayed immediately or with the visualization of the sudoku solving algorithm if "vizualisation" is checked.<br />

![Demo #1](/img/demo1.gif/)

![Demo #2](/img/demo2.gif/)
 
