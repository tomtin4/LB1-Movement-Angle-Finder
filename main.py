import dolphin_memory_engine as dolphin
import math
from tkinter import *
import json

window = Tk()
window.title("Dolphin Line Calculator")
window.resizable(False, False)


unhookedFrame = Frame(window, width=400, height=180)
Label(unhookedFrame, text="Please run dolphin emulator...").grid(row=0, column=0, sticky=W, padx=10)
unhookedFrame.grid_propagate(0)

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


Label(infoFrame, text="Player 2").grid(row=0, column=3, sticky=W, padx=10)

target2XPosEntry = Entry(infoFrame, width=17)
target2XPosEntry.grid(row=1, column=4, sticky=W, padx=10)
target2XPosEntry.insert(0, "0.0")

target2ZPosEntry = Entry(infoFrame, width=17)
target2ZPosEntry.grid(row=1, column=5, sticky=W, padx=10)
target2ZPosEntry.insert(0, "0.0")

Label(infoFrame, text="Position:").grid(row=2, column=3, sticky=W, padx=10)

player2PosLabel = Label(infoFrame)
player2PosLabel.grid(row=2, column=4, sticky=W, padx=10)

Label(infoFrame, text="Speed:").grid(row=3, column=3, sticky=W, padx=10)

player2SpeedLabel = Label(infoFrame)
player2SpeedLabel.grid(row=3, column=4, sticky=W, padx=10)

Label(infoFrame, text="Velocity:").grid(row=4, column=3, sticky=W, padx=10)

player2VelocityLabel = Label(infoFrame)
player2VelocityLabel.grid(row=4, column=4, sticky=W, padx=10)

Label(infoFrame, text="Efficiency %:").grid(row=5, column=3, sticky=W, padx=10)

player2EfficiencyLabel = Label(infoFrame)
player2EfficiencyLabel.grid(row=5, column=4, sticky=W, padx=10)

Label(infoFrame, text="Nunchuck input:").grid(row=6, column=3, sticky=W, padx=10)

suggestedInputP2 = Label(infoFrame)
suggestedInputP2.grid(row=6, column=4, sticky=W, padx=10)


def calculate_input_angle(camera_offset, angle):
    input_rads = angle - camera_offset - (math.pi / 2)
    return round(127 * math.cos(input_rads)) + 128, round(127 * math.sin(input_rads)) + 128

with open('addresses.json', 'r') as file:
    addressDict = json.load(file)

player1xAddress = addressDict["player1x"]
player1zAddress = addressDict["player1z"]
player2xAddress = addressDict["player2x"]
player2zAddress = addressDict["player2z"]
sinYawAddress = addressDict["sinYaw"]
cosYawAddress = addressDict["cosYaw"]

player1x = 0.0
player1z = 0.0
speed1 = 0.0
velocity1 = 0.0

player2x = 0.0
player2z = 0.0
speed2 = 0.0
velocity2 = 0.0

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
        print("Hmm, I cant find this value right now, try restarting dolphin.")


unhookedFrame.pack_forget()
infoFrame.pack()

while dolphin.is_hooked():

    oldPlayer1x = player1x
    oldPlayer1z = player1z
    player1x = dolphin.read_float(2419802108)
    player1z = dolphin.read_float(2419802116)

    oldPlayer2x = player2x
    oldPlayer2z = player2z
    player2x = dolphin.read_float(2419807996)
    player2z = dolphin.read_float(2419808004)

    try:
        target1x = float(target1XPosEntry.get())
    except:
        target1x = 0.0
    try:
        target1z = float(target1ZPosEntry.get())
    except:
        target1z = 0.0

    try:
        target2x = float(target2XPosEntry.get())
    except:
        target2x = 0.0
    try:
        target2z = float(target2ZPosEntry.get())
    except:
        target2z = 0.0

    sinYaw = dolphin.read_float(2151539448)
    cosYaw = dolphin.read_float(2151539480)
    yaw = math.atan2(sinYaw, -cosYaw)

    angleToTarget1 = math.atan2(-(target1z - player1z), -(target1x - player1x))
    angleToTarget2 = math.atan2(-(target2z - player2z), -(target2x - player2x))

    if oldPlayer1x != player1x or oldPlayer1z != player1z:
        speed1 = math.sqrt(((player1x-oldPlayer1x)**2) + ((player1z-oldPlayer1z)**2))
        velocity1 = math.sqrt(((target1x-oldPlayer1x)**2) + ((target1z-oldPlayer1z)**2)) - math.sqrt(((target1x-player1x)**2) + ((target1z-player1z)**2))

    if oldPlayer2x != player2x or oldPlayer2z != player2z:
        speed2 = math.sqrt(((player2x-oldPlayer2x)**2) + ((player2z-oldPlayer2z)**2))
        velocity2 = math.sqrt(((target2x-oldPlayer2x)**2) + ((target2z-oldPlayer2z)**2)) - math.sqrt(((target2x-player2x)**2) + ((target2z-player2z)**2))


    player1PosLabel['text'] = ('%.4f' % player1x) + " " + ('%.4f' % player1z)
    player1SpeedLabel['text'] = '%.12f' % speed1
    player1VelocityLabel['text'] = '%.12f' % velocity1
    player1EfficiencyLabel['text'] = '%.11f' % ((velocity1/speed1)*100)
    suggestedInputP1['text'] = str(calculate_input_angle(yaw, angleToTarget1))

    player2PosLabel['text'] = ('%.4f' % player2x) + " " + ('%.4f' % player2z)
    player2SpeedLabel['text'] = '%.12f' % speed2
    player2VelocityLabel['text'] = '%.12f' % velocity2
    player2EfficiencyLabel['text'] = '%.11f' % ((velocity2 / speed2) * 100)
    suggestedInputP2['text'] = str(calculate_input_angle(yaw, angleToTarget2))

    window.update()



