import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

from .e621 import E621
from .config import Config
from tkinter import Spinbox
import webbrowser

def download_pools():
    config_file_path = Path(config_entry.get())
    pool_ids = [int(id) for id in pool_entry.get().split()]
    num_threads = int(threads_entry.get())

    config = Config(config_file_path)
    e621 = E621(config)

    for pool_id in pool_ids:
        pool = e621.get_pool(pool_id)
        pool.download(num_threads)

    messagebox.showinfo('Download Complete', 'All pools have been downloaded.')

root = tk.Tk()

config_label = tk.Label(root, text='Config File Path')
config_label.pack()
config_entry = tk.Entry(root)
config_entry.insert(0, 'config.yaml')
config_entry.pack()

def browse_config_file():
    file_path = filedialog.askopenfilename(filetypes=[('YAML Files', '*.yaml')])
    if file_path:
        config_entry.delete(0, tk.END)
        config_entry.insert(0, file_path)

browse_button = tk.Button(root, text='Browse', command=browse_config_file)
browse_button.pack()

pool_label = tk.Label(root, text='Pool IDs (separated by spaces)')
pool_label.pack()
pool_entry = tk.Entry(root)
pool_entry.insert(0, '933')
pool_entry.pack()

link_label = tk.Label(root, text='Click here to view available pools')
link_label.pack()

def open_pools_link():
    webbrowser.open('https://e621.net/pools/gallery')

link_label.bind('<Button-1>', lambda e: open_pools_link())

threads_label = tk.Label(root, text='Number of Threads')
threads_label.pack()
threads_entry = Spinbox(root, from_=1, to=10)
threads_entry.insert(0, '3')
threads_entry.delete(1)
threads_entry.pack()

download_button = tk.Button(root, text='Download Pools', command=download_pools)
download_button.pack()

def main():
	root.mainloop()
