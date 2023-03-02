import random
import string


def name_gen():
    symbols = string.ascii_uppercase + string.digits
    rand_name = ''.join(random.sample(symbols, 8))
    return rand_name
