# Karthik Kribakaran
# Jan 2016
from __future__ import division

import shutil
import wave, struct, sys, getopt
from Tkinter import *
import Tkinter as tk
from tkFileDialog import askopenfilename
import tkMessageBox


def hide(textfile, wavfile, hiddenfile):
    text = open(textfile, 'r')
    contents = text.read()
    contentslength = len(contents)  # number of chars in text file
    if (contentslength == 0):
        print("Empty text file")
        sys.exit()
    sourcewav = wave.open(wavfile, 'r')
    outputwav = wave.open(hiddenfile, 'w')
    outputwav.setparams(sourcewav.getparams())
    framecount = sourcewav.getnframes()  # number of frames in wav file
    if (contentslength > 99999999):
        print("Text file too large")
    if (contentslength > framecount / 2):
        print("Sound file not large enough")
        sys.exit()
    chunklength = framecount // (
                contentslength + 1)  # number of frames per chunk. first frame of chunk contains text data, other chunklength-1 frames contain audio data
    temp = contentslength  # value of first frame in first chunk is length of text file
    sourcewav.readframes(1)
    frame = ''
    for i in range(0, 4):
        if (temp > 0):
            frame += chr(temp % 100)
        else:
            frame += chr(0)
        temp = temp // 100
    outputwav.writeframes(frame)  # writes length of text file
    outputwav.writeframes(sourcewav.readframes(chunklength - 1))  # fills rest of chunk with audio data
    for i in range(0, contentslength):
        y = sourcewav.readframes(1)
        frame = ''
        frame += contents[i]  # reads char from text file and writes to first index of the first frame of the chunk
        for j in range(1, 4):
            frame += y[j]  # fills other indeces with audio data
        outputwav.writeframes(frame)  # writes first frame
        outputwav.writeframes(sourcewav.readframes(chunklength - 1))  # fills rest of chunk with audio data
    outputwav.writeframes(sourcewav.readframes(framecount % contentslength))  # writes remaining audio data
    sourcewav.close()
    outputwav.close()
    text.close()


def extract(hiddenfile, message):
    text = open(message, 'w')
    sourcewav = wave.open(hiddenfile, 'r')
    framecount = sourcewav.getnframes()  # number frames in wav file
    frame = sourcewav.readframes(1)
    contentslength = ord(frame[0]) + 100 * (ord(frame[1])) + 10000 * (ord(frame[2])) + 1000000 * (
        ord(frame[3]))  # grabs text length from first frame of audio
    chunklength = framecount // (contentslength + 1)
    sourcewav.readframes(chunklength - 1)
    for i in range(0, contentslength):
        text.write(sourcewav.readframes(1)[0])  # reads first index of first frame of current chunk, writes to text file
        sourcewav.readframes(chunklength - 1)  # reads past regular audio data
    sourcewav.close()
    text.close()


def main():



    root = Tk()
    root.title("Main Menu")
    root.geometry('400x200')
    root.configure(bg='black')

    def encode():
        enc = Tk()
        enc.title("Menu Encode")
        enc.geometry('400x200')
        enc.configure(bg='black')

        def klikEnc():

            if txAudi.get() == "" or txPs.get() == "":
                tkMessageBox.showinfo('error', 'Harap masukan file')
            else:

                # data_open = open(enc.filename_audio, 'rb')
                # data_audio = data_open.read()
                # data_open.close()
                #
                # data_open = open(enc.filename_tks, 'rb')
                # data_txt = data_open.read()
                # data_open.close()

                shutil.copyfile(enc.filename_tks, 'temp.txt')
                shutil.copyfile(enc.filename_audio, 'temp.wav')

                print(enc.filename_tks, enc.filename_audio, txNm.get())
                hide(enc.filename_tks, enc.filename_audio, txNm.get())
                tkMessageBox.showinfo('gud', 'sukses')

        def klikBr():
            enc.filename_audio = askopenfilename(initialdir="/", title="Select A File",
                                                 filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
            print(enc.filename_audio)
            txAudi.insert(tk.INSERT, enc.filename_audio)
        def klikBrT():
            enc.filename_tks = askopenfilename(initialdir="/", title="Select A File",
                                                 filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            print(enc.filename_tks)
            txPs.insert(tk.INSERT,enc.filename_tks)

        # label audio
        lAudi = Label(enc, text="Input Audio :", font=('Arial', 12), fg='white')
        lAudi.configure(bg='black')
        lAudi.place(x=5, y=3)

        # label pesan
        lPs = Label(enc, text="Input Message :", font=('Arial', 12), fg='white')
        lPs.configure(bg='black')
        lPs.place(x=5, y=35)

        # textfield audio
        txAudi = Entry(enc, width=25)
        txAudi.place(x=130, y=5)

        # textfield audio
        txPs = Entry(enc, width=25)
        txPs.place(x=130, y=38)

        # Button Browse Audio
        btBrw = Button(enc, text="Browse", command=klikBr)
        btBrw.place(x=300, y=3)

        # Button Browse teks
        bttks = Button(enc, text="Browse", command=klikBrT)
        bttks.place(x=300, y=35)

        lNm = Label(enc, text="Input Judul :", font=('Arial', 12), fg='white')
        lNm.configure(bg='black')
        lNm.place(x=5, y=70)

        txNm = Entry(enc, width=25)
        txNm.place(x=130, y=70)

        # Button Encode
        btEn = Button(enc, text="    Encode    ", command=klikEnc)
        btEn.place(x=50, y=100)



    def decode():
        dec = Tk()
        dec.title("Menu Decode")
        dec.geometry('400x180')
        dec.configure(bg='black')

        def klikDec():
            if txAudi2.get() == "":
                tkMessageBox.showinfo('error', 'Harap masukan file')
            else:
                extract(dec.filename_audio, txPs2.get())
                tkMessageBox.showinfo('gud', 'sukses')
        def klikBr2():
            dec.filename_audio = askopenfilename(initialdir="/", title="Select A File",
                                                 filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
            print(dec.filename_audio)
            txAudi2.insert(tk.INSERT, dec.filename_audio)
        # label audio
        lAudi2 = Label(dec, text="Input Audio :", font=('Arial', 12), fg='white')
        lAudi2.configure(bg='black')
        lAudi2.place(x=5, y=3)

        # textfield audio
        txAudi2 = Entry(dec, width=25)
        txAudi2.place(x=130, y=5)

        # Button Browse
        btBrw2 = Button(dec, text="Browse", command=klikBr2)
        btBrw2.place(x=300, y=3)

        # Button Decode
        btDe = Button(dec, text="Decode", command=klikDec)
        btDe.place(x=150, y=70)

        # label pesan
        lPs2 = Label(dec, text="Judul file :", font=('Arial', 12), fg='white')
        lPs2.configure(bg='black')
        lPs2.place(x=5, y=35)

        # textfield pesam
        txPs2 = Entry(dec, width=25)
        txPs2.place(x=130, y=38)

    def note():
        ab = Tk()
        ab.title("Note")
        ab.geometry('300x75')
        ab.configure(bg='black')

        label1 = Label(ab, text = "1. File hanya berbentuk .wav", justify = 'center', fg = 'white')
        label1.configure(bg='black')
        label1.pack()
        label2 = Label(ab, text = "2. Pesan hanya berbentuk .txt", justify = 'center', fg = 'white')
        label2.configure(bg='black')
        label2.pack()
        label3 = Label(ab, text = "3. Semua file hasil tersimpan di folder project", justify = 'center', fg = 'white')
        label3.configure(bg='black')
        label3.pack()


    ljudul = Label(root, text="Steganography Text to Audio", font=('Arial', 20), fg='white')
    ljudul.configure(bg='black')
    ljudul.pack()

    lspasi = Label(root)
    lspasi.configure(bg='black')
    lspasi.pack()

    btnEn = Button(root, text="Encode", command=encode)
    btnEn.pack()
    btnDe = Button(root, text="Decode", command=decode)
    btnDe.pack()
    btnNo = Button(root, text="Note", command=note)
    btnNo.pack()

    lbn = Label(root, text = "By : Arna M Rasyid", fg='white')
    lbn.configure(bg = 'black')
    lbn.pack()
    lbnn = Label(root, text="11180910000089", fg='white')
    lbnn.configure(bg='black')
    lbnn.pack()
    root.resizable(0, 0)

    root.mainloop()


if __name__ == '__main__':
    main()