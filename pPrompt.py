import sys, termios, tty

import pHistory
import pBuffer

key_Enter = 13
key_Esc = 27
key_Tab = 9
key_BkSpc = 127

key_Up = '\033[A'
key_Down = '\033[B'

fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

def getch():
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)

    if len(ch) == 1:
        if ord(ch) < 32 or ord(ch) > 126:
            ch = ord(ch)
    elif ord(ch[0]) == 27:
        ch = '\033' + ch[1:]

    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return ch

sys.stdout.write( "\r> ")

while True:
	# Gets a single character
	c = getch()

	if c == key_Up:
		st = pHistory.previous()
		pBuffer.set( st )

	elif c == key_Down:
		st = pHistory.next()
		pBuffer.set( st )

#	elif c == key_Left:
#		a = 1
#	elif c == key_Right:
#		a = 1

	elif c == key_Enter:
		st = pBuffer.string()
		if st in { 'q', 'quit' }:
			print()
			sys.exit(0)

		sys.stdout.write( "\33[2K\r> " + st + "\n" )
		sys.stdout.write( "\rexecute this statement ... (%s)\n" % st )
		pHistory.add( st )
		pBuffer.clear()
	
	elif c == key_BkSpc:
		pBuffer.backspace()

	elif c == key_Esc:
		pBuffer.clear()
		
	else:
		pBuffer.append(c)
	
	sys.stdout.write( "\33[2K\r> " + pBuffer.output() )
