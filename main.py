import dolphin_memory_engine as dolphin
import math
from tkinter import *

window = Tk()
window.title("Dolphin Line Calculator")

Label(window, text="Player 1").grid(row=0, column=0, sticky=W, padx=10)

Label(window, text="Position:").grid(row=1, column=0, sticky=W, padx=10)

player1PosLabel = Label(window)
player1PosLabel.grid(row=1, column=1, sticky=W, padx=10)

Label(window, text="Nunchuck input:").grid(row=2, column=0, sticky=W, padx=10)

sugestedInput = Label(window)
sugestedInput.grid(row=2, column=1, sticky=W, padx=10)

dolphin.hook()

inputAngle = 0

while dolphin.is_hooked():

    player1x = dolphin.read_float(2419802108)
    player1z = dolphin.read_float(2419802116)

    target1x = 25.6507
    target1z = 10.0086

    sinYaw = dolphin.read_float(2151539448)
    cosYaw = dolphin.read_float(2151539480)

    yawRad = math.atan2(sinYaw, -cosYaw)

    destinationAngle = math.atan2(-(target1z - player1z), -(target1x - player1x))

    inputRads = destinationAngle - yawRad - (math.pi/2)

    oldInputAngle = inputAngle
    inputAngle = round(127*math.cos(inputRads))+128, round(127*math.sin(inputRads))+128

    sugestedInput['text'] = str(inputAngle)
    player1PosLabel['text'] = ('%.4f' % player1x)+" "+('%.4f' % player1z)
    window.update()



