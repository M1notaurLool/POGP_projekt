import game
import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

if __name__ == "__main__":
    g = game.Game(int(screen_width),int(screen_height))
    g.run()