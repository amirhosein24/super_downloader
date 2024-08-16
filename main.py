

if __name__ == "__main__":

    from telbot.bothandler import updater

    while True:
        try:
            print("dispacher going live...", end=" ")
            updater.start_polling()
            print("done, bot is live.")
            updater.idle()

        except Exception as error:
            print(f"error happend, sleeping for 30 sec,  error: {error}")
            from time import sleep
            sleep(30)
