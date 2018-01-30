# -*- coding: utf-8 -*-

from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image


def _add_thumb(s):
    """
    Modifies a string (filename, URL) containing an image filename, to insert
    '.thumb'
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        # print('self.path=', _add_thumb(self.path))
        return _add_thumb(self.path)

    thumb_path = property(_get_thumb_path)


    def _get_thumb_url(self):
        return _add_thumb(self.url)

    thumb_url = property(_get_thumb_url)

    @staticmethod
    def _scale_dimensions(width, height, longest_side=800):
        if width > height:
            koeficent = float(width) / float(longest_side)
            width = longest_side
            height = int(height / koeficent)
            return width, height
        elif width < height:
            koeficent = float(height) / float(longest_side)
            height = longest_side
            width = int(width / koeficent)
            return width, height
        else:
            return longest_side, longest_side

    def save(self, name, content, save=True):
        from datetime import datetime
        dt = str(datetime.now()).replace('-', '_').replace(':', '').replace(' ', '_')
        img_name = 'img_' + dt.split('.')[0] + '.jpg'
        super(ThumbnailImageFieldFile, self).save(img_name, content, save)
        img = Image.open(self.path)
        (width, height) = img.size
        if width > 800 or height > 800:
            (width, height) = self._scale_dimensions(width, height)
        newImg = img.resize((width, height), Image.ANTIALIAS)
        newImg.save(self.path, 'JPEG')
        img.thumbnail(
            (self.field.thumb_width, self.field.thumb_height),
            Image.ANTIALIAS
        )
        img.save(self.thumb_path, 'JPEG')

        # def delete(self, save=True):
        #     print('self.thumb_path', self.thumb_path)
        #     if os.path.exists(self.thumb_path):
        #         os.remove(self.thumb_path)
        #     super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    """
    Behaves like a regular ImageField, but stores an extra (JPEG) thumbnail
    image, providing FIELD.thumb_url and FIELD.thumb_path.

    Accepts two additional, optional arguments: thumb_width and thumb_height,
    both defaulting to 200 (pixels). Resizing will preserve aspect ratio while
    staying inside the requested dimensions; see PIL's Image.thumbnail()
    method documentation for details.
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=200, thumb_height=200, *args, **kwargs):
        # self.img_name = img_name
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

        super(ThumbnailImageField, self).__init__(*args, **kwargs)

        # def delete(self, save=True):
        #     print('self.thumb_path', self.thumb_path)
        #     if os.path.exists(self.thumb_path):
        #         os.remove(self.thumb_path)
        #     super(ThumbnailImageField, self).delete(save)
