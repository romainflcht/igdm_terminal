import securestore
from rich.console import Console
from format_data import format_thread_selection
CONSOLE = Console()
csrf_base = "3VT33LVCH4FH5RSR3QOJU0AVDFUGOPCN8"
sid_base = "lEXy+TxHbRhp6UU5Ei1rh3pdxtATurb3jTg0RpTE8jMsnWQBqEk4/DYMz42gBV9P+2KjCqc"
securestore.setEncryptedData(console=CONSOLE, 
                                csrf_token=csrf_base, 
                                session_id=sid_base,
                                ) # allat is test data

resp = securestore.openEncryptedData(console=CONSOLE)
print(resp)
print(resp == (sid_base, csrf_base))