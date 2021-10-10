import sys, termios, tty

import pHistory
import pBuffer

key_Enter = 13
key_Esc = 27
key_Tab = 9
key_BkSpc = 127
key_CtrlC = 3

key_Up = '\033[A'
key_Down = '\033[B'

fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

# =============================================
#  Read a single character from the keyboard
# =============================================
def getch():
	# Terminal magic reading the character into 'ch'
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)

    # Some characters are 1 char long and therefore simple to deal with.
    if len(ch) == 1:
    	# Ctrl+C quits the program. We do this as soon as possible to be a good citizen.
        if ord(ch[0]) == key_CtrlC:
            sys.exit(0)

        # Characters less than 32 and greater than 126 aren't alphanumerics. We convert
        # these to their ordinal counterparts for ease of working later.
        if ord(ch) < 32 or ord(ch) > 126:
            ch = ord(ch)

    # Escape characters have 127 as their first character. This must be replaced
    # with \033 for some reason.
    elif ord(ch[0]) == key_Esc:
        ch = '\033' + ch[1:]

    # More terminal magic and then return our character.
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return ch

# ======================================
#  Main loop
# ======================================
sys.stdout.write( "\r> ")

while True:
	# Get a single character
	c = getch()

	# Up arrow replaces the buffer content with the previous historical line.
	if c == key_Up:
		pBuffer.set( pHistory.previous() )

	# Down arrow replaces the buffer content with the next historical line.
	elif c == key_Down:
		pBuffer.set( pHistory.next() )

	# Enter submits the current line for processing, adds it to history, and clears the
	# buffer ready for the next line.
	elif c == key_Enter:
		st = pBuffer.string()
		if st in { 'q', 'quit' }:
			print()
			sys.exit(0)

		sys.stdout.write( "\33[2K\r> " + st + "\n" )
		sys.stdout.write( "\rexecute this statement ... (%s)\n" % st )
		pHistory.add( st )
		pBuffer.clear()
	
	# Backspace must be passed onto the buffer.
	elif c == key_BkSpc:
		pBuffer.backspace()

	# Esc can be used to clear all of the current line.
	elif c == key_Esc:
		pBuffer.clear()
		
	# Otherwise, append the current character onto the end of the buffer.
	else:
		pBuffer.append(c)
	
	# Display a prompt and the current state of the buffer. Here we used the buffer's
	# output, not its string, so that ANSI or control characters get properly represented.
	sys.stdout.write( "\33[2K\r> " + pBuffer.output() )
