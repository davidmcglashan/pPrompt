dictionaries = dict()

# ===================================================================
# Returns any words matching the in string in the named dictionary.
# ===================================================================
def match( dic, ins ):
    matches = list()

    if dic in dictionaries:
        for c in dictionaries[dic]:
            if c.startswith( ins ):
                matches.append( c )

        matches.sort()

    return matches

# ===================================================================
# Returns any words matching the in string in the named dictionary.
# ===================================================================
def clear( dic ):
    if dic in dictionaries:
        dictionaries[dic].clear()
        return

# ====================================================================================
# Add the listed words to the named dictionary (which will be created if necessary).
# ====================================================================================
def putList( dic, list ):
    # Init the dictionary if it's non-existent.
    if dic not in dictionaries:
        dictionaries[dic] = []

    # Add the words.
    dictionaries[dic].extend( list )
