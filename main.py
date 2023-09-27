from rich.console import Console
import requests
from format_data import format_thread_selection
from send_direct_msg import send_message
from inbox import Inbox
from login import login
from HEADERS import HEADERS

# Create the request session that will be used for every component. 
SESSION = requests.session()
SESSION.headers.update(HEADERS)

# Console object were every print will be displayed. 
CONSOLE = Console()

# Change those numbers how you want. 
CONV_INBOX_NB = 15
CONV_ITEMS_NB = 20



if __name__ == '__main__':
    # Clear the screen.
    CONSOLE.print('\n' * 1000)

    # Get connection information and generate cookies for requests.
    session_id, csrf_token = login(CONSOLE, HEADERS)
    cookies = {
        'csrftoken': csrf_token,
        'sessionid': session_id,
    }


    # Create an unique session for every future requests. 
    SESSION.cookies.update(cookies)

    # Create inbox object.
    inbox = Inbox(SESSION, CONSOLE, True)

    while 1: 
        # Fetch inbox datas. 
        inbox.update_indox(CONV_INBOX_NB)
        inbox.show()

        # Ask the user the conversation that he want to see.
        try: 
            thread_id = format_thread_selection(CONSOLE, CONV_INBOX_NB)
        
        except KeyboardInterrupt:
            # Exit on CTRL+C. 
            CONSOLE.print('\n[bold green]Au revoir :)\n')
            exit()

        # Fetch items inside the selected thread.
        selected_thread = inbox.get_thread(thread_id)

        # Start a loop on the thread. 
        thread_loop_is_running = 1
        while thread_loop_is_running:
            # Clear the screen and update the thread items. 
            CONSOLE.print('\n' * 1000)
            selected_thread.update_thread(CONV_ITEMS_NB)
            selected_thread_items = selected_thread.get_items()

            # Show every item in the thread.
            for item in selected_thread_items:
                item.show()

            # Ask the user for a message to send or if he want to quit the selected thread. 
            reponse = send_message(SESSION, CONSOLE, selected_thread.get_thread_id())

            # Check the response code of the send message request. 
            if reponse == 1: 
                # Sent successfully. 
                CONSOLE.print('[green bold]\u2713[/] Message envoyé !')
            
            elif reponse == -1:
                # User ask to update the thread. 
                CONSOLE.print('[yellow bold]\u27F3[/] Mise à jour de la conversation...')
            
            elif reponse == -2:
                # User ask to quit the selected thread. 
                thread_loop_is_running = 0

                # Clear the sreen. 
                CONSOLE.print('\n' * 1000)
            
            else:
                # Error when sending the message.
                CONSOLE.print('[red bold]\u26A0[/] Il y a eu un problème lors de l\'envoie du message...')

