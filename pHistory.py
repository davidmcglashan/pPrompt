history = list()
index = 0

# ======================================
# return the previous item in history
# ======================================
def previous():
	if len(history) == 0:
		return None

	global index
	index = max( 0, index - 1 )

	return history[index]

# ======================================
# return the next item in history
# ======================================
def next():
	if len(history) == 0:
		return None

	global index
	index = min( index+1, len(history)-1 )

	return history[index]

# ======================================
# reset the history pointer
# ======================================
def reset():
	global index
	index = len( history )

# ======================================
# add a new item to history
# ======================================
def add( item ):
	history.append( item )
	reset()
