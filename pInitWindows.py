import os,sys

from . import pBuffer
from . import pCodes
from . import pComplete

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

# ======================================
#  Main loop
# ======================================
def prompt( callback=None ):
	sys.stdout.write( "\r> ")
	getch = _Getch()

	while True:
		# Get a single character and let the buffer process it.
		ch = getch()
		command = pBuffer.handleKeyPress( ch )
		if command != None and callback != None:
			callback( command )

		# read the size of the terminal, and work out how many lines the output *might* be. Then move
		# the cursor up that number before we let it be drawn. This is naive as all hell but stops
		# wrapping text going crazy in the terminal. Other issues still exist.
#		columns, rows = 30,12#os.get_terminal_size(0)
#		bufstr = pBuffer.string()
#		lines = len(bufstr)/columns
#		sys.stdout.write( "\33[A"*int(lines) )
		
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
os.system('')


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
