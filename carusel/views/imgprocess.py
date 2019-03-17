import os
from os import path
import uuid
import PIL
from PIL import Image


def get_resized_img(fullsized, baseheight=300):
    """Creates resized image in subfolder 'resized'

    Absolute file path must be passed
    """

    target_dir = path.join(path.dirname(fullsized), 'resized')
    file_name = path.basename(fullsized)
    target_file_name = path.join(target_dir, file_name)
    if path.isfile(target_file_name):
        return dict(
            result_file=target_file_name,
            status='exist'
        )
    if not path.isdir(target_dir):
        try:
            os.mkdir(target_dir)
        except OSError:
            print("Creation of the directory %s failed" % target_dir)
    # Image processing
    img = Image.open(fullsized)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save(target_file_name)
    return dict(
        result_file=target_file_name,
        status='created'
    )


def get_unique_file_name(file_name):
    extension = os.path.splitext(file_name)[1]
    unque_name = uuid.uuid4().hex
    return unque_name + extension
