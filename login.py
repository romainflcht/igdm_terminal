from rich.prompt import Prompt, Confirm
from rich.console import Console
import requests
import os


def login(console: Console, headers: dict) -> tuple:
    """
    Function that handle the login feature.
    :param console: Console on which everything will be printed out.
    :param headers: headers of the request.
    :return: A valid session_id and csrf_token.
    """

    # Check if a session_id and csrf_token are already saved and valid.
    if os.path.isfile(os.path.join('cache', 'session_id')) and os.path.isfile(os.path.join('cache', 'csrf_token')):
        with open(os.path.join('cache', 'session_id'), 'r') as file:
            session_id = file.read()

        with open(os.path.join('cache', 'csrf_token'), 'r') as file:
            csrf_token = file.read()

    else:
        session_id = ''
        csrf_token = ''

    if check_session(console, headers, session_id, csrf_token):
        # Valid, returned.
        return session_id, csrf_token


    else:
        # Check if there is an unvalid session_id saved. If true, tell to the user.
        if session_id != '':
            console.print('[bold red]Votre session ID ou votre csrftoken ne sont plus valide, veuillez les modifier[/]')

            # Delete the old session_id.
            with open(os.path.join('cache', 'session_id'), 'w') as file:
                file.write('')

            with open(os.path.join('cache', 'csrf_token'), 'w') as file:
                file.write('')

        while True:
            # While the user hasn't input a correct session_id, keep asking.
            try:
                session_id, csrf_token = get_session_id(console)

                # Check if the session_id is valid:
                if check_session(console, headers, session_id, csrf_token):
                    console.print('[bold #2cb00b]Votre ID de session et votre csrftoken ont été validé ![/]')

                    # If so save it and return it.
                    save_session(console, session_id, csrf_token)
                    return session_id, csrf_token
                else:
                    # Else keep asking.
                    console.print('[bold red]Votre ID de session ou votre csrftoken ne sont pas valide, '
                                  'veuillez reéssayer...\n[/]')

            except KeyboardInterrupt:
                # Say goodbye when exiting :)
                console.print('\n' * 1000 + 'Au revoir :)')
                exit()


def get_session_id(console: Console) -> tuple:
    """
    Function that ask the user his SessionID and his CSRF_Token
    :param console: the SessionID and the CSRF_Token.
    :return:
    """

    console.print('[bold #1279e0 link=]Où trouvé mon session ID et mon CSRT Token Instagram Inc. ?[/]')

    # Ask the information needed.
    session_id = Prompt.ask('Veuillez entrer votre [bold #e0c112]session ID Instagram Inc. [/]'
                            '(La saisie ne sera pas affiché)', password=True)

    csrf_token = Prompt.ask('Veuillez entrer votre [bold #e0c112]CSRF Token d\'Instagram Inc. [/]'
                            '(La saisie ne sera pas affiché)', password=True)

    # return information.
    return session_id, csrf_token


def save_session(console: Console, session_id: str, csrf_token: str) -> None:
    """
    Function that save the session ID and CSRF token into a text file.
    :param console: Console on which everything will be printed out.
    :param session_id: Session ID that need to be saved.
    :param csrf_token: CSRF Token that need to be saved.
    :return: None
    """

    # Check if the user wnat to save it.
    if Confirm(console=console).ask('Voulez-vous savegarder vos informations de connexion pour plus tard ?'):
        try:
            # Write it into text files.
            with open(os.path.join('cache', 'session_id'), 'w') as session_file:
                session_file.write(session_id)

            with open(os.path.join('cache', 'csrf_token'), 'w') as csrf_token_file:
                csrf_token_file.write(csrf_token)

            console.print('[bold #2cb00b]Votre session a été sauvegardé pour les prochaines fois ![/]')
            return

        except FileNotFoundError:
            # No file were found.
            console.print('[bold red]Impossible d\'enregistrer votre session, fichiers manquants[/]')
            return

    else:
        # File not saved.
        console.print('[bold #e0c112]Votre session n\'a pas été sauvegardé...')
        return


def check_session(console: Console, headers: dict, session_id: str, csrf_token: str) -> bool:
    """
    Function that check if the session_id is valid.
    :param console: Console on which everything will be printed out.
    :param headers: Headers of the request.
    :param session_id: Session ID that need to be saved.
    :param csrf_token: CSRF Token that need to be saved.
    :return: Boolean that tell if the session_id is valid or not.
    """
    with console.status(status='[bold]Verifing your Session ID and CSRF Token with Instagram Inc.[/]', spinner='dots',
                        spinner_style='white'):

        # Make a request with the session_id.
        req = requests.get('https://i.instagram.com/api/v1/direct_v2/inbox/',
                           cookies={'sessionid': session_id, 'csrftoken': csrf_token},
                           headers=headers)

        # If the request is successful and can be converted in json, the session_id is valid.
        if req.status_code == 200:
            try:
                req.json()
                return True

            except requests.exceptions.JSONDecodeError:
                # Else it isn't.
                return False

        # Else it isn't.
        return False


if __name__ == '__main__':
    print('This code is intended to be imported...')
