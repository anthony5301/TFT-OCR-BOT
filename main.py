"""
Where the bot execution starts & contains the game loop that keeps the bot running indefinitely
"""
import ctypes
import sys
import multiprocessing
from ui import UI
import auto_queue
from game import Game
import settings


def game_loop(ui_queue: multiprocessing.Queue) -> None:
    """Keeps the program running indefinetly by calling queue and game start in a loop"""
    while True:
        auto_queue.queue()
        Game(ui_queue)

def is_admin():
    """Check if bot is running as admin to prevent bot can't move in-game"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except: # pylint: disable=bare-except
        return False

if __name__ == "__main__":
    if settings.LEAGUE_CLIENT_PATH is None:
        raise ValueError("No league client path specified. Please set the path in settings.py")
    if is_admin():
        message_queue = multiprocessing.Queue()
        overlay: UI = UI(message_queue)
        game_thread = multiprocessing.Process(target=game_loop, args=(message_queue,))

        print("TFT OCR | https://github.com/jfd02/TFT-OCR-BOT")
        print("Close this window to terminate the overlay window & program")
        game_thread.start()
        overlay.ui_loop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
