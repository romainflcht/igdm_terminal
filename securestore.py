import blowfish # from [here](https://github.com/jashandeep-sohi/python-blowfish)
import os, json
from rich.prompt import Prompt, Confirm
from rich.console import Console
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
THIS IS A WWARNING TO EVERYONE ATTEMPTING TO UNDERSTAND THIS

this shitpile of code was written at midnight while running on enough coffe to kill an orca,
attempting to understand it might push you to sewerslide ideas, or consuming high amounts of bleach

-------
UPDATE: it is now 1:17am, i'm getting somewhere but the salt is being bitchy, might save it to it's own file to avoid confusion
eh, fuck it, lemme add a todo for tomorrow (well not tomorrow since it'll be the same day but you get it)

-------
UPDATE: it's said "tomorrow", blowfish is done, thx earlier me for leaving a TO DO
"""


def openEncryptedData(console: Console) -> tuple:
    """
    function to return the actual stored data, automatically prompt for required information from user
    data about the status is stored inside a json file of this structure at path `cache/encr.json`
    {
        "path": "full path to stored data"
        "style": "None|aes(WIP)|blowfish|system_wallet(WIP)"
        "level": "None:None|aes:[128, 256](WIP)|blowfish:ECB-CTS|system_wallet:(WIP)"
        "optional": [dependant on encryption used, usually salt data and such]
    }
    """
    encrpth = os.path.join('cache', 'securestore.json')
    with open(encrpth, 'r') as file:
        j = json.load(file)
    style = j["style"]
    level = j["level"]
    path  = j["path"]
    match style:
        case "None": # plain text stored inside json
            with open(path) as file:
                resp = json.load(file)
            return (resp['session_id'], resp['csrf_token'])
        case "blowfish":
            match level:
                case "ECB-CTS":
                    console.print(f"[bold #1279e0] encryption {style}-{level} détéctée")
                    passwd = Prompt.ask("veuillez entrer le mots de passe [bold red]Blowfish[/]"
                                        '(La saisie ne sera pas affiché)', password=True)
                    # deriving key from password
                    with open(os.path.join('cache', 'salt.bin'), 'rb') as file:
                        SALT = file.read()
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA512(),
                        salt=SALT,
                        length=56,
                        iterations=480000,
                    )
                    key = kdf.derive(str.encode(passwd))
                    cipher = blowfish.Cipher(key)
                    with open(path, 'rb') as file:
                        encr_data = file.read()
                    decrypted_bytes = b''.join(cipher.decrypt_ecb_cts(encr_data))
                    resp = json.loads(decrypted_bytes.decode(encoding='UTF-8'))
                    return (resp['session_id'], resp['csrf_token'])


def setEncryptedData(console: Console, session_id:str, csrf_token: str) -> None:
    """
    function to prompt for encryption to use for storage of both session_id and csrf_token
    available now:
    None:None -> clear text storage inside json file
    blowfish:ECB-CTS -> storage of data inside a json encoded as bytes, encrypted using blowfish
    """
    console.clear()
    available = [None, "Blowfish", "wallet", "AES"]
    available_dict = dict(Clear="stored in plain text", 
                                Blowfish="encrypted with blowfish",
                                AES="store in an aes encrypted file",
                                keychain="attempts to use the system wallet [not made, f*** you]"
                                )
    genstr = ""
    for i in range(len(available_dict)) :
        genstr += f'\n\t[bold red]{i+1}.[/] [yellow italic]{list(available_dict.keys())[i]}[/]: {available_dict[list(available_dict.keys())[i]]}'
    console.print(f"here you will be asked how you want to store your auth data{genstr}")
    ans = Prompt.ask("->", default=list(available_dict).index('Blowfish')+1)
    match int(ans):
        case 1: 
            # plain text storage
            with open(os.path.join('cache', 'securestore.json'), 'w') as file:
                json.dump(dict(style= "None", level= "None", path= str(os.path.join('cache', 'plain.json'))), file)
            with open(os.path.join('cache', 'plain.json'), "w") as file:
                json.dump(dict(session_id=session_id, csrf_token=csrf_token), file)
            return
        case 2:
            # blowfish storage
            console.print(f"[bold #1279e0] l'encryption Blowfish ECB-CTS dérive une clé de 56bit à partir d'un mots de passe")
            p_ok = False
            while p_ok == False:
                passwd = Prompt.ask("veuillez entrer le mots de passe [bold red]Blowfish[/]"
                                    '(La saisie ne sera pas affiché)', password=True)
                passwd2 = Prompt.ask("veuillez entrer à nouveau le mots de passe [bold red]Blowfish[/]"
                                    '(La saisie ne sera pas affiché)', password=True)
                if passwd != passwd2: console.print("[bold red] le mots de passe n'est pas identique, veuillez réessayer")
                else: p_ok = True
            SALT = os.urandom(16)
            # deriving key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA512(),
                salt=SALT,
                length=56,
                iterations=480000,
            )
            key = kdf.derive(str.encode(passwd))
            cipher = blowfish.Cipher(key)
            clear_str = json.dumps(dict(session_id=session_id, csrf_token=csrf_token))
            encr_data = b''.join(cipher.encrypt_ecb_cts(str.encode(clear_str, encoding='UTF-8')))
            with open(os.path.join('cache', 'securestore.json'), 'w') as file:
                json.dump(dict(style='blowfish', level='ECB-CTS', path=str(os.path.join('cache', 'blow_ecb_cts.bin'))), file)
            with open(os.path.join('cache', 'salt.bin'), 'wb') as file:
                file.write(SALT)
            with open(os.path.join('cache', 'blow_ecb_cts.bin'), 'wb') as file:
                file.write(encr_data)
            return
        case 3:
            # keyring storage
            console.print('[bold red]not yet implemented')
            exit()
        case 4:
            #aes storage
            # TODO : prompt for level [128, 256, 512]
            # TODO : handle key derivation, handle different encryption level
            console.print('[bold red]not yet implemented')
            exit()

def delete_sessions():
    filelist = ['securestore.json', 'clear.json', 'salt.bin', 'blowfish_ecb_cts.bin', 'aes.bin']
    for i in filelist :
        if os.path.isfile(os.path.join('cache', i)): os.remove(os.path.join('cache', i)) 