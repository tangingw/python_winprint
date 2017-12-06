import os
import json
import time
import threading
from flask import Flask, request
from werkzeug.utils import secure_filename
from redis import StrictRedis
from print_lib import print_file


REDIS_CONNECTION = StrictRedis(host=json.loads(open("config/config.json", "r").read())["REDIS_SERVER"])
UPLOAD_FOLDER = json.loads(open("config/config.json", "r").read())["SERVER"]["PRINT_PATH"]
ALLOWED_EXTENSIONS = set(["jpg", "txt", "pdf", "xls", "xlsx", "doc", "docx"])


APP = Flask(__name__)
APP.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def print_engine(redis_conn):

    while True:

        print_file(redis_conn)
        time.sleep(5)


def allowed_file(filename):

    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_error(error_msg):

    return json.dumps({"Status": "Error", "Error_Msg": error_msg})


@APP.route('/')
def front_page():

    return "HELLO WORLD!"


@APP.route("/upload", methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:

            return gen_error("No File part")

        file = request.files['file']

        if file.filename == '':

            return gen_error("No selected file")

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(APP.config["UPLOAD_FOLDER"], filename))

            return json.dumps(
                {
                    "Status": "Success", "File_Uploaded": filename,
                    "Job_status": "Sent for printing"
                }
            )

    return gen_error("Invalid Action")


def main():

    print_thread = threading.Thread(target=print_engine, args=(REDIS_CONNECTION,))
    print_thread.setDaemon(True)
    print_thread.start()
    APP.run(host='0.0.0.0', debug=True, threaded=True)


if __name__ == '__main__':

    main()
