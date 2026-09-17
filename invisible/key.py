from PIL import Image
import random


def xor(x, y):
    if x in [0, 1] and y in [0, 1]:
        return x ^ y
    else:
        return (x + y) % 2


class Key(object):
    FILENAME = 'key.png'

    @classmethod
    def generate_key(cls):
        key_img = Image.new('1', (152, 10), 1)
        for y in range(10):
            for x in range(152):
                v = random.randint(0, 1)
                key_img.putpixel((x, y), v)

        key_img.save(cls.FILENAME)
        return key_img


class Share(object):
    FILENAME = 'share.png'

    @classmethod
    def make(cls, secret, key):
        w, h = secret.size
        share = Image.new("1", (w, h), 1)
        for y in range(h):
            for x in range(w):
                s = secret.getpixel((x, y))
                k = key.getpixel((x, y))
                if k > 127:
                    k = 1
                else:
                    k = 0
                share.putpixel((x, y), xor(s, k))
        share.save(cls.FILENAME)
        return share


def load_key():
    try:
        key = Image.open(Key.FILENAME)
    except IOError:
        key = Key.generate_key()
    return key


if __name__ == '__main__':
    Key.generate_key()
