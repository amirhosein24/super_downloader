
from telbot.bothandler import go_live
from time import sleep

if __name__ == "__main__":
    while True:

        try:
            go_live()

        except Exception as error:
            print(f"error in main if, sleeping for 10 sec,  error: {error}")
            sleep(10)
