import sys
from . import pHistory
from . import pCodes
from . import pComplete

index = -1
buffer = list()
escToggle = 0

# ========================================
#  Handles key presses from the terminal.
# =========================================
def handleKeyPress( c ):
	global escToggle
	ch = c[0]

	# If this char is an esc sequence it means the _next_ key press is meaningful. This one can be
	# ignored and shouldn't be added to the buffer.
	if ch == pCodes.seq_Esc:
		escToggle = 1 - escToggle
		return

	# Ctrl+C quits quickly and immediately.
	elif ch == pCodes.key_CtrlC:
		sys.exit(0)

	# Up arrow replaces the buffer content with the previous historical line.
	elif escToggle == 1 and ch == pCodes.key_Up:
		set( pHistory.previous() )

	# Down arrow replaces the buffer content with the next historical line.
	elif escToggle == 1 and ch == pCodes.key_Down:
		set( pHistory.next() )

	# Enter submits the current line for processing, adds it to history, and clears the
	# buffer ready for the next line.
	elif ch == pCodes.key_Enter:
		st = string()
		if st in { 'q', 'quit' }:
			print()
			sys.exit(0)

		sys.stdout.write( "\33[2K\r> " + st + "\n" )
		pHistory.add( st )
		clear()
		return st
	
	# Backspace must be passed onto the buffer.
	elif ch == pCodes.key_BkSpc:
		backspace()

	# Esc can be used to clear all of the current line.
	elif ch == pCodes.key_Esc:
		clear()
		
	# Tab issues an autocomplete.
	elif ch == pCodes.key_Tab:
		tab()

	# Otherwise, append the current character onto the end of the buffer.
	else:
		append( chr(ch) )

	escToggle = 0

# ======================================
#  Set a string as the current buffer
# ======================================
def set( str ):
	clear()
	if str != None:
		for chr in str:
			append( chr )

# =====================================================================
#  Remove the characters between i and index from the current buffer.
# =====================================================================
def removeTo( i ):
	global index

	while index != i:
		if i < index:
			buffer.pop( i )
		else:
			buffer.pop( index )
		index = index - 1
	buffer.pop( index )
	index = index - 1

# ===========================================
#  Insert a string into the current buffer.
# ===========================================
def insert( str ):
	global index

	for chr in str:
		buffer.insert( index+1, chr )
		index = index + 1

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

# ========================================================
#  Handles a tab key press based on the current buffer.
# ========================================================
def tab():
	# track back from index to find a good starting point
	start = index
	while start > 0:
		if buffer[start-1] == ' ':
			break
		start = start - 1

	# buffer is a char array so we need to join our range to make a string we can search with.
	try:
		word = "".join(buffer[start:index+1])
	except( TypeError ):
		return

	# Search the commands dictionary if we're at the beginning of the buffer.
	if start == 0:
		matches = pComplete.match( 'commands', word )

	# Otherwise, use the commands dictionary everywhere else. (for now)
	else:
		matches = pComplete.match( 'payload', word )

	# No matches does nothing.
	if len( matches ) == 0:
		return

	# A single match gets to become the buffer content.
	elif len( matches ) == 1:
		removeTo( start )
		insert( matches[0] )

		# If we're at the end of the buffer also append a space to be nice.
		if index == len(buffer)-1:
			insert( ' ' )

	# Lots of matches get displayed in the terminal.
	else:
		# Find the longest 'stem' that matches all the matches
		l = len( word )
		count = len( matches )
		stem = ''

		while count == len( matches ):
			insertstem = stem
			count = 0
			l = l + 1
			stem = matches[0][0:l].lower()

			# Does everyone else match the stem?
			for m in matches:
				if len(m) < l:
					break
				elif m.lower().startswith( stem ):
					count = count + 1

		if len(insertstem) > len(word):
			removeTo( start )
			insert( insertstem )

		print()
		print( "\t".join(matches) )
