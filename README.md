[![Build Status](https://travis-ci.com/zwoefler/Tetris-Python-Game.svg?branch=master)](https://travis-ci.com/zwoefler/Tetris-Python-Game)

# Tetris
This is a python version of the famous tetris game amde for my father as a birthday gift. We used to play WinTETRIS battles when I was waaaay younger. So now I want to gift him this little game that he can enjoy on every computer he uses.

# Features to implement
- [ ] Implement the scoringsystem of the original Tetris (MS Entertainment Pack for Windows)
- [X] Preview the next piece
- [X] Clear Rows once they are complete
- [ ] Hold the right-, left-, or uparrow to move the piece
- Adapt colors from original `WinTETRIS`:
    - [X] L-Shape, yellow
    - [x] J-Shape, pink
    - [x] I-Shape, red
    - [x] S-Shape, darkblue
    - [x] Z-Shape, green
    - [x] O-Shape, lightblue
    - [x] T-Shape, gray

# To Do's
- [X] Remove visible grid
- [ ] Gray Border like in [this](https://classicreload.com/sites/default/files/tetris-for-windows.png) image.
- [ ] Gray Inforbox to the left of the palying grid
- [ ] Show levels, next piece and score in the gray Box to the left of the Playinggrid
- [ ] Background should match the levelimages from original "WinTETRIS"
    - [ ] Level 1
    - [ ] Level 2
    - [ ] Level 3
    - [ ] Level 4
    - [ ] Level 5
    - [ ] Level 6
    - [ ] Level 7
    - [ ] Level 8
    - [ ] Level 9
    - [ ] Level 10
- [X] Find out how many points you get per dropoff of a piece and cleared rows per level


# Scoring System
According to the [tetris.wiki](https://tetris.wiki/Tetris_(Microsoft_Entertainment_Pack_for_Windows)) the Tetris in the Microsoft Entertainment Pack has the following scoring system:

- Each piece has an initial score value and decreases with each rotation and horizontal move
- A piece has an initial score value, which decreases on:
    - Rotation or
    - horizontal moves
- Dropping the piece increases the score value of the piece

Bonuses for clearing rows:
|Row|Points|
|---|------|
| 1 | 100  |
| 2 | 200  |
| 3 | 400  |
| 4 | 800  |



# Known Issues
- [X] Rows are not cleared
- [X] The window can't be closed with the X-Button in the top right corner

# Lessons Learned
- Getting to experiment with [PyGame](https://www.pygame.org/news)
- **Clean Code** Using [PyLint](https://www.pylint.org/) for Style Guide Checks in [TravisCI](https://travis-ci.com/)
    - Getting knowledge of PIP8 Style Guide (Unnecessary parens, naming conventions, )
    - Avoid using global variables



Inspired by the original "WinTETRIS" for Windows98 and the code of [Tetris-Game](https://github.com/techwithtim/Tetris-Game) from [TechwithTim](https://github.com/techwithtim).


