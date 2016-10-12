from random import randint
from time import sleep

def events(max_delay, limit):
    while True:
        delay = randint(1, max_delay)
        if delay >= limit:
            sleep(limit)
            yield None
        else:
            sleep(delay)
            yield 'Event generated, awaiting %d s' % delay