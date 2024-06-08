import tkinter

from tkinter import filedialog
from tkinter import colorchooser
from tkinter import simpledialog

m = tkinter.Tk()


def get_value(title, prompt, initial_value):
    m = tkinter.Tk()
    value = simpledialog.askinteger(title, prompt, initialvalue=initial_value)
    m.destroy()
    if value is not None:
        return value
    return initial_value


def get_file():
    m = tkinter.Tk()
    filename = filedialog.askopenfilename(
        filetypes=(
            ("JPG files", "*.jpg"),
            ("Text files", "*.txt"),
            ("Python Files", ("*.py", "*.pyx")),
            ("All Files", "*.*")
        )
    )
    m.destroy()

    return filename


def save_file(title="Zapisz jako...", filetypes=[("BMP files", "*.bmp")], defaultextension=".bmp", confirmoverwrite=False, initialfile="screenshot.bmp"):
    m = tkinter.Tk()
    filename = filedialog.asksaveasfilename(
        filetypes=filetypes,
        defaultextension=defaultextension,
        confirmoverwrite=confirmoverwrite,
        initialfile=initialfile,
        title=title

    )
    m.destroy()
    return filename


def read_file(title="Wczytaj plik", filetypes=[("BMP files", "*.bmp")], defaultextension=".bmp", initialfile="screenshot.bmp"):
    m = tkinter.Tk()
    filename = filedialog.askopenfilenames(
        filetypes=filetypes,
        defaultextension=defaultextension,
        initialfile=initialfile,
        title=title
    )
    m.destroy()
    print(filename)
    if filename != () and filename is not None:
        if type(filename) is tuple:
            # bodge
            if filename[0] is not None:
                return filename[0]
        else:
            if filename is not None:
                return filename
    return initialfile


def get_name(filename):

    filename_list = list(filename)
    new_list = []

    while len(filename_list):
        character = filename_list.pop()
        if character != "/" and character != "\\":
            new_list.append(character)
        else:
            break

    new_list.reverse()
    return ''.join(new_list)


def get_colour(previous_colour):
    m = tkinter.Tk()
    colour_code = colorchooser.askcolor(title="Choose color", color=previous_colour)
    m.destroy()
    if bool(colour_code[0]):
        return colour_code[0]

    return previous_colour


def get_string(title, prompt, initial_value):
    m = tkinter.Tk()
    value = simpledialog.askstring(title, prompt, initialvalue=initial_value)
    m.destroy()
    if value is not None:
        return value
    return initial_value


m.destroy()