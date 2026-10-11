from tkinter import *
import random
import time

class Game:
  def _init_(self):
    self.tk
    self.tk.title("Title pending")
    self.tk.resizable(0,0)
    self.tk.wm_attributes("-topmost", 1)
    self.canvas = Canvas(self.tk, width = 500, height = 500, \ highlightthickness = 0)
