index = -1
buffer = list()

key_Right = '\033[C'
key_Left = '\033[D'

# ======================================
#  Set a string as the current buffer
# ======================================
def set( str ):
	clear()
	for chr in str:
		append( chr )

# ======================================
#  Append a character to the buffer
# ======================================
def append( chr ):
	global index

	# detect arrow key presses that move the index within the buffer
	if chr == key_Left and index > -1:
		buffer.append( chr )
		index = index - 1
	elif chr == key_Right and index < len(string()):
		buffer.append( chr )
		index = index + 1
	else:
		buffer.insert( index+1, chr )
		index = index + 1

# ======================================
#  
# ======================================
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
			if chr not in { key_Left, key_Right }:
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