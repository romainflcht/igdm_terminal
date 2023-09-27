from format_data import format_last_item
from rich.console import Console
from thread import Thread
import requests


class Inbox:
    URL = 'https://i.instagram.com/api/v1/direct_v2/inbox/'

    def __init__(self, session: requests.Session, console: Console, debug:bool = False) -> None:
        """
        Constructor of the Inbox class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param debug: Turn on or off debug mode.
        """
        self._session = session
        self._console = console
        self._debug = debug
        self._threads = []
        self._unseencount = 0


    def update_indox(self, nb_threads: int) -> None:
        """
        Method that update the inbox by fetching every thread in the inbox.
        :param nb_threads: Number of threads to get.
        """

        #  Delete previous threads in the inbox. 
        self._threads = []

        with self._console.status(status='[bold]Fetching direct messages from Instagram Inc.[/]',
                                  spinner='dots', spinner_style='#ffffff'):

            # Request threads of the inbox.
            req = self._session.get(Inbox.URL, params={'limit': nb_threads})

            # Check if the request is successful.
            if req.status_code == 200:
                response = req.json()['inbox']
                self._unseencount = response['unseen_count']

                for thread in response['threads']:
                    # Create a Thread object and save it.
                    self._threads.append(Thread(self._session,
                                                self._console,
                                                thread['thread_id'],
                                                thread['thread_title'],
                                                thread['users'],
                                                format_last_item(self._session, thread['items'][0]),
                                                thread['muted'],
                                                thread['read_state'],
                                                self._debug))

            else:
                self._console.print(f' -> [bold #ff0000]({req.status_code}) Error when fetching instagram server.[/]')

    def show(self):
        self._console.clear()
        self._console.print(f'Inbox ' + ('[#ff0000]' if self._unseencount else '[#ffffff]') +
                            f'({self._unseencount})[/]', style='bold')

        for index, thread in enumerate(self._threads):
            # Print thread with the index that is used to open the conversation.
            if self._debug: 
                self._console.print(f'({index + 1}) THREAD ID -> {thread._id}')
            thread.show(index + 1)

        # Footer :).
        self._console.print('coded by romainflcht', style='#3b3b3b', justify='right')

    def get_thread(self, thread_id):
        return self._threads[thread_id]


if __name__ == '__main__':
    print('This code is intended to be imported...')
