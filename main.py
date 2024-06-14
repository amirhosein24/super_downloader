
from telbot.bothandler import go_live


if __name__ == "__main__":
    while True:

        try:
            go_live()
        except Exception as error:
            print(f"error in main if, error: {error}")
