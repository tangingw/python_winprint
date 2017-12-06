import os
import sys
import time
import json
import requests
from redis import StrictRedis
from pdf_gen import print_pdf
from print_log import Logger


PRINT_PATH = json.loads(open("config/config.json", "r").read())["CLIENT"]["PRINT_PATH"]


def send_print_job(redis_connection, filename):

    client_logger = Logger.client_logger()
    logger = client_logger.genLogger("print_client")

    URL = json.loads(open("config/config.json", "r").read())["UPLOAD_URL"]

    file_object = {"file": open(PRINT_PATH + filename, 'rb')}
    req = requests.post(URL, files=file_object)

    if req.status_code == 200:

        if req.json()["Status"] == "Success":

            #print "Send File %s for printing" % filename
            logger.info("Send File %s for printing" % filename)
            redis_connection.sadd("File_Queue", filename)

        elif req.json()["Status"] == "Error":

            #print "Upload Failed: %s" % req.json()["Error_Msg"]
            logger.error("Upload Failed: %s" % req.json()["Error_Msg"])
    else:

        #print "Error from Webserver!"
        #print req.text
        logger.error("Error from Webserver!")
        logger.error(req.text)


def main():

    """
    This is the main logic for sending printing to queue server:

    Example:

        $ python print_client.py <FILE_NAME> <PAGE_RANGE>

    Parameters:

        required:
            <FILE_NAME> : file_name for the file to be printed

        optional:
            <PAGE_RANGE>: The format is as such:
            x-x: Single page of page x
            x-y: Pages range from page x to page y

    """

    redis_connection = StrictRedis(host=json.loads(open("config/config.json", "r").read())["REDIS_SERVER"])

    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print "Invalid parameters!"
        print "Format: python print_client.py <FILENAME> <PAGE_RANGE>"
        exit(1)

    else:

        file_name = os.path.basename(sys.argv[1])

        if file_name.split(".")[-1] != "pdf":

            print "Not a PDF file!"
            exit(1)

        if len(sys.argv) == 3:

            page_range = sys.argv[2]

            new_filename = PRINT_PATH + file_name[:-4] + "_temp.pdf"
            print_pdf(sys.argv[1], new_filename, page_range)
            file_name = os.path.basename(new_filename)

        elif len(sys.argv) == 2:

            if not os.path.exists(PRINT_PATH + file_name) and os.path.isfile(sys.argv[1]):

                os.system("cp " + os.path.abspath(sys.argv[1]) + " " + PRINT_PATH)
                time.sleep(5)

        send_print_job(redis_connection, file_name)


if __name__ == "__main__":

    main()
