from format_data import format_last_item
from rich.console import Console
from thread import Thread
import requests


class Inbox:
    URL = 'https://i.instagram.com/api/v1/direct_v2/inbox/'

    def __init__(self, console: Console, cookies: dict, headers: dict) -> None:
        """
        Constructor of the Inbox class.
        :param cookies: Cookies that contain session id.
        :param headers: Headers that contain header info (To not be blocked by Instagram server).
        """
        self._cookies = cookies
        self._headers = headers
        self._session = requests.Session()
        self._console = console
        self._threads = []
        self._unseencount = 0

        self._session.headers.update(headers)
        self._session.cookies.update(cookies)

    def update_indox(self, nb_threads: int) -> None:
        """
        Method that update the inbox by fetching every thread in the inbox.
        :param nb_threads: Number of threads to get.
        """
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
                                                thread['read_state']))

            else:
                self._console.print(f' -> [bold #ff0000]({req.status_code}) Error when fetching instagram server.[/]')

    def show(self):
        self._console.clear()
        self._console.print(f'Inbox ' + ('[#ff0000]' if self._unseencount else '[#ffffff]') +
                            f'({self._unseencount})[/]', style='bold')

        for index, thread in enumerate(self._threads):
            # Print thread with the index that is used to open the conversation.
            thread.show(index + 1)

        # Footer :).
        self._console.print('coded by romainflcht', style='#3b3b3b', justify='right')

    def get_thread(self, thread_id):
        return self._threads[thread_id]


if __name__ == '__main__':
    print('This code is intended to be imported...')
