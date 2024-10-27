from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
    random_pair = random.choice(to_learn)
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global random_pair, flip_timer, to_learn
    window.after_cancel(flip_timer)
    random_pair = random.choice(to_learn)
    random_french_word = random_pair["French"]
    canvas.itemconfig(word, text=random_french_word, font=("Arial", 60, "bold"), fill="Black")
    canvas.itemconfig(title, text="French", font=("Arial", 40, "italic"), fill="Black")
    canvas.itemconfig(front, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    global random_pair
    random_english_word = random_pair["English"]
    canvas.itemconfig(word, text=random_english_word, font=("Arial", 60, "bold"), fill="white")
    canvas.itemconfig(title, text="English", font=("Arial", 40, "italic"), fill="white")
    canvas.itemconfig(front, image=card_back_img)

def learnt():
    global random_pair, to_learn
    to_learn.remove(random_pair)
    data2 = pandas.DataFrame(to_learn)
    data2.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
front = canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_label = PhotoImage(file="images/right.png")
right_button = Button(image=right_label, highlightthickness=0, command=learnt)
right_button.grid(column=1, row=2)

wrong_label = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_label, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=2)

next_card()

window.mainloop()
