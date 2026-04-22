import tkinter as tk
from screens.menu import MenuScreen

ventana = tk.Tk()
ventana.title("Hackermate")
ventana.geometry("900x650")

canvas = tk.Canvas(ventana)
canvas.pack(fill="both", expand=True)

MenuScreen(canvas)

ventana.mainloop()