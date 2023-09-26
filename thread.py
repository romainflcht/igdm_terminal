from fetch_data import fetch_profile_pic_by_id
from format_data import format_timestamp, get_smallest_img
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
import items


class Thread:
    URL = 'https://i.instagram.com/api/v1/direct_v2/threads/'

    def __init__(self, session: requests.Session, console: Console, thread_id: str, thread_title: str, users: dict,
                 last_item_sent: tuple, muted: bool, readed: bool) -> None:
        """
        Constructor of the Thread class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param thread_id: Thread id to fetch items.
        :param thread_title: Name of the group or thread.
        :param users: Users in the group or thread.
        :param last_item_sent: Last item that is print below the username in the inbox.
        :param muted: Is the thread muted.
        :param readed: Is the thread readed.
        """
        self._session = session
        self._console = console
        self._id = thread_id
        self._title = thread_title
        self._users = []
        self._last_item = last_item_sent
        self._muted = muted
        self._readed = readed
        self._items = []

        for user in users:
            self._users.append(user.get('pk'))

    def update_thread(self, nb_items):
        """
        Method that update the thread by fetching every item sent in the thread.
        :param nb_items: Number of items to get.
        """

        # Delete previous items in the thread. 
        self._items = []

        with self._console.status(status='[bold]Fetching direct messages from Instagram Inc.[/bold]',
                                  spinner='dots', spinner_style='white'):

            # Request items of the thread.
            req = self._session.get(Thread.URL + self._id, params={'limit': nb_items})

        # Check if the request is successful.
        if req.status_code == 200:
            response = req.json()

            # For every item in the thread create an object of the item type.
            for item in response['thread']['items']:
                if item.get('item_type') == 'text':
                    # Item is a text.
                    self._items.append(items.Text(self._session,
                                                  self._console,
                                                  item['is_sent_by_viewer'],
                                                  item['user_id'],
                                                  item['timestamp'],
                                                  item['text'],
                                                  item.get('reactions')))

                elif item.get('item_type') == 'link':
                    # Item is a link.
                    self._items.append(items.Link(self._session,
                                                  self._console,
                                                  item['is_sent_by_viewer'],
                                                  item['user_id'],
                                                  item['timestamp'],
                                                  item['link']['text'],
                                                  item.get('reactions')))

                elif item.get('item_type') == 'clip':
                    # Item is a clip.
                    first_frame = get_smallest_img(item['clip']['clip']['image_versions2']['candidates'])

                    self._items.append(items.Clip(self._session,
                                                  self._console,
                                                  item['is_sent_by_viewer'],
                                                  item['user_id'],
                                                  item['timestamp'],
                                                  first_frame,
                                                  item['clip']['clip']['video_versions'][0]['url'],
                                                  item['clip']['clip']['video_duration'],
                                                  item.get('reactions')))

                elif item.get('item_type') == 'media_share':
                    # Item is a post (one item post or multiple items post).
                    
                    # Get the image id that was sent (to show the correct image of the post).
                    img_id = item['media_share'].get('carousel_share_child_media_id')
                    if img_id is None:
                        # If there is no id, the post contain only one image, fetch the url.
                        post_img = get_smallest_img(item['media_share']['image_versions2']['candidates'])
                    else:

                        # Looking for the correct image attached to the id.
                        for img in item['media_share']['carousel_media']:
                            if img['id'] == img_id:
                                # If the ids match, fetch it.
                                post_img = get_smallest_img(img['image_versions2']['candidates'])
                                break

                        else:
                            # id not found (Should be impossible).
                            post_img = '[red]Ce post ne peut pas être chargé...[/]'

                    # Create the object and store it.
                    self._items.append(items.MediaShare(self._session,
                                                        self._console,
                                                        item['is_sent_by_viewer'],
                                                        item['user_id'],
                                                        item['timestamp'],
                                                        post_img,
                                                        item['media_share']['code'],
                                                        item['media_share']['caption']['text'],
                                                        item.get('reactions')))


                elif item.get('item_type') == 'voice_media':
                    # Item is a voice message.
                    self._items.append(items.VoiceMedia(self._session,
                                                        self._console,
                                                        item['is_sent_by_viewer'],
                                                        item['user_id'],
                                                        item['timestamp'],
                                                        item['voice_media']['media']['audio']['audio_src'],
                                                        item['voice_media']['media']['audio']['duration'],
                                                        item.get('reactions')))

                elif item.get('item_type') == 'raven_media':
                    # Item is a one shot media.
                    self._items.append(items.RavenMedia(self._session,
                                                        self._console,
                                                        item.get('is_sent_by_viewer'),
                                                        item.get('user_id'),
                                                        item.get('timestamp'),
                                                        item['raven_media'].get('media_type'),
                                                        item.get('reactions')))

                elif item.get('item_type') == 'media':
                    # Item is a media.
                    url = get_smallest_img(item['media']['image_versions2']['candidates'])
                    self._items.append(items.Media(self._session,
                                                   self._console,
                                                   item.get('is_sent_by_viewer'),
                                                   item.get('user_id'),
                                                   item.get('timestamp'),
                                                   item['media'].get('media_type'),
                                                   url,
                                                   item.get('reactions')))

                elif item.get('item_type') == 'story_share':
                    # Item is a story share.

                    # Set the story as unavailable before check. 
                    first_frame = None
                    url = None

                    # Check if the story is available and set first_frame and url accordingly.  
                    if item['story_share'].get('media') is not None:
                        # Story is available, define the first frame.
                        first_frame = get_smallest_img(item['story_share']['media']['image_versions2']['candidates'])
                        url = first_frame

                        if item['story_share']['media']['media_type'] != 1:
                            url = item['story_share']['media']['video_versions'][0]['url']

                    self._items.append(items.StoryShare(self._session,
                                                        self._console,
                                                        item['is_sent_by_viewer'],
                                                        item['user_id'],
                                                        item['timestamp'],
                                                        first_frame,
                                                        url,
                                                        item.get('reactions')))

                elif item.get('item_type') == 'reel_share':
                    # Item is a story share.

                    first_frame = None
                    url = None

                    # Check if the story is available and set first_frame and url accordingly.  
                    if item['reel_share'].get('media') is not None:
                        first_frame = get_smallest_img(item['reel_share']['media']['image_versions2']['candidates'])
                        url = first_frame

                        if item['reel_share']['media']['media_type'] != 1:
                            url = item['reel_share']['media']['video_versions'][0]['url']

                    self._items.append(items.ReelShare(self._session,
                                                       self._console,
                                                       item['is_sent_by_viewer'],
                                                       item['user_id'],
                                                       item['timestamp'],
                                                       first_frame,
                                                       item['reel_share']['text'],
                                                       url,
                                                       item['reel_share']['reel_owner_id'],
                                                       item.get('reactions')))
                    
                elif item.get('item_type') == 'placeholder':
                    pass
                    self._items.append(items.Placeholder(self._session, 
                                                         self._console, 
                                                         item['is_sent_by_viewer'],
                                                         item['user_id'],
                                                         item['timestamp'],
                                                         item['placeholder']['message']))

                else:
                    # Ignore action_log item because they are not supposed to be displayed.
                    if not item.get('item_type') == 'action_log':
                        self._console.print(f'[bold red]Item type {item["item_type"]} not supported...[/]')

            # Sort every item by time.
            self._items.sort(key=lambda elt: elt.get_timestamp())

        else:
            self._console.print(f' -> [bold red]({req.status_code}) Error when fetching instagram server.[/]')

    def show(self, thread_index: int):
        """
        Function that print the thread on the screen.
        :param thread_index: Number to display beside the username. Number that is used to open the thread by
        choosing this number on the main menu.
        """
        profile_pic = ''
        for user in self._users:
            # fetch profile picture for every user in the thread.
            profile_pic += fetch_profile_pic_by_id(self._session, user) + ' '

        thread = Table.grid(expand=True)

        # Create the structure to display the thread correctly in the inbox.
        thread.add_column()
        thread.add_column(justify="right")

        # Print every info.
        thread.add_row(f'({thread_index}) ' + profile_pic + ('[#ff0000]•[/#ff0000] ' if self._readed else '') +
                       self._title + (' (🔇)' if self._muted else ''), '[bold]' + format_timestamp(self._last_item[1]))
        thread.add_row(('[bold]' if self._readed else '[#3b3b3b]') + self._last_item[0])
        self._console.print(Panel(thread))

    def get_items(self):
        """
        Getter function that return the list of every items of the thread. 
        :return: The list of every items of the thread. 
        """
        return self._items
    
    def get_thread_id(self):
        """
        Getter function that return the id of the thread. 
        :return: The id of the thread. 
        """
        return self._id

if __name__ == '__main__':
    print('This code is intended to be imported...')
