import time
import json
import win32api
import win32print
from print_log import Logger


PRINT_PATH = json.loads(open("config/config.json", "r").read())["SERVER"]["PRINT_PATH"]


def print_file(redis_conn):

    """
    This function fetches file queue from redis server and
    print the file using win32 print API

    Args:

        redis_conn(redis.Redis)

    Returns:
        void

    Example:

       redis_connection = StrictRedis()
       print_file(redis_connection)

    """
    win_logger = Logger.win_logger()
    logger = win_logger.genLogger("win_print")

    if redis_conn.ping():

        filename_list = list(redis_conn.smembers("File_Queue"))

        while len(filename_list) != 0:

            file_name = ""
            received_time = int(time.time())
            filename = filename_list[0].decode('utf-8')

            printed_file = [i.decode('utf-8') for i in list(redis_conn.smembers("Printed_File"))]

            if filename in printed_file:

                file_name = filename[:-4] + "_" + str(received_time) + "_" + filename[-4:]

            else:

                file_name = filename

            if not redis_conn.hgetall(file_name):

                redis_conn.hmset(
                    file_name,
                    {
                        "filename": filename,
                        "queue_name": file_name,
                        "received_time": received_time,
                        "printed_status": "NO"
                    }
                )

            logger.info("Currently Printing %s" % file_name)

            win32api.ShellExecute(
                0,
                "print",
                PRINT_PATH + filename,
                win32print.GetDefaultPrinter(),
                ".",
                0
            )

            redis_conn.sadd("Printed_File", file_name)
            redis_conn.hset(file_name, "printed_status", "YES")
            redis_conn.srem("File_Queue", filename)

            filename_list = list(redis_conn.smembers("File_Queue"))

    else:

        #print("Queue Server cannot be located")
        logger.error("Queue Server cannot be located!")
