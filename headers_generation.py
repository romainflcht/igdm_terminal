import random
import time
from DEVICES import DEVICES

# Header from @bruvv in the 'igbot' GitHub repo. 
BASE_HEADERS = {
    'X-IG-App-Locale': 'fr_FR',
    'X-IG-Device-Locale': 'fr_FR',
    'X-IG-Mapped-Locale': 'fr_FR',
    'X-Pigeon-Rawclienttime': str(round(time.time() * 1000)),
    'X-IG-Connection-Speed': '-1kbps',
    'X-IG-Bandwidth-Speed-KBPS': str(random.randint(7000, 10000)),
    'X-IG-Bandwidth-TotalBytes-B': str(random.randint(500000, 900000)),
    'X-IG-Bandwidth-TotalTime-MS': str(random.randint(50, 150)),
    'X-IG-App-Startup-Country': 'FR',
    'X-Bloks-Is-Layout-RTL': 'false',
    'X-Bloks-Enable-RenderCore': 'false',
    'X-IG-Connection-Type': 'WIFI',
    'X-IG-Capabilities': '3brTvwM=',
    'X-FB-HTTP-Engine': 'Liger',
    'X-IG-Prefetch-Request': 'foreground',
    'X-IG-APP-IP': '936619743392459',
    'Accept-Language': 'fr-FR',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'close',
    'authority': 'www.instagram.com',
    'User-Agent': '',
}


def generate_request_header() -> dict:
    """
    Function that generate a request header based on a random selected android device. 
    :return: The request header. 
    """

    # Get a random device, get every info needed and format it. 
    device = DEVICES.get(random.choice(list(DEVICES.keys())))
    device_info = list(device.values())

    # Create the user-agent based on the selected device. 
    user_agent = 'Instagram {0} Android ({1}/{2}; {3}; {4}; {5}; {6}; {7}; {8}; en_US; {9})'.format(*device_info)
    BASE_HEADERS['User-Agent'] = user_agent

    # return the generated header.  
    return BASE_HEADERS


if __name__ == '__main__':
    print('This code is intended to be imported...')
