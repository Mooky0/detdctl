from stream import *
from cli import CLI


def init():
    stream_collection = StreamCollection()



if "__main__" == __name__:
    init()
    cli = CLI()
    cli.run_forever()