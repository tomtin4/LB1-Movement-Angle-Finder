from calendar import error

import dolphin_memory_engine as dolphin
import math
from tkinter import *

window = Tk()
window.title("Dolphin Line Calculator")
window.resizable(False, False)


unhookedFrame = Frame(window)
Label(unhookedFrame, text="Please run dolphin emulator...").grid(row=0, column=0, sticky=W, padx=10)


infoFrame = Frame(window)

Label(infoFrame, text="Player 1").grid(row=0, column=0, sticky=W, padx=10)

target1XPosEntry = Entry(infoFrame, width=17)
target1XPosEntry.grid(row=1, column=1, sticky=W, padx=10)
target1XPosEntry.insert(0, "0.0")

target1ZPosEntry = Entry(infoFrame, width=17)
target1ZPosEntry.grid(row=1, column=2, sticky=W, padx=10)
target1ZPosEntry.insert(0, "0.0")

Label(infoFrame, text="Position:").grid(row=2, column=0, sticky=W, padx=10)

player1PosLabel = Label(infoFrame)
player1PosLabel.grid(row=2, column=1, sticky=W, padx=10)

Label(infoFrame, text="Speed:").grid(row=3, column=0, sticky=W, padx=10)

player1SpeedLabel = Label(infoFrame)
player1SpeedLabel.grid(row=3, column=1, sticky=W, padx=10)

Label(infoFrame, text="Velocity:").grid(row=4, column=0, sticky=W, padx=10)

player1VelocityLabel = Label(infoFrame)
player1VelocityLabel.grid(row=4, column=1, sticky=W, padx=10)

Label(infoFrame, text="Efficiency %:").grid(row=5, column=0, sticky=W, padx=10)

player1EfficiencyLabel = Label(infoFrame)
player1EfficiencyLabel.grid(row=5, column=1, sticky=W, padx=10)

Label(infoFrame, text="Nunchuck input:").grid(row=6, column=0, sticky=W, padx=10)

suggestedInputP1 = Label(infoFrame)
suggestedInputP1.grid(row=6, column=1, sticky=W, padx=10)


def calculate_input_angle(camera_offset, angle):
    input_rads = angle - camera_offset - (math.pi / 2)
    return round(127 * math.cos(input_rads)) + 128, round(127 * math.sin(input_rads)) + 128


player1x = 0.0
player1z = 0.0
speed1 = 0.0
velocity1 = 0.0


unhookedFrame.pack()

while not dolphin.is_hooked():
    dolphin.hook()
    window.update()

canRead = False
while not canRead:
    try:
        dolphin.read_float(2419802108)
        canRead = True
    except:
        print(error)


unhookedFrame.pack_forget()
infoFrame.pack()

while dolphin.is_hooked():

    oldPlayer1x = player1x
    oldPlayer1z = player1z
    player1x = dolphin.read_float(2419802108)
    player1z = dolphin.read_float(2419802116)

    try:
        target1x = float(target1XPosEntry.get())
    except:
        target1x = 0.0
    try:
        target1z = float(target1ZPosEntry.get())
    except:
        target1z = 0.0

    sinYaw = dolphin.read_float(2151539448)
    cosYaw = dolphin.read_float(2151539480)
    yaw = math.atan2(sinYaw, -cosYaw)

    angleToTarget1 = math.atan2(-(target1z - player1z), -(target1x - player1x))

    if oldPlayer1x != player1x or oldPlayer1z != player1z:
        speed1 = math.sqrt(((player1x-oldPlayer1x)**2) + ((player1z-oldPlayer1z)**2))
        velocity1 = math.sqrt(((target1x-oldPlayer1x)**2) + ((target1z-oldPlayer1z)**2)) - math.sqrt(((target1x-player1x)**2) + ((target1z-player1z)**2))

    player1PosLabel['text'] = ('%.4f' % player1x) + " " + ('%.4f' % player1z)
    player1SpeedLabel['text'] = '%.12f' % speed1
    player1VelocityLabel['text'] = '%.12f' % velocity1
    player1EfficiencyLabel['text'] = '%.10f' % ((velocity1/speed1)*100)
    suggestedInputP1['text'] = str(calculate_input_angle(yaw, angleToTarget1))
    window.update()



