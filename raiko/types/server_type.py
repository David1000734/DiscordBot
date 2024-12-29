from raiko.types.reddit_type import Reddit as rd
from raiko.types.music_type import Music as ms
from typing import Optional


class Server(object):
    __name = None
    __guild_id = 0

    def __init__(self):
        self.Reddit: Optional[rd] = None
        self.Music: Optional[ms] = None

        pass

    pass
