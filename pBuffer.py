import sys
import pHistory
import pCodes

index = -1
buffer = list()

# ========================================
#  Handles key presses from the terminal.
# =========================================
def handleKeyPress( c ):
	# Up arrow replaces the buffer content with the previous historical line.
	if c == pCodes.key_Up:
		set( pHistory.previous() )

	# Down arrow replaces the buffer content with the next historical line.
	elif c == pCodes.key_Down:
		set( pHistory.next() )

	# Enter submits the current line for processing, adds it to history, and clears the
	# buffer ready for the next line.
	elif c == pCodes.key_Enter:
		st = string()
		if st in { 'q', 'quit' }:
			print()
			sys.exit(0)

		sys.stdout.write( "\33[2K\r> " + st + "\n" )
		sys.stdout.write( "\rexecute this statement ... (%s)\n" % st )
		pHistory.add( st )
		clear()
	
	# Backspace must be passed onto the buffer.
	elif c == pCodes.key_BkSpc:
		backspace()

	# Esc can be used to clear all of the current line.
	elif c == pCodes.key_Esc:
		clear()
		
	# Otherwise, append the current character onto the end of the buffer.
	else:
		append(c)

# ======================================
#  Set a string as the current buffer
# ======================================
def set( str ):
	clear()
	if str != None:
		for chr in str:
			append( chr )

# ======================================
#  Append a character to the buffer
# ======================================
def append( chr ):
	global index

	# detect arrow key presses that move the index within the buffer
	if chr == pCodes.key_Left and index > -1:
		buffer.append( chr )
		index = index - 1
	elif chr == pCodes.key_Right and index < len(string()):
		buffer.append( chr )
		index = index + 1
	else:
		buffer.insert( index+1, chr )
		index = index + 1

# =====================================================
#  Output the buffer verbatim, including Ctrl codes. 
# =====================================================
def output():
	str = ""
	for chr in buffer:
		try:
			str = str + chr
		except( TypeError ):
			str = str + "?"
	return str

# ======================================
#  Return the buffer as a string.
# ======================================
def string():
	str = ""
	for chr in buffer:
		try:
			if chr not in { pCodes.key_Left, pCodes.key_Right }:
				str = str + chr
		except( TypeError ):
			str = str + "?"
	return str

# ======================================
#  Backspaces from the current index
# ======================================
def backspace():
	global index
	if index > -1:
		buffer.pop(index)
		index = index - 1

# ======================================
#  Clears the input buffer
# ======================================
def clear():
	global buffer
	global index
	buffer = list()
	index = -1