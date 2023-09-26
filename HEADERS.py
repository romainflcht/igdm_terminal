# If you get any weird request error, try to modify the user agent of the main_header. 
# If you can't send messages anymore, the BROADCAST_HEADER need to be modified with another device.


# Header for every fetch requests such as fetch inbox data, thread content...
MAIN_HEADERS = {
    'authority': 'www.instagram.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
    'x-ig-app-id': '936619743392459',
}

# Header used to send message, otherwise, we get a '403 Unauthorized' request status code. 
BROADCAST_HEADERS = {
    'authority': 'www.instagram.com',
    'User-Agent': 'Instagram 117.0.0.28.123 Android (28/9.0; 420dpi; 1080x1920; OnePlus; ONEPLUS A3003; OnePlus3;qcom; en_US; 180322800)',
    'x-ig-app-id': '936619743392459',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
}

if __name__ == '__main__': 
    print('This code is intended to be imported...')
