import random
import os.path
from pygame import mixer
from tkinter import *
import requests
from bs4 import BeautifulSoup as Bs

mixer.init()
global i  # noinspection PyRedeclaration
i = 0

path = "..\\..\\Music"
music = os.listdir(path)
# print(music, path)
mixer.music.load(path + "\\" + music[0])

player = Tk()
player.configure()
player.title("MP3")
player.geometry("1000x500")


def on_press():  # play_button
    global i
    selected = music_list.curselection()

    if not selected:  # if no music has been selected from the listbox, load and play the current one
        mixer.music.load(path + "\\" + music[i])
        mixer.music.play()
    elif selected:  # else if music has been selected play the selected one
        i = selected[0]
        mixer.music.load(path + "\\" + music[i])
        mixer.music.play()


def next_song():  # next_button
    global i
    mixer.music.stop()
    i += 1 if i != len(music) - 1 else 0  # checking so it doesnt exceed the list range
    mixer.music.load(path + "\\" + music[i])
    mixer.music.play()


def previous_song():  # previous_button
    global i
    mixer.music.stop()
    i -= 1
    mixer.music.load(path + "\\" + music[i])
    mixer.music.play()


def shuffle():  # shuffle_button TODO make it as it is on-off button
    mixer.music.stop()
    random.shuffle(music)
    mixer.music.load(path + "\\" + music[0])
    mixer.music.play()


def pause():
    mixer.music.pause()


def search_song():
    if search_entry.get() == "":
        pass


def lift_lyrics_frame():  # new lyric frame

    page = music[i].replace(".mp3", "") + " lyrics"  # get the page using the music folder
    page = page.replace(' ', '+')  # replace " " with +  to make it easier for the browser
    url = f"https://google.com/search?q={page}"  # fill the complete url
    resp = requests.get(url)  # politely ask google for permission to get what you need
    if resp.status_code == 200:  # if what you searched "exists"
        soup = Bs(resp.content, "html.parser")
        try:
            lyrics_l = soup.find_all('div', class_="ZINbbc xpd O9g5cc uUPGi")  #  class of google lyrics
            lyrics = lyrics_l[0].get_text()
            if "Πηγή" in lyrics:  # get rid of the source and the singers may need to make it for all languages
                lyrics = lyrics.replace(lyrics[lyrics.index("Πηγή")::], "")
        except:
            print("Sorry run into a problem")
    else:
        lyrics = "Sorry could not find lyrics for this song"

    lyrics_frame = Frame(player, bg="darkblue")
    lyrics_frame.place(x=0, y=0, width=1000, height=500)
    lyrics_text = Text(lyrics_frame)
    lyrics_text.insert(INSERT, lyrics)
    # lyrics_text.config(state=DISABLED)
    lyrics_text.place(x=200, y=75, width=600, height=350)


main_frame = Frame(player, bg="white")
second_frame = Frame(player, bg="darkblue")
main_frame.place(x=0, y=400, width=1000, height=100)
second_frame.place(x=0, y=0, width=1000, height=400)

search = StringVar()

play_button = Button(main_frame, text="Play", command=lambda: on_press())
pause_button = Button(main_frame, text="Pause", command=lambda: pause())
next_button = Button(main_frame, text="Next", command=lambda: next_song())
previous_button = Button(main_frame, text="Previous", command=lambda: previous_song())
shuffle_button = Button(main_frame, text="Shuffle", command=lambda: shuffle())
search_entry = Entry(second_frame, text="Search for a song", textvariable=search)
search_button = Button(second_frame, command=lambda: search_song())
lyrics_button = Button(main_frame, text="lyrics", command=lambda: lift_lyrics_frame())

play_button.place(x=334, y=20, width=166, height=80)
pause_button.place(x=500, y=20, width=166, height=80)
next_button.place(x=666, y=20, width=333, height=80)
previous_button.place(x=0, y=20, width=333, height=80)
shuffle_button.place(x=500, y=0, width=166, height=20)
search_entry.place(x=325, y=10, width=350, height=30)
search_button.place(x=677, y=10, width=10, height=30)
lyrics_button.place(x=334, y=0, width=166, height=20)

music_list = Listbox(second_frame, bg="lightslategray", fg="white", bd=5, relief=SUNKEN, highlightthickness=10,
                     highlightcolor="lightslategray")
music_list.place(x=250, y=50, width=500, height=300)  # placing the listbox

for j in range(len(music)):  # Filling the listbox based on the music folder
    music_list.insert(j, re.sub(".mp3", "", music[j]))

if __name__ == '__main__':
    player.mainloop()
