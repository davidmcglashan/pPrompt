import platform

# The only functions we want to expose are use of the prompt ...
if platform.system() == "Windows":
    from .pInitWindows import prompt
else:
    from .pInitUnix import prompt

# ... and adding things to the autocomplete dictionary ...
from .pComplete import putList
from .pComplete import putJsonFile
from .pComplete import putJson
