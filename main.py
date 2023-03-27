from inbox import Inbox
import requests_data.req

if __name__ == '__main__':
    inbox = Inbox(requests_data.req.COOKIES_r, requests_data.req.HEADERS)
    inbox.update_indox(10)
    inbox.show()

    conversation_id = int(input('conversation > ')) - 1

    inbox._threads[conversation_id].update_thread(15)
    for item in inbox._threads[conversation_id]._items:
        item.show()
