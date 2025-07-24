import logging

class NoSocketIOFilter(logging.Filter):
    """
    Filter to omit logs of polling from Socket.IO.
    """
    def filter(self, record):
        list_filter_msg = ['POST /socket.io', 'GET /socket.io/']
        message = record.getMessage()
        for msg in list_filter_msg:
            for msg in list_filter_msg:
                if msg in message and '" 200' in message:
                    return False

        return True
