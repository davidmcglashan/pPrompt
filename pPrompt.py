import os, sys, termios, tty

import pBuffer
import pCodes
import pComplete

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
        if ord(ch[0]) == pCodes.key_CtrlC:
            sys.exit(0)

        # Characters less than 32 and greater than 126 aren't alphanumerics. We convert
        # these to their ordinal counterparts for ease of working later.
        if ord(ch) < 32 or ord(ch) > 126:
            ch = ord(ch)

    # Escape characters have 127 as their first character. This must be replaced
    # with \033 for some reason.
    elif ord(ch[0]) == pCodes.key_Esc:
        ch = '\033' + ch[1:]

    # More terminal magic and then return our character.
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return ch

# ======================================
#  Main loop
# ======================================
def prompt( callback=None ):
	sys.stdout.write( "\r> ")

	while True:
		# Get a single character and let the buffer process it.
		ch = getch()
		command = pBuffer.handleKeyPress( ch )
		if command != None and callback != None:
			callback( command )

		# read the size of the terminal, and work out how many lines the output *might* be. Then move
		# the cursor up that number before we let it be drawn. This is naive as all hell but stops
		# wrapping text going crazy in the terminal. Other issues still exist.
		columns, rows = os.get_terminal_size(0)
		bufstr = pBuffer.string()
		lines = len(bufstr)/columns
		sys.stdout.write( "\33[A"*int(lines) )
		
		# Display a prompt and the current state of the buffer. Here we used the buffer's
		# output, not its string, so that ANSI or control characters get properly represented.
		sys.stdout.write( "\33[2K\r> " + pBuffer.output() )

# ===========================================================
#  Default callback (attached only when running standalone)
# ===========================================================
def callback( str=None ):
	print( "\rexecute this statement ... (%s)\n" % str )

# ======================================
#  Stuff to do when the module is imported
# ======================================
fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

# Populate the dictionaries when running standalone
if (__name__ == '__main__'):
	# Put 100 random words in the commands dictionary.
	pComplete.putList( 'commands', { 'adorable','arch','attraction',
	'bad','bent','bounce','calculating','calm','capable','changeable','chess','chunky','competition',
	'curious','dare','decorous','describe','diligent','earsplitting','easy','egg','expert','explain',
	'exultant','fasten','fluffy','front','fry','goofy','gratis','habitual','helpless','hill','idiotic',
	'impossible','impress','irritate','jewel','judge','kaput','kick''known','lock','loss','machine',
	'meddle','medical','metal','note','ordinary','part','pause','peep','perform','poised','poison','prose',
	'question','quiet','quilt','range','road','room','rural','seal','seat','sheep','skillful','small',
	'smiling','spray','step','stitch','story','stream','substantial','super','tail','tasteless','teeth',
	'territory','thoughtful','threatening','unable','unfasten','unite','unnatural','unwieldy','vest',
	'view','volcano','waiting','want','well-off','whimsical','wide','witty','woman','wonder','worthless'
	} )

	# Put a JSON file into the payload dictionary.
	pComplete.putJsonFile( 'payload', 'example.json' )
	prompt( callback )
