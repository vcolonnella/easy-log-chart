from datetime import date


class Event:
    name = ""
    channel = ""
    start = date(1970, 1, 1)
    end = date(1970, 1, 1)

    def __init__(self, name, channel, start):
        self.name = name
        self.channel = channel
        self.start = start