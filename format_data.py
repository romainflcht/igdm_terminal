from fetch_data import fetch_username_by_id, fetch_profile_pic_by_id
from securestore import delete_sessions
from rich.console import Console
from rich.prompt import IntPrompt
from PIL import Image
import datetime
import requests
import re


def format_timestamp(timestamp: int) -> str:
    """
    Function that format timestamps of every item.
    :param timestamp: Timestamp to format.
    :return: Formatted timestamp.
    """
    return datetime.datetime.fromtimestamp(float(str(timestamp)[0:10])).strftime('%d/%m/%y à %H:%M')


def format_duration(duration: int) -> str:
    """
    Function that format duration of voice_media item.
    :param duration: Duration of a voice message to format.
    :return: Formatted duration.
    """
    return str(datetime.timedelta(milliseconds=duration))[0:-7]


def format_reaction(session: requests.Session, reactions: dict) -> str:
    """
    Function that format reactions on an item.
    :param session: Session that contain cookies and headers.
    :param reactions: Dict that contain reactions on the item.
    :return: Formatted reaction.
    """

    # Check if there is reactions on the massage.
    if reactions is None:
        return ''

    emojis = {}
    for reaction in reactions.get('emojis'):
        # Extract every reaction and asign them to user_id that put the reaction.
        emojis[reaction['emoji']] = []
        emojis[reaction['emoji']].append(reaction['sender_id'])

    # Format every reaction.
    formatted_reaction = '\n'
    for emoji in emojis:
        for user in emojis[emoji]:
            formatted_reaction += fetch_profile_pic_by_id(session, user)
        formatted_reaction += emoji + ' '

    return formatted_reaction


def format_last_item(session: requests.Session, item: dict) -> tuple:
    """
    Function that format the last item sent in a thread to be displayed in the inbox.
    :param session: Session that contain cookies and headers.
    :param item: Last item that was sent in a thread.
    :return: Formatted last item with timestamp.
    """

    # Check the item type to diplay the correct message.
    if item.get('item_type') == 'text':
        # item is text.
        return item['text'], item['timestamp']

    elif item.get('item_type') == 'link':
        # item is a text with links.
        return item['link']['text'], item['timestamp']

    elif item.get('item_type') == 'action_log':
        # Item is reaction.
        return fetch_username_by_id(session, item.get('user_id')) + ' à aimé un message', item['timestamp']

    elif item.get('item_type') == 'reel_share':
        # Item is a reaction to a story.

        # Get the text of the reply.
        text = item['reel_share']['text']

        if item['is_sent_by_viewer']:
            story_owner = fetch_username_by_id(session, item['reel_share']['reel_owner_id'])
            return f'Vous avez réagis à la story de {story_owner} : {text}', item['timestamp']

        else:
            sender_username = fetch_username_by_id(session, item['user_id'])
            return sender_username + f'a réagis à votre story : {text}', item['timestamp']

    elif item.get('item_type') == 'story_share':
        # item is a story.
        item_type = 'une story.'

    elif item.get('item_type') == 'clip':
        # item is a reel.
        item_type = 'un réel.'

    elif item.get('item_type') == 'media_share':
        # item is a post.
        item_type = 'un post.'

    elif item.get('item_type') == 'raven_media':
        # item is a one-shot media.
        item_type = 'une ' + ('photo.' if item['raven_media'].get('media_type') else 'vidéo.')

    elif item.get('item_type') == 'animated_media':
        # item is a GIF.
        item_type = 'un GIF.'

    elif item.get('item_type') == 'media':
        # item is a media.
        item_type = 'une ' + ('photo.' if item['media'].get('media_type') else 'vidéo.')

    elif item.get('item_type') == 'voice_media':
        # item is a voice message.
        item_type = 'un message vocal.'

    elif item.get('item_type') == 'story_share':
        # item is a story.
        item_type = 'une story.'

    else:
        # item_type not supported.
        item_type = f'un élément [bold red]non supporté ({item.get("item_type")})[/].'

    # Change the message depending on which user sent the message.
    if item.get('is_sent_by_viewer'):
        user = 'Vous avez '
    else:
        user = fetch_username_by_id(session, item.get('user_id')) + ' à '

    # construct the final message with the sender and the item type.
    return user + 'envoyé ' + item_type, item['timestamp']


def format_img_from_path(path: str, height: int) -> str:
    """
    Function that fetch an image from a URL and format it to be able to render it in the _console.
    :param path: Local path to the image.
    :param height: Height of the formatted image.
    :return: The formatted image ready to be rendered.
    """
    # Open and resize the image.
    img = Image.open(path)
    img_ratio = img.width / img.height

    new_height = height
    new_width = int(img_ratio * new_height) * 2

    img = img.resize((new_width, new_height))

    # Format the image into a string.
    formatted_img = ''
    for line in range(img.height - 1):
        for pixel in range(img.width):
            r1, g1, b1 = img.getpixel((pixel, line + 1))
            r2, g2, b2 = img.getpixel((pixel, line))

            formatted_img += '[#{:02x}{:02x}{:02x} on #{:02x}{:02x}{:02x}]▄[/]'.format(r1, g1, b1, r2, g2, b2)
        formatted_img += '\n'

    # return the formatted image.
    return formatted_img


def get_smallest_img(candidates: list):
    """
    Function that get the smallest image to save memory.
    :param candidates: List that contain dict with height, width and url.
    :return: The url of the smallest image available.
    """

    # Get the size and url of the first element to compare with the others.
    is_square = candidates[0]['height'] == candidates[0]['width']
    minimum_size = candidates[0]['height'] * candidates[0]['width']
    url = candidates[0]['url']

    # Search the smallest image.
    for index in range(1, len(candidates)):
        # Calculate the size of the image.
        current_size = candidates[index]['height'] * candidates[index]['width']

        if is_square == (candidates[index]['height'] == candidates[index]['width']):
            if current_size < minimum_size:
                minimum_size = current_size
                url = candidates[index]['url']

    return url


def format_link(text: str):
    """
    Function that parse string text by transforming links in the text into clickable links.
    :param text: Text with links.
    :return: The formatted text with clickable links.
    """

    # find every link in the string.
    links = re.findall(r'(https?://\S+)', text)

    parsed_text = ''
    index = 0

    # Parse the string by adding tags around the link.
    for link in links:
        # Find the begining index of the link.
        beginning = text.find(link)

        # Add the text before the link, add the tag, the link and the closing tag.
        parsed_text += text[index:beginning] + f'[link={link}]' + link + '[/]'
        index = beginning + len(link)

    # Add the rest of the string that contain no link.
    parsed_text += text[index:]

    return parsed_text


def format_thread_selection(console: Console, max_thead_nb: int) -> int:
    """
    Function that ask thread number to the user and return his choice parsed.
    :param console:
    :param max_thead_nb:
    :return:
    """
    is_valid_thread_id = False
    thread_id = 0

    while not is_valid_thread_id:
        # Ask the conversation number.
        console.print('[italic grey50]Entrer [bold]0[/bold] pour se déconnecter ou [bold]CRTL+C[/bold] pour quitter le programme.[/]')
        thread_id = IntPrompt.ask(f'Selectionnez la conversation : (1-{max_thead_nb})')

        if thread_id == 0:
            delete_sessions()
            console.print('\n[bold green]Vous avez été déconnecté, au revoir :)\n')
            exit()

        # Check if the number is valid.
        if 0 < thread_id <= max_thead_nb:
            is_valid_thread_id = True

        else:
            # Tell the user that hiw choice is not correct.
            console.print('La conversation sélectionné n\'existe pas, veuillez réessayer...')
            is_valid_thread_id = False

    # return the conversation number.
    return thread_id - 1


if __name__ == '__main__':
    print('This code is intended to be imported...')
