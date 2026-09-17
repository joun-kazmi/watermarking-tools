import re
import random

from PIL import Image
from time import strftime

from key import load_key, Share


def load_numbers():
    numbers = []
    img = Image.open('number.png')
    for i in range(12):
        num = Image.new('1', (8, 10), 1)  # binary, 8x10, all white
        numbers.append(num)

    for y in range(10):
        for x in range(8):
            for i in range(12):
                r, g, b = img.getpixel((x+8*i, y))
                v = (r+g+b)/3
                if v > 200:
                    v = 1
                else:
                    v = 0
                numbers[i].putpixel((x, y), v)

    return numbers


def xor(x, y):
    if x in [0, 1] and y in [0, 1]:
        return x ^ y
    else:
        return (x + y) % 2


class Timestamp(object):
    NUMBERS_IMG = load_numbers()
    FILENAME = 'timestamp.png'

    @classmethod
    def current(cls):
        t = strftime("%Y-%m-%d %H:%M:%S")
        secret = Image.new("1", (8 * len(t), 10), 1)

        for i in range(len(t)):
            offset = -1
            if re.match(r'[0-9:-]', t[i]):
                try:
                    offset = int(t[i])
                except ValueError as e:
                    if t[i] in ['-', ':']:
                        offset = 10 if t[i] == ':' else 11
                    else:
                        raise e

            if offset < 0:
                continue
            for y in range(10):
                for x in range(8):
                    v = cls.NUMBERS_IMG[offset].getpixel((x, y))
                    secret.putpixel((x+i*8, y), v)

        secret.save(cls.FILENAME)
        return secret


def reconstruction(share, key):
    w, h = share.size
    reconst = Image.new("1", (w, h), 1)
    for y in range(h):
        for x in range(w):
            s = share.getpixel((x, y))
            k = key.getpixel((x, y))
            if k > 127:
                k = 1
            else:
                k = 0
            reconst.putpixel((x, y), xor(s, k))
    reconst.save('reconstructed_timestamp.png')
    return reconst


def load_signature(filename):
    sign = Image.open(filename)
    sign = sign.convert("RGB")
    return sign


class Marker(object):
    FILENAME = 'watermarked.png'
    @classmethod
    def watermark(cls, sign, share):
        w, h = sign.size
        w_s, h_s = share.size
        offset_x, offset_y = (int(w/2 - w_s/2), int(h/2 - h_s/2))
        wtm_sign = Image.new("RGB", (w, h))

        resized_share = Image.new("1", (w, h))
        for y in range(h):
            for x in range(w):
                v = random.randint(0, 1)
                resized_share.putpixel((x, y), v)
        for y in range(h_s):
            for x in range(w_s):
                v = share.getpixel((x, y))
                resized_share.putpixel((x+offset_x, y+offset_y), v)

        for y in range(h):
            for x in range(w):
                r, g, b = sign.getpixel((x, y))
                if b % 2 == 1:
                    b -= 1
                b += resized_share.getpixel((x, y))
                wtm_sign.putpixel((x, y), (r, g, b))
        wtm_sign.save(cls.FILENAME)
        return wtm_sign


def main():
    # Generate Timestamp & (2, 2) Scheme using XOR
    key = load_key()
    secret = Timestamp.current()
    share = Share.make(secret, key)
    reconst = reconstruction(share, key)

    # Watermarking
    sign = load_signature('kaist.gif')
    wtm_sign = Marker.watermark(sign, share)

if __name__ == '__main__':
    main()
