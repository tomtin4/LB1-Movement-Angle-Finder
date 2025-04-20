import dolphin_memory_engine as dolphin
import math
from tkinter import *

window = Tk()
window.title("Dolphin Line Calculator")


unhooked = Frame(window)
Label(unhooked, text="Please run dolphin emulator...").grid(row=0, column=0, sticky=W, padx=10)


info = Frame(window)

Label(info, text="Player 1").grid(row=0, column=0, sticky=W, padx=10)

Label(info, text="Position:").grid(row=1, column=0, sticky=W, padx=10)

player1PosLabel = Label(info)
player1PosLabel.grid(row=1, column=1, sticky=W, padx=10)

Label(info, text="Nunchuck input:").grid(row=2, column=0, sticky=W, padx=10)

suggestedInputP1 = Label(info)
suggestedInputP1.grid(row=2, column=1, sticky=W, padx=10)


def calculate_input_angle(camera_offset, angle):
    input_rads = angle - camera_offset - (math.pi / 2)
    return round(127 * math.cos(input_rads)) + 128, round(127 * math.sin(input_rads)) + 128


unhooked.pack()

while not dolphin.is_hooked():
    dolphin.hook()
    window.update()

unhooked.pack_forget()
info.pack()

while dolphin.is_hooked():

    player1x = dolphin.read_float(2419802108)
    player1z = dolphin.read_float(2419802116)

    target1x = 25.6507
    target1z = 10.0086

    sinYaw = dolphin.read_float(2151539448)
    cosYaw = dolphin.read_float(2151539480)
    yaw = math.atan2(sinYaw, -cosYaw)

    angleToTarget1 = math.atan2(-(target1z - player1z), -(target1x - player1x))

    player1PosLabel['text'] = ('%.4f' % player1x) + " " + ('%.4f' % player1z)
    suggestedInputP1['text'] = str(calculate_input_angle(yaw, angleToTarget1))
    window.update()



