import random
import string


def get_random_string(length: int = 64) -> str:
    '''Create random string based on given length.'''
    sys_random = random.SystemRandom()
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join([sys_random.choice(letters) for _ in range(length)])
