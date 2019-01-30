import threading
from datetime import datetime
from tkinter import Tk, Label, Button, BOTTOM, Text, DISABLED
from tkinter.ttk import Combobox

from main_package.configurations import TIME_FRAME_DICT, TIMEFRAME_LABLE_TEXT, TERM_TEXT
from twitter_api_handler.twiter_api_handler import TwitterAPIHandler


def run_analyzing():
    """
    The thread method, starts the streaming
    """

    api_handler.stream_term(term_text.get("1.0", 'end-1c').split(','), TIME_FRAME_DICT[combo.get()])


def start_analyzing():
    """
    This method starts the analyzing thread
    """

    analyze_thread = threading.Thread(target=run_analyzing)
    analyze_thread.start()
    start_btn.config(state=DISABLED)


if __name__ == "__main__":
    print(datetime.now())
    root = Tk()
    combo = Combobox(root, state="readonly", values=list(TIME_FRAME_DICT.keys()))
    label = Label(root, text=TIMEFRAME_LABLE_TEXT)
    label.pack()
    combo.pack()
    combo.current(0)
    label2 = Label(root, text=TERM_TEXT)
    label2.pack()
    term_text = Text(root, height=1, width=20)
    term_text.pack()
    start_btn = Button(root, text='Start', width=10, command=start_analyzing)
    start_btn.pack(side=BOTTOM)
    root.geometry("300x150")

    # connect to twitter api
    api_handler = TwitterAPIHandler()
    api_handler.authenticate()

    root.mainloop()
