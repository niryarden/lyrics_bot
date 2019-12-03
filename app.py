import sys
from bot import main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        chat_id = sys.argv[1]
        main(chat_id)
    else:
        print("please supply chat id")
