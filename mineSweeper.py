##
##  Minesweeper implemented in Python using SimpleGraphics
##
from SimpleGraphics import *
import random, time, inspect, sys, traceback, types, os
from pprint import pprint

# Vertical offset in the user interface
VOFFSET = 48

###############################################################################
##
##  Do not modify code above this point in the file
##
###############################################################################

# This creates the game board. Placing "C " in covered places, while randomly placing mines "C*"
# on the board
# Parameters: 
#      NUM_ROWS: Controls the amount of rows on the board
#      NUM_COLS: Controls the amount of columns on the board
#      MINES: Controls the amount of mines to be placed on the board 
# Returns: The game board 
def createBoard(NUM_ROWS, NUM_COLS, MINES):
  board = []
  for row in range(NUM_ROWS):
    board.append([])
    for col in range(NUM_COLS):
      board[row].append(" ")
  for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
      letter = "C "
      board[row][col] = letter
  Num_mines = 0
  while Num_mines < MINES:
    row_location  = random.randrange(NUM_ROWS)
    col_location = random.randrange(NUM_COLS)
    position = board[row_location][col_location]
    if position != "C*":
      position = position.replace(position,"C*")
      board[row_location][col_location] = position
      Num_mines = Num_mines + 1 

  return board 

# Given a location specified by a row&col, determine if it is within the board 
# parameters:
#     board: Take the games board
#     row: Takes a row on the board
#     col: Takes a col on the board
# Return: True if the location is within the board, otherwise False   
def isValid(board, row, col):
    result = True
    max_col = len(board[0])
    max_row = len(board)
    
    # 0 < row < max_row
    if row < 0 or row >= max_row :
        result = False
     
    # 0 < col < max_col    
    if col < 0 or col >= max_col :
        result = False 
    
    return result
  
# This searches a position on the board to see if it's visible, by checking if its valid,
# and then looking at its first index 
# Parameters: 
#      board: Takes the game board 
#      row: Takes a row on the game board 
#      col: Takes a col on the game board 
# Returns: True if the row and col is visible. False if the position is covered 
def isVisible(board,row,col):
  if isValid(board,row,col) and str((board[row][col])[0]) == "V":
    return True
  return False

# This searches a position on the board to see if it has a mine "C*" 
# Parameters: 
#      board: Takes the game board 
#      row: Takes a row on the game board 
#      col: Takes a col on the game board 
# Returns: True if the row and col has a mine. False if the position doesn't  
def isMine(board,row,col):
    if isValid(board,row,col) and board[row][col] == "C*":
        return True
    return False

# This determines whether or not the player has cleared all of the non-mine spaces from the board
# Parameters: 
#     board: Takes the game board 
# Returns: False  if there is any location/space that is still covered
def hasWon(board):
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            # if it has not been revealed
            if board[row][col][0] == "C" :
                return False
    return True          

# Determines how many mines that are adjacent to a specific location on the board.  
# parameters:
#      board: Takes the game board 
#      row: Take a row on the board 
#      col: Takes a col on the board
# Return: The number of mines adjacent to the specified location
def numMines(board,row,col):
    count = 0

    # CHECK TOP
    for y in range(-1,2):
        if isMine(board, row-1, col+y): #checks for mines in that location 
            count += 1 
    
    # CHECK BOTTOM
    for y in range(-1,2):
        if isMine(board, row+1, col+y):
            count += 1    

    # Check Left
    if isMine(board, row, col-1):  
        count += 1

    # Check Right
    if isMine(board, row, col+1):  
        count += 1

    return count
    
# This function looks at a square to check for a mine, it also checks the squares neighbours to see
# if they also have mines. if the square doesn't contain a mine, it is left blank.
# parameters:
#     board: Takes the game board
#     row: Takes a row in the board
#     col: Take a col in the board 
# Return: (None)   
def reveal(board, row, col):  
    if not isValid(board, row, col):
        # Do nothing for invalid location
        return
        
    if isVisible(board, row, col) :
        # Do nothing for already revealed location
        return  
    
    # Reveal the cell/location    
    board[row][col] = "V" + board[row][col][1]
    
    # if its neighbours has mines
    if numMines(board, row, col) >= 1 :
        board[row][col] = "V" + str(numMines(board,row,col))   
    else :   
        #Reveal TOP neighbour
        for y in range(-1,2):
            if not isVisible(board, row-1, col+y):
                reveal(board, row-1, col+y)
                
        # Reveal BOTTOM neigbours
        for y in range(-1,2):
            if not isVisible(board, row+1, col+y):
                reveal(board, row+1, col+y)
        
        # Reveal Left
        if not isVisible(board, row, col-1):
            reveal(board, row, col-1)
    
        # Reveal Right
        if not isVisible(board, row, col+1):
            reveal(board, row, col+1)

##############################################################################
##
##  Do not modify code below this point, except possibly for changing the
##  order that the tests are applied at the beginning of the main function
##  (this is *not* recommended).
##
##############################################################################

##############################################################################
##
##  Code for testing the functions written by the students
##
##############################################################################

# Determine whether or not a function exists in the namespace at the time
# this function is called
# Parameters:
#   name: The name of the function to check the existence of
# Returns: True if the function exists, False otherwise
def functionExists(name):
  members = inspect.getmembers(sys.modules[__name__])
  for (n, m) in members:
    if n == name and inspect.isfunction(m):
      return True
  return False

# Run a series of tests on the createBoard function
# Parameters: (None)
# Returns: True if all tests passed.  False if any test fails.
def testCreateBoard():
  print("Testing createBoard...")

  # Does the createBoard function exist?
  if functionExists("createBoard"):
    print("  The function seems to exist...")
  else:
    print("  The createBoard function doesn't seem to exist...")
    return False

  for (rows, cols, mines) in [(10, 10, 10), (20, 10, 10), (10, 20, 10), (10, 10, 20)]:
    # Try and call the function
    try:
      print("  Attempting to create a board: %d rows, %d columns and %d mines... " % (rows, cols, mines), end="")
      b = createBoard(rows, cols, mines)
    except Exception as e:
      print("\n  An exception occurred during the attempt.")
      traceback.print_exc(file=sys.stdout)
      return False
  
    # Does it have the correct return type?
    if type(b) is not list:
      print("\n  The value returned was a", str(type(b)) + ", not a list.")
      return False
  
    # Does the list have the corret number of elements?
    if len(b) != rows:
      print("\n  The board had", len(b), "rows when", rows, "were expected.")
      return False
  
    # Is each row a list?  Does each row have the current length?
    for i in range(len(b)):
      if type(b[i]) is not list:
        print("\n  The row at index", i, "is a", str(type(b[i])) + ", not a list.")
        return False
      if len(b[i]) != cols:
        print("\n  The row at index", i, "had", len(b[i]), "elements when", cols, "were expected.")
        return False
  
    # Is every element in the board a string, of two characters, and one of 
    # either "C " or "C*"?
    for r in range(0, len(b)):
      for c in range(0, len(b[r])):
        if type(b[r][c]) is not str:
          print("\n  The value in row", r, "column", c, "is a", str(type(b[r][c])) + ", not a string")
          return False
        if len(b[r][c]) != 2:
          print("\n  The string in row", r, "column", c, "is '%s', which does not have length 2" % b[r][c])
          return False
        if b[r][c] != "C " and b[r][c] != "C*":
          print("\n  The string in row", r, "column", c, "is '%s', which is not a valid representation of a space in the initial board.  All spaces in the initial board must be either 'C ' or 'C*'." % b[r][c])
          return False
  
    # Does the board have the correct number of mines?
    num_mines = 0
    for r in range(0, len(b)):
      for c in range(0, len(b[r])):
        if b[r][c][1] == "*":
          num_mines += 1
    if num_mines != mines:
      print("\n  The board contained", num_mines, "mines when", mines, "were expected.")
      return False
  
    print("Success.")

  print()
  return True

# Run a series of tests on the isMine function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testIsMine():
  print("Testing isMine...")

  # Does the isMine function exist?
  if functionExists("isMine"):
    print("  The function seems to exist...")
  else:
    print("  The isMine function doesn't seem to exist...")
    return False

  # Run a series of test cases
  for (b, r, c, a) in [([["C ", "C "], ["C*", "C "]], 0, 0, False),
                       ([["C ", "C "], ["C*", "C "]], 0, 1, False),
                       ([["C ", "C "], ["C*", "C "]], 1, 0, True),
                       ([["C ", "C "], ["C*", "C "]], 1, 1, False),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "]], 0, 2, True),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "]], 1, 2, False)] :
    # Attempt the function call
    try:
      print("  Attempting to use isMine on board %s at row %d column %d... " % (str(b), r, c), end="")
      result = isMine(b, r, c)
    except Exception as e:
      print("\n  An exception occurred during the attempt.")
      traceback.print_exc(file=sys.stdout)
      return False

    # Does it have the correct return type?
    if type(result) is not bool:
      print("\n  The value returned was a", str(type(result)) + ", not a Boolean.")
      return False

    # Did it return the correct value
    if result != a:
      print("\n  The value returned was", str(result), "when", str(a), "was expected.")
      return False

    print("Success.")

  print()
  return True

# Run a series of tests on the isVisible function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testIsVisible():
  print("Testing isVisible...")

  # Does the isVisible function exist?
  if functionExists("isVisible"):
    print("  The function seems to exist...")
  else:
    print("  The isVisible function doesn't seem to exist...")
    return False

  # Run a series of test cases
  for (b, r, c, a) in [([["V*", "C "], ["C*", "V "]], 0, 0, True),
                       ([["V*", "C "], ["C*", "V "]], 0, 1, False),
                       ([["V*", "C "], ["C*", "V "]], 1, 0, False),
                       ([["V*", "C "], ["C*", "V "]], 1, 1, True),
                       ([["C ", "C ", "V*"], ["C*", "C ", "C "]], 0, 2, True),
                       ([["C ", "C ", "V*"], ["C*", "C ", "C "]], 1, 2, False)] :
    # Attempt the function call
    try:
      print("  Attempting to use isVisible on board %s at row %d column %d... " % (str(b), r, c), end="")
      result = isVisible(b, r, c)
    except Exception as e:
      print("\n  An exception occurred during the attempt.")
      traceback.print_exc(file=sys.stdout)
      return False

    # Does it have the correct return type?
    if type(result) is not bool:
      print("\n  The value returned was a", str(type(result)) + ", not a Boolean.")
      return False

    # Did it return the correct value
    if result != a:
      print("\n  The value returned was", str(result), "when", str(a), "was expected.")
      return False

    print("Success.")

  print()
  return True

# Run a series of tests on the numMines function
# Parameters: (None)
# Returns: True if all tests passed.  False otherwise.
def testNumMines():
  print("Testing numMines...")

  # Does the numMines function exist?
  if functionExists("numMines"):
    print("  The function seems to exist...")
  else:
    print("  The numMines function doesn't seem to exist...")
    return False

  # Run a series of test cases
  for (b, r, c, a) in [
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 0, 0, 1),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 0, 1, 2),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 0, 2, 0),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 1, 0, 1),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 1, 1, 3),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 1, 2, 1),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 2, 0, 1),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 2, 1, 2),
                       ([["C ", "C ", "C*"], ["C*", "C ", "C "], ["C*", "C ", "C "]], 2, 2, 0),]:



#                       ([["C ", "C ", "C*"], ["C*", "C ", "C "]], 1, 2, False)] :
    # Attempt the function call
    try:
      print("  Attempting to use numMines on board %s at row %d column %d... " % (str(b), r, c), end="")
      result = numMines(b, r, c)
    except Exception as e:
      print("\n  An exception occurred during the attempt.")
      traceback.print_exc(file=sys.stdout)
      return False

    # Does it have the correct return type?
    if type(result) is not int:
      print("\n  The value returned was a", str(type(result)) + ", not an integer.")
      return False

    # Did it return the correct value
    if result != a:
      print("\n  The value returned was", str(result), "when", str(a), "was expected.")
      return False

    print("Success.")

  print()
  return True

###############################################################################
##
##  Main game code
##
###############################################################################

# Determine how many mines are currently marked on the board.  This value
# is displayed in the UI.
# Parameters:
#   board: The board to examine
# Returns: An integer number of mines that are currently marked
def minesMarked(board):
  count = 0
  for y in range(0, len(board)):
    for x in range(0, len(board[y])):
      if board[y][x][0] == "M":
        count = count + 1

  return count

# Draw the game board using SimpleGraphics
# Parmaeters:
#   board: The game board to draw
# Returns: (None)
def drawBoard(board, start_time, num_mines, hasWon = False):
  # Disable screen updates until we have everything drawn
  setAutoUpdate(False)

  # It turns out that switching fonts is slow.  As a result, we keep track
  # of what font we are currently using (cf), and only switch when necessary.
  setFont("Helvetica", 8, "bold")
  cf = ("Helvetica", 8, "bold")

  # Start with a clean slate
  clear()

  # Draw the board background
  setColor(128, 128, 128)
  rect(0, VOFFSET, len(board[0]) * 16 + 1, len(board) * 16 + 1)

  # For every square on the board
  for y in range(len(board)):
    for x in range(len(board[y])):
      # If the user hasn't yet won, draw a covered square
      if hasWon == False and \
         (board[y][x][0] == "C" or \
         board[y][x][0] == "M" or \
         board[y][x][0] == "?"):
        setColor(255, 255, 255)
        rect(x * 16, VOFFSET + y * 16, 16, 16)
        setColor(224, 224, 224)
        rect(x * 16 + 1, VOFFSET + y * 16 + 1, 15, 15)

        setColor(128, 128, 128)
        rect(x * 16 + 2, VOFFSET + y * 16 + 2, 14, 14)
        rect(x * 16 + 15, VOFFSET + y * 16 + 1, 1, 1)
        rect(x * 16 + 1, VOFFSET + y * 16 + 15, 1, 1)

        setColor(192, 192, 192)
        rect(x * 16 + 2, VOFFSET + y * 16 + 2, 12, 12)

        # If the covered square is marked as a mine, add a M on it
        # If the covered square is marked as unknown, add a ? on it
        if board[y][x][0] == "M" or board[y][x][0] == "?":
          setColor(0, 0, 0)
          if cf != ("Helvetica", 8, "bold"):
            setFont("Helvetica", 8, "bold")
            cf = ("Helvetica", 8, "bold")
          text(x * 16 + 9, VOFFSET + y * 16 + 8, board[y][x][0], "center")

      # If the square is visible, or we are drawing the board fully revealed
      # because the player has won the game
      if board[y][x][0] == "V" or hasWon:
        setOutline(128, 128, 128)
        setFill(192, 192, 192)
        rect(x * 16, VOFFSET + y * 16, 17, 17)

        # Draw a circle for a mine
        if board[y][x][-1] == "*":
          setColor(64, 64, 64)
          ellipse(x * 16 + 3, VOFFSET + y * 16 + 3, 11, 11)

        # Report the number of mines, using different colors for different 
        # numbers
        elif numMines(board, y, x) > 0:
          nm = numMines(board, y, x)
          if nm == 1:
            setColor(0, 0, 255)
          elif nm == 2:
            setColor(0, 128, 0)
          elif nm == 3:
            setColor(255, 0, 0)
          else:
            setColor(0, 0, 0)

          if cf != ("Helvetica", 8, "bold"):
            setFont("Helvetica", 10, "bold")
            cf = ("Helvetica", 10, "bold")
          text(x * 16 + 9, VOFFSET + y * 16 + 9, numMines(board, y, x), "center")
  # Update the status information at the top of the window
  setColor(0, 0, 0)
  setFont("Helvetica", 10, "bold")
  text(2, 16, "Marked: " + str(minesMarked(board)) + " of " + str(num_mines), "w")
  elapsed = time.time() - start_time
  text(2, 32, "Elapsed Time: %d:%02d" % (elapsed // 60, round(elapsed % 60)), "w")
  setAutoUpdate(True)

# Display the game board for debugging purposes
# Parameters:
#   board: The game board to display
# Returns: (None)
def displayBoard(board):
  print()
  for row in board:
    print(row)

# The main program
def main():
  #
  #  Perform tests on the first four functions that the students need to write
  #
  if testCreateBoard() == False:
    close()
    quit()
  if testIsMine() == False:
    close()
    quit()
  
  if testIsVisible() == False:
    close()
    quit()

  if testNumMines() == False:
    close()
    quit()

  # Verify that the image files are present
  if os.path.isfile("win.gif") == False or os.path.isfile("loose.gif") == False:
    print("This program requires access to win.gif and loose.gif.  Please")
    print("download them from the course website and save them in the")
    print("same directory as this program.")
    close()
    quit()

  width = 12
  height = 9
  mines = 10
  if len(sys.argv) > 2:
    print("Usage: python %s [easy | medium | hard]" % sys.argv[0])
    close()
    quit()

  if len(sys.argv) > 1:
    if sys.argv[1].lower() == "easy":
      pass;
    elif sys.argv[1].lower() == "medium":
      width = 20
      height = 10
      mines = 35
    elif sys.argv[1].lower() == "hard":
      width = 32
      height = 16
      mines = 99
    else:
      print("Unknown Option: '%s'" % sys.argv[1])
      close()
      quit()

  # Resize the window and draw the board
  board = createBoard(height, width, mines)
  resize(len(board[0]) * 16 + 1, VOFFSET + len(board) * 16 + 1)
  start_time = time.time()
  drawBoard(board, start_time, mines)

  # Display the board in the terminal
  # displayBoard(board)

  me = ""          # Mouse event message
  lost = False     # Has the user lost the game?
  old_elapsed = 0  # How much time has elapsed in the game?

  # While the game has not been closed
  while not closed():
    # Get the next mouse event
    mEvent = getMouseEvent()
    if mEvent != None:
      (me, (mx, my)) = mEvent
      x = mx // 16
      y = (my - VOFFSET) // 16
    else:
      me = ""
  
    # If the user pressed button 1
    if me == "<Button-1>":
      # If the press was on the board
      if y >= 0 and y < len(board) and x >= 0 and x < len(board[0]):
        # If the location is a mine
        if isMine(board, y, x):
          # Highlight the mine
          drawBoard(board, start_time, mines)
          setColor(255, 0, 0)
          rect(x * 16, VOFFSET + y * 16, 16, 16)
          setColor(64, 64, 64)
          ellipse(x * 16 + 3, VOFFSET + y * 16 + 3, 11, 11)
  
          # The game has been lost
          time.sleep(1)
          img = loadImage("loose.gif")
          drawImage(img, (getWidth() - getWidth(img)) / 2, (getHeight() - getHeight(img) - VOFFSET) / 2 + VOFFSET)
          lost = True
          break
        # If the location is covered
        elif isVisible(board, y, x) == False:
          # Reveal the square and its neighbours
          reveal(board, y, x)
          drawBoard(board, start_time, mines)
 
    if me == "<Button-2>" or me == "<Button-3>":
      # If the press was on the board
      if y >= 0 and y < len(board) and x >= 0 and x < len(board[0]):
        # If the square is already visible there is nothing to do
        if board[y][x][0] == "V":
          pass
        # If the square was covered then mark it as a mine
        elif board[y][x][0] == "C":
          board[y][x] = "M" + board[y][x][1:]
        # If the square was marked as a mine then mark it as unknown
        elif board[y][x][0] == "M":
          board[y][x] = "?" + board[y][x][1:]
        # If the square was marked as unknown then mark it as covered
        elif board[y][x][0] == "?":
          board[y][x] = "C" + board[y][x][1:]
        # Redraw the board so that the change is visible
        drawBoard(board, start_time, mines)
  
    # Keep track of the amount of time that has elapsed since the game began
    elapsed = time.time() - start_time

    # Only update the clock when it needs to be changed to avoid unnecessary
    # drawing
    if elapsed - old_elapsed >= 1:
      old_elapsed = elapsed
      setColor(208, 208, 208)
      setAutoUpdate(False)
      rect(0, 24, len(board[0]) * 16, 16)
      setColor(0, 0, 0)
      text(2, 32, "Elapsed Time: %d:%02d" % (elapsed // 60, round(elapsed % 60)), "w")
      setAutoUpdate(True)

    # If the user has won the game then exit the game loop
    if hasWon(board):
      drawBoard(board, start_time, mines, True)
      update()
      time.sleep(1)
      img = loadImage("win.gif")
      drawImage(img, (getWidth() - getWidth(img)) / 2, (getHeight() - getHeight(img) - VOFFSET) / 2 + VOFFSET)
      break
  
  # Keep the window open with the win or lost message until the player closes
  # the window
  while not closed():
    pass;

main()
