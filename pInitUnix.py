import os, sys, termios, tty

from . import pBuffer
from . import pCodes
from . import pComplete

# =============================================
#  Read a single character from the keyboard
# =============================================
def getch():
    # Terminal magic reading the character into 'ch'
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)

   	# Ctrl+C quits the program. We do this as soon as possible to be a good citizen.
    if ord(ch[0]) == pCodes.key_CtrlC:
        sys.exit(0)

    # Escape characters have 127 as their first character. This must be replaced
    # with \033 for some reason.
    if ord(ch[0]) == pCodes.key_Esc and len(ch)>2:
        rch = [ pCodes.seq_Esc, ord(ch[2]) ]
    else:
   	    rch = [ord(ch[0])]

    # More terminal magic and then return our character.
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return rch

# ======================================
#  Main loop
# ======================================
def prompt( callback=None ):
	sys.stdout.write( "\r> ")

	while True:
		# Get a single character and let the buffer process it.
		ch = getch()
		for chr in ch:
			command = pBuffer.handleKeyPress( [chr] )
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
