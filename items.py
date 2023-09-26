from fetch_data import fetch_username_by_id, fetch_profile_pic_by_id, fetch_img_from_url
from format_data import format_timestamp, format_reaction, format_duration, format_link
from rich.console import Console
import requests


class Text:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, text: str, reactions: dict) -> None:
        """
        Constructor of the Text class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param text: Text of this item.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._text = text
        self._reactions = reactions

    def show(self):
        # Fetch every data needed.
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)

        # Check if the item is sent by the owner of the account. 
        if self._issentbyviewer:
            # display the item. 
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'{self._text}'
                                f'{reactions}\n', soft_wrap=True)

        else:
            # display the item. 
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'{self._text}'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class Link:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, text: str, reactions: dict) -> None:
        """
        Constructor of the Link class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param text: Text of this item.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._text = text
        self._reactions = reactions

    def show(self):
        # Fetch every data needed. 
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        text = format_link(self._text)
        reactions = format_reaction(self._session, self._reactions)

        # Check if the item is sent by the owner of the account. 
        if self._issentbyviewer:
            # display the item. 
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'{text}'
                                f'{reactions}\n', soft_wrap=True)

        else:
            # display the item. 
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'{text}'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class Clip:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: str,
                 timestamp: int, first_frame: str, src: str, duration: int, reactions: dict):
        """
        Constructor of the Clip class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param src: URL of the clip.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._first_frame = first_frame
        self._src = src
        self._duration = duration
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)
        first_frame = fetch_img_from_url(self._session, self._console, self._first_frame)

        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n\n'
                                f'[link={self._src}]{first_frame}[/]'
                                f'([#0373fc]{self._duration}[/]s)\n'
                                f'[bold]Crtl+Clic to open[/]'
                                f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n\n'
                                f'[link={self._src}]{first_frame}[/]'
                                f'([#0373fc]{self._duration}[/]s)\n'
                                f'[bold]Crtl+Clic to open[/]'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class MediaShare:
    URL = 'https://www.instagram.com/p/'

    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: str,
                 timestamp: int, post_img: str, url_code: str, caption: str, reactions: dict):
        """
        Constructor of the Clip class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param post_img: Image that the post contain.
        :param url: URL of to the post.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._post_img = post_img
        self._url_code = url_code
        self._caption = caption
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)
        post_img = fetch_img_from_url(self._session, self._console, self._post_img)

        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'[link={self.URL + self._url_code}]{post_img}[/]'
                                f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'[link={self.URL + self._url_code}]{post_img}[/]'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class VoiceMedia:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, audio_src: str, audio_duration: int, reactions: dict):
        """
        Constructor of the Clip class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param audio_src: Url of the audio.
        :param audio_duration: Duration in millisecond of the audio.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._src = audio_src
        self._duration = audio_duration
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)

        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'[link={self._src}]▶[/] 🔘─────────────────────({format_duration(self._duration)})'
                                f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'[link={self._src}]▶[/] 🔘─────────────────────({format_duration(self._duration)})'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class RavenMedia:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, media_type: str, reactions: dict):
        """
        Constructor of the RavenMedia class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param session: Session that contain cookies and headers.
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param media_type: If the media is video or photo.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._media_type = media_type
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)

        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\nVous avez envoyé une '
                                + ('photo.' if self._media_type == 1 else 'vidéo.') + f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n{username} a envoyé '
                                f'une ' + ('photo.' if self._media_type == 1 else 'vidéo.') + f'{reactions}\n',
                                soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class Media:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, media_type: str, src: str, reactions: dict):
        """
        Constructor of the RavenMedia class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param media_type: If the media is video or photo.
        :param src: Url that lead to the media.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._media_type = media_type
        self._src = src
        self._reactions = reactions

    def show(self):
        if self._media_type == 1:
            username = fetch_username_by_id(self._session, str(self._sender_id))
            profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
            reactions = format_reaction(self._session, self._reactions)
            media = fetch_img_from_url(self._session, self._console, self._src)

            if self._issentbyviewer:
                self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                    f'{media}'
                                    f'{reactions}\n', soft_wrap=True)

            else:
                self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                    f'{media}'
                                    f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class StoryShare:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, first_frame: str, url: str, reactions: dict):
        """
        Constructor of the StoryShare class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param first_frame: First frame of the story (image if the story is an image).
        :param url: Url that lead to the story media.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._first_frame = first_frame
        self._url = url
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)
        
        # set the text to display as unavailable and check after. 
        display_text = '[red italic]Cette story n\'est plus disponible...\n[/]'

        # Check if the story is available. 
        if self._first_frame is not None and self._url is not None:
            first_frame = fetch_img_from_url(self._session, self._console, self._first_frame)
            display_text = f'[link={self._url}]{first_frame}[/]'


        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                'Vous avez partagé une story.\n'
                                f'{display_text}'
                                f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                'A partagé une story.\n'
                                f'{display_text}'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


class ReelShare:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, first_frame: str, text: str, url: str, story_owner_id: str, reactions: dict):
        """
        Constructor of the ReelShare class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param issentbyviewer: Boolean that is true if the item is sent by the user, false otherwise. 
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param first_frame: First frame of the story (image if the story is an image).
        :param text: Text that come with the story share.
        :param url: Url that lead to the story media.
        :param reactions: Contain reactions of every user.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._first_frame = first_frame
        self._text = text
        self._url = url
        self._story_owner_id = story_owner_id
        self._reactions = reactions

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))
        reactions = format_reaction(self._session, self._reactions)
        first_frame = fetch_img_from_url(self._session, self._console, self._first_frame)

        # set the text to display as unavailable and check after. 
        display_text = '[red italic]Cette story n\'est plus disponible...\n[/]'

        # Check if the story is available. 
        if self._first_frame is not None and self._url is not None:
            first_frame = fetch_img_from_url(self._session, self._console, self._first_frame)
            display_text = f'[link={self._url}]{first_frame}[/]'

        if self._issentbyviewer:
            story_owner = fetch_username_by_id(self._session, str(self._story_owner_id))
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'Vous avez réagi a la story de {story_owner}.\n'
                                f'{display_text}'
                                f'{self._text}'
                                f'{reactions}\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'A réagi a votre story.\n'
                                f'{display_text}'
                                f'{self._text}'
                                f'{reactions}\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp
    

class Placeholder:
    def __init__(self, session: requests.Session, console: Console, issentbyviewer: bool, sender_id: int,
                 timestamp: int, message: str):
        """
        Constructor of the Placeholder class.
        :param session: Session that contain cookies and headers.
        :param console: Console object that contain every info on the current console.
        :param sender_id: Instagram ID of the user that send this item.
        :param timestamp: Timestamp of this item.
        :param message: The message inside the placeholder.
        """
        self._session = session
        self._console = console
        self._issentbyviewer = issentbyviewer
        self._sender_id = sender_id
        self._timestamp = timestamp
        self._message = message

    def show(self):
        username = fetch_username_by_id(self._session, str(self._sender_id))
        profile_pic = fetch_profile_pic_by_id(self._session, str(self._sender_id))

        # Display the placeholder message. 
        if self._issentbyviewer:
            self._console.print(f'{profile_pic} ({format_timestamp(self._timestamp)}) {username}\n'
                                f'[red italic]{self._message}[/]\n', soft_wrap=True)

        else:
            self._console.print(f'{username} ({format_timestamp(self._timestamp)}) {profile_pic}\n'
                                f'[red italic]{self._message}[/]\n', soft_wrap=True, justify='right')

    def get_timestamp(self):
        """
        Function that return the timestamp of the item. Useful to sort items of a thread in the right order.
        :return: Timestamp of the item.
        """
        return self._timestamp


if __name__ == '__main__':
    print('This code is intended to be imported...')
