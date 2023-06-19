from rich.console import Console
from format_data import format_thread_selection
from inbox import Inbox
from login import login

HEADERS = {
    'authority': 'www.instagram.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/107.0.0.0 Safari/537.36',
    'x-ig-app-id': '936619743392459',
}

CONV_INBOX_NB = 10
CONV_ITEMS_NB = 15
CONSOLE = Console()

if __name__ == '__main__':
    # Clear the screen.
    CONSOLE.print('\n' * 1000)

    # Get connection information and generate cookies for requests.
    session_id, csrf_token = login(CONSOLE, HEADERS)
    cookies = {
        'csrftoken': csrf_token,
        'sessionid': session_id,
    }

    # Fetch inbox datas.
    inbox = Inbox(CONSOLE, cookies, HEADERS)
    inbox.update_indox(CONV_INBOX_NB)
    inbox.show()

    # Ask the user the conversation that he want to see.
    thread_id = format_thread_selection(CONSOLE, CONV_INBOX_NB)

    # Fetch items inside the thread.
    selected_thread = inbox.get_thread(thread_id)
    selected_thread.update_thread(CONV_ITEMS_NB)
    selected_thread_items = selected_thread.get_items()

    # Show every item in the thread.
    for item in selected_thread_items:
        item.show()
