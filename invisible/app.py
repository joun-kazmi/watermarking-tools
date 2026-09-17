from Tkinter import Tk, Frame, Button, Label
from tkFileDialog import askopenfilename

from PIL import Image
from PIL.ImageTk import PhotoImage

from key import Key, Share
from watermarking import Timestamp, Marker
from auth import auth


class _Label(Frame):
    def __init__(self, master=None, width=0, height=0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.label = Label(self, **kwargs)
        self.label.pack(expand=True, fill='both')
        self.label.saved_image = None

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

    @property
    def image(self):
        return self.label.saved_image

    def set_img(self, img):
        # img = Image.open(filename)
        width = self.width if img.width > self.width else img.width
        height = self.height if img.height > self.height else img.height

        if width == self.width or height == self.height:
            print 'resized'
            self_ratio = 1.0 * self.width / self.height
            img_ratio = 1.0 * img.width / img.height

            height = self.height if self_ratio > img_ratio else img.height
            width = self.height * img_ratio

            resized = img.resize((int(width), int(height)), Image.ANTIALIAS)
        else:
            resized = img

        resized = PhotoImage(resized)
        self.label.configure(image=resized)
        self.label.image = resized
        self.label.saved_image = img


class App(Frame):
    def insert_image(self, panel, filename=None, image=None):
        if filename is None and image is None:
            raise TypeError('insert_image takes filename or image')
        if filename is not None:
            panel.set_img(Image.open(filename))
        elif image is not None:
            panel.set_img(image)
        else:
            raise TypeError

    def key(self):
        Key.generate_key()
        self.insert_image(self._key_img, filename=Key.FILENAME)

    def timestamp(self):
        Timestamp.current()
        self.insert_image(self._ts_img, filename=Timestamp.FILENAME)

    def share(self):
        if (self._ts_img.image is not None and
            self._key_img.image is not None):
            share = Share.make(
                self._ts_img.image,
                self._key_img.image
            )
            self.insert_image(self._share_img, filename=Share.FILENAME)
            # self.insert_image(self._share_img, image=share)
            self._share = share
        else:
            raise ValueError('share can be made from key and timestamp')

    def input_img(self):
        filename = askopenfilename()
        if filename:
            self.insert_image(self._input_img, filename)

    def watermark(self):
        if (self._share_img.image is not None and
            self._input_img.image is not None):
            rgb_image = self._input_img.image.convert('RGB')
            wm = Marker.watermark(
                rgb_image,
                self._share
            )
            self.insert_image(self._watermark_img, filename=Marker.FILENAME)
        else:
            raise ValueError('share can be made from share and input image')

    def verify(self):
        if (self._key_img.image is not None and
            self._watermark_img.image is not None):
            wm = auth(
                self._watermark_img.image,
                self._key_img.image
            )
            self.insert_image(self._verify_img, filename='watermark.png')
        else:
            raise ValueError('share can be made from share and input image')

    def create_widgets(self):
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)
        self.columnconfigure(5, pad=3)
        self.columnconfigure(6, pad=3)

        self.rowconfigure(0, pad=50)
        self.rowconfigure(1, pad=50)
        self.rowconfigure(2, pad=50)
        self.rowconfigure(3, pad=50)

        self._key = Button(self, text='key', command=self.key)
        self._key.pack(side='left')
        self._key.grid(row=0, column=0)

        self._key_img = _Label(master=self, width=170, height=30)
        self._key_img.pack(side='right', fill='both', expand='no')
        self._key_img.grid(row=0, column=1)

        self._ts = Button(self, text='timestamp', command=self.timestamp)
        self._ts.pack(side='left')
        self._ts.grid(row=0, column=2)

        self._ts_img = _Label(master=self, width=170, height=30)
        self._ts_img.pack(side='right', fill='both', expand='no')
        self._ts_img.grid(row=0, column=3)

        self._share = Button(self, text='share', command=self.share)
        self._share.pack(side='left')
        self._share.grid(row=0, column=4)

        self._share_img = _Label(master=self, width=170, height=30)
        self._share_img.pack(side='right', fill='both', expand='no')
        self._share_img.grid(row=0, column=5)

        self._input = Button(self, text='image', command=self.input_img)
        self._input.pack(side='bottom')
        self._input.grid(row=1, column=0)

        self._input_img = _Label(master=self, width=770, height=196)
        self._input_img.pack(side='right', fill='both', expand='no')
        self._input_img.grid(row=1, column=1, columnspan=5)

        self._watermark = Button(self,
                                 text='watermark', command=self.watermark)
        self._watermark.pack(side='bottom')
        self._watermark.grid(row=2, column=0)

        self._watermark_img = _Label(master=self, width=770, height=196)
        self._watermark_img.pack(side='right', fill='both', expand='no')
        self._watermark_img.grid(row=2, column=1, columnspan=5)

        self._verify = Button(self, text='verify', command=self.verify)
        self._verify.pack(side='bottom')
        self._verify.grid(row=3, column=0)

        self._verify_img = _Label(master=self, width=770, height=196)
        self._verify_img.pack(side='right', fill='both', expand='no')
        self._verify_img.grid(row=3, column=1, columnspan=5)

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.pack()
        self.create_widgets()


if __name__ == '__main__':
    root = Tk()
    root.title('Watermark')
    root.minsize(950, 950)
    app = App(master=root, width=900, height=750)
    root.mainloop()

closeInput = raw_input("Press ENTER to exit")
print "Closing..."	
