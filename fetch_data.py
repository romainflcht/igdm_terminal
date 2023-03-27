from rich.console import Console
from PIL import Image
import requests
import json
import os


def fetch_username_by_id(session: requests.session, user_id: str) -> str:
    """
    Function that fetch the IG username linked to the ID.
    :param session: Session that contain cookies and headers.
    :param user_id: Instagram User ID.
    :return: The username linked to the user ID.
    """
    with open(os.path.join('cache', 'saved_usernames.json'), 'r') as save_file:
        data = json.load(save_file)

    # Check if the username is in the cache if not request the username and save it.
    username = data.get(user_id)
    if username is None:
        req = session.get('https://i.instagram.com/api/v1/users/' + user_id + '/info/')

        # Check if the request is successful.
        if req.status_code == 200:

            # Fetch the username and save it into the cache/saved_usernames.json file.
            username = req.json()['user'].get('username')
            data[user_id] = username
            with open(os.path.join('cache', 'saved_usernames.json'), 'w') as save_file:
                json.dump(data, save_file)

        else:
            # The connection was not successful.
            print(f' -> [{req.status_code}] Error when fetching instagram server.')

    return username


def fetch_profile_pic_by_id(session: requests.Session, user_id: str) -> str:
    """
        Function that fetch the IG profile picture linked to the ID.
        :param session: Session that contain cookies and headers.
        :param user_id: Instagram User ID.
        :return: The 4 colors of the profile picture.
        """
    with open(os.path.join('cache', 'saved_profile_pic.json'), 'r') as save_file:
        data = json.load(save_file)

    # Check if the profile picture is in the cache if not request it and save it.
    colors = data.get(user_id)
    if colors is None:
        colors = []
        req = session.get('https://i.instagram.com/api/v1/users/' + user_id + '/info/')

        # Check if the request is successful.
        if req.status_code == 200:

            # Fetch the profile picture url and request it.
            profile_pic_url = req.json()['user'].get('profile_pic_url')
            req = session.get(profile_pic_url, stream=True)

            # Check if the request is successful.
            if req.status_code == 200:
                profile_pic = Image.open(req.raw).resize((2, 2))

                for index_width in range(profile_pic.width):
                    for index_height in range(profile_pic.height):

                        r, g, b = profile_pic.getpixel((index_width, index_height))
                        colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b))

                data[user_id] = colors
                with open(os.path.join('cache', 'saved_profile_pic.json'), 'w') as save_file:
                    json.dump(data, save_file)

    return f'[{colors[0]} on {colors[1]}]▄[/][{colors[2]} on {colors[3]}]▄[/]'


def fetch_img_from_url(session: requests.Session, console: Console, url: str) -> str:
    """
    Function that fetch an image from a URL and format it to be able to render it in the _console.
    :param session: Session that contain cookies and headers.
    :param console: Console object that contain every info on the current console.
    :param url: URL of the image.
    :return: The formatted image ready to be rendered.
    """

    # Fetch raw data of the image.
    req = session.get(url, stream=True)

    # check if the request is successful.
    if req.status_code == 200:
        # Open and resize the image.
        img = Image.open(req.raw)
        img_ratio = img.width / img.height

        # The resize depend on if the image is portrait or landscape.
        if img.height > img.width:
            # Image is portrait, define a new height and find the new width using the image ratio.
            new_height = console.height // 2
            new_width = int(img_ratio * new_height) * 2

        else:
            # Image is landscape or square, define a new width and find the new height using the image ratio.
            new_width = console.width // 2
            new_height = int(img_ratio * new_width) // 2

        img = img.resize((new_width, new_height))

        # Format the image into a string.
        formatted_img = ''
        for line in range(img.height - 1):
            for pixel in range(img.width):
                r1, g1, b1 = img.getpixel((pixel, line + 1))
                r2, g2, b2 = img.getpixel((pixel, line))

                formatted_img += '[#{:02x}{:02x}{:02x} on #{:02x}{:02x}{:02x}]▄[/]'.format(r1, g1, b1, r2, g2, b2)
            formatted_img += '\n'
    else:
        # If the request was not successful, return and error message.
        formatted_img = '[red]Cannot be loaded...[/]'

    # return the formatted image.
    return formatted_img


if __name__ == '__main__':
    print('This code is intended to be imported...')
