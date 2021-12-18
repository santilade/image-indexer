import threading
import os
import os.path
import hashlib
import datetime

from flask import Blueprint, jsonify, render_template
from PIL import Image
from flask_cors import cross_origin
from unsync import unsync

image_indexer = Blueprint('image_indexer', __name__)


@unsync
def process_file(f, imgs_path, valid_formats):
    file_name = os.path.splitext(f)
    file_path = os.path.join(imgs_path, f)
    title, ext = file_name[0], file_name[1]

    print(threading.current_thread().name + " -> " + f)

    if ext.lower() in valid_formats:
        img = Image.open(file_path)
        md5hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        response = {"title": title, "size": img.size, "format": ext, "md5sum": md5hash, "src": file_path}
        return response


@image_indexer.route('/imgs', methods=['GET'])
def run_image_indexer():
    t0 = datetime.datetime.now()
    print(threading.current_thread().name)

    # imgs_path = request.json['imgs_path']
    # valid_formats = request.json['valid_formats']
    imgs_path = "C:/Users/Santiago/Pictures/Wallpapers"
    valid_formats = [".jpg", ".gif", ".png", ".tga"]

    tasks = []
    for f in os.listdir(imgs_path):
        tasks.append(process_file(f, imgs_path, valid_formats))

    results = []
    for t in tasks:
        results.append(t.result())

    dt = datetime.datetime.now() - t0
    print("Done in {:,.2f} seconds.".format(dt.total_seconds()))
    return render_template("index.html", imgs_path=imgs_path, results=results)
