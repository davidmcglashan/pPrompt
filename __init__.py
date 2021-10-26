# The only functions we want to expose are use of the prompt ...
from .pInitWindows import prompt

# ... and adding things to the autocomplete dictionary ...
from .pComplete import putList
from .pComplete import putJsonFile
from .pComplete import putJson
