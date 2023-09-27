import uuid
import requests
from rich.console import Console
from rich.prompt import Prompt
import shutil


BROADCAST_URL = 'https://www.instagram.com/api/v1/direct_v2/threads/broadcast/'


def send_item(session: requests.Session, text: str, thread_id: str, user_id:str = '') -> bool:
    """
    Function that send a direct (text) message to an instagram thread.
    :param session: Session that contain cookies and headers.
    :param text: text to send. 
    :param thread_id: the identifier of the conversation you want to send your message to. 
    :param user_id: the identifier of the user that send the message. 
    :return: 1 if the request was successful, 0 otherwise. 
    """
    
    # Check if data is in the correct format.

    if session is None: 
        return 0

    if  thread_id == '':
        return 0
    
    if not isinstance(text, str):
        return 0

    # Build the data structure to send to instagram. 
    data = {
        'action': 'send_item',
        'client_context': str(uuid.uuid4()),
        'recipient_users': f'[[{user_id}]]',
        'thread_ids': f'[{thread_id}]',
        'text': str(text),
    }

    # Make the request with a custom header to be able to send message and check if it was successful.
    response = session.post(BROADCAST_URL + 'text/', data=data)
    if response.status_code == 200: 
        # Message sent successfully ! 
        return 1

    # Message did not sent properly.
    print(response.status_code)
    return 0


def ask_message_to_send(console: Console) -> str:
    """
    Function that ask the user a string and format it.
    :param console: Console object that contain every info on the current console.
    :return: The formatted string.
    """

    # Get the width of the console. 
    cols, _ = shutil.get_terminal_size()

    # Create a small UI and ask the user a string. 
    console.print('━' * cols)
    console.print('[italic grey50]Utiliser [white bold]CTRL+C[/white bold] pour quitter le programme.[/]')
    console.print('[italic grey50]Pour un retour à la ligne, écrivez [white bold]\\n[/white bold]'
                  ' dans votre message.[/]')
    console.print('[italic grey50][white bold]ENTER[/white bold] pour envoyer, [white bold]u[/white bold]'
                  ' pour mettre à jour les messages ou [white bold]q[/white bold] pour quitter la conversation[/]')
    try: 
        text_to_send = Prompt.ask('Votre message ')
    
    except KeyboardInterrupt:
        console.print('\n[bold green]Au revoir :)\n')
        exit()

    # Format and return the text. 
    text_to_send = text_to_send.replace('\\n', '\n')
    return text_to_send


def send_message(session: requests.Session, console: Console, thread_id: str, user_id:str = '') -> int:
    """
    Function that handle sending message to a thread.
    :param session: Session that contain cookies and headers.
    :param console: Console object that contain every info on the current console.
    :param thread_id: Thread id to fetch items.
    :param user_id: Id of the sender (Not necessary)
    :return: 1 if successful, 0 otherwise.
    """

    # Get the message from the user. 
    message_to_send = ask_message_to_send(console)

    # Check if the user want to quit the conversation. 
    if message_to_send == 'q':
        return -2

    elif message_to_send == 'u' or message_to_send == '':
        return -1
    
    # make the request and return the response code.
    return send_item(session, message_to_send, thread_id, user_id)


if __name__ == '__main__': 
    print('This code is intended to be imported...')
