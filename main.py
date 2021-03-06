#!/usr/bin/python3
import mido
import math
import threading
import time
import random
global midi
midi = [0]*128
for i in range(0, 128):
    midi[i] = (440 / 32) * (math.pow(2, (i-9) / 12))


class Feeper:
    def __thread__(self):
        import RPi.GPIO as gpio
        global midi
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin, gpio.OUT)
        while 1:
            if self.note > -1:
                self.phase = not self.phase
                gpio.output(self.pin, self.phase)
                time.sleep(1/midi[self.note])

    def __init__(self, pin):
        self.pin = pin
        self.note = -1
        self.phase = False
        threading.Thread(target=self.__thread__).start()

    def setnote(self, note):
        self.note = note
free = [Feeper(3)]
busy = []
m = mido.MidiFile("midi.mid")

for i in m.play():
    random.shuffle(free)
    if i.type == "note_on":
        try:
            a = free.pop()
            a.note = i.note
            busy = busy + [a]
        except:
            print("Not enough speakers to play note "+str(i.note))
    elif i.type == "note_off":
        for j in busy:
            if j.note == i.note:
                j.note = -1
                busy.remove(j)
                free = free + [j]
                break
