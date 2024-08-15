
from telbot.bothandler import updater


if __name__ == "__main__":

    while True:
        try:
            print("dispacher going live...", end=" ")
            updater.start_polling()
            print("done, bot is live.")
            updater.idle()

        except Exception as error:
            print(f"error in main if, sleeping for 10 sec,  error: {error}")
            from time import sleep
            sleep(30)
