import json

dictionaries = dict()

# ===================================================================
#  Returns any words matching the in string in the named dictionary.
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
#  Returns any words matching the in string in the named dictionary.
# ===================================================================
def clear( dic ):
    if dic in dictionaries:
        dictionaries[dic].clear()
        return

# ====================================================================================
#  Add the listed words to the named dictionary (which will be created if necessary).
# ====================================================================================
def putList( dic, list ):
    # Init the dictionary if it's non-existent.
    if dic not in dictionaries:
        dictionaries[dic] = set()

    # Add the words.
    dictionaries[dic].update( list )

# ============================================================================================
#  Adds contents of file (JSON) to the named dictionary (which will be created if necessary)
# ============================================================================================
def putJsonFile( dic, file ):
    # Open the JSON file
    try:
        with open( file ) as json_file:
            json_data = json.load(json_file)
            putJson( dic, json_data )
    except( FileNotFoundError ):
        print( "File not found: %s" % file )
        return

# ============================================================================================
#  Adds contents of file (JSON) to the named dictionary (which will be created if necessary)
# ============================================================================================
def putJson( dic, json_data ):
    # Init the dictionary if it's non-existent.
    if dic not in dictionaries:
        dictionaries[dic] = set()

    walk( dic, json_data )

# ============================================================================================
#  
# ============================================================================================
def walk( dic, data ):
    # Lists are simply walked by their contents.
    if type( data ) == type( list() ):
        for d in data:
            walk( dic, d )

    # For dictionaries we put the keys in the dictionary and walk the values.
    elif type( data ) == type( dict() ):
        for k in data.keys():
            try:
                dictionaries[dic].add( k )
            except( KeyError ):
                pass
            walk( dic, data[k] )

    # Integers get put in the dictionary
    elif type( data ) == type( int() ):
        try:
            dictionaries[dic].add( str(data) )
        except( KeyError ):
            pass

    # Strings get broken up into words and each word put in the dictionary.
    elif type( data ) == type( str() ):
        words = data.split( ' ' )
        for word in words:
            try:
                dictionaries[dic].add( word )
            except( KeyError ):
                pass

    else:
        pass