from map import Map
from camera import Camera
from command import Com, SmallMotor, LargeMotor, Servo, Switch, Movement
from actions import Actions
from visual import Visual

import math
import time
import os

# updating code
# git add .
# git commit -m "message"
# git push

# getting code
# cd robot/nuc-data
# git pull

running_nuc = os.name != 'nt'

preBlur = 9
postBlur = 7
resizeWidth = 256
resizeHeight = 192

green_range = [[40, 30, 30], [80, 255, 255]]
red_range = [[-10, 120, 70], [10, 255, 255]]

unitLength = 1452
unitRotation = 1575

camera_bias_x = -8

# roughStartX = 4.25
# roughStartY = 1.75
roughStartX = 0.75
roughStartY = 0.75

# stackOrder = [2, 4, 3, 1, 0]
stackOrder = [4, 2, 3, 1, 0]
maxLoop = 20
dropTime = 150

map = Map("mapleft.txt", roughStartX, roughStartY)
camera = Camera(running_nuc, resizeWidth, resizeHeight, preBlur, postBlur)
command = Com(115200)
visual = Visual(camera, camera_bias_x, green_range, red_range)
act = Actions(map, command, visual, unitLength, unitRotation, maxLoop, dropTime)

def init():
    command.startGyroCal(5000)
    while not command.isGyroCal():
        time.sleep(1/maxLoop)

    command.setPosition(map.roughStartX*unitLength, map.roughStartY*unitLength, map.startAng)

    command.setMotorEnable(LargeMotor.Lift, 1)
    command.setMotorDirection(LargeMotor.Lift, 0)
    command.setMotorCurrent(LargeMotor.Lift, 22)
    command.setMotorEnable(LargeMotor.Chute, 1)
    command.setMotorDirection(LargeMotor.Chute, 1)
    command.setMotorCurrent(LargeMotor.Chute, 100)

    command.setParameters(0.6, 0.00075)

    command.moveServo(Servo.Camera, 275)
    command.moveServo(Servo.Gate, 100)
    command.moveServo(Servo.LeftChute, 50)
    command.moveServo(Servo.RightChute, 520)

    command.motorMove(SmallMotor.Gate, 0, 100)
    command.setMotorSpeed(LargeMotor.Lift, 50)
    command.setMotorSpeed(LargeMotor.Chute, 100)

    time.sleep(1.5)

    command.motorMove(SmallMotor.Gate, 0, 0)
    command.setMotorDirection(LargeMotor.Chute, 0)
    command.setMotorDirection(LargeMotor.Lift, 0)

    time.sleep(0.25)

    command.setMotorEnable(LargeMotor.Lift, 0)
    command.setMotorSpeed(LargeMotor.Lift, 0)

    while not command.getSwitch(Switch.ChuteLimit):
        time.sleep(1/maxLoop)

    command.setMotorSpeed(LargeMotor.Chute, 0)
    command.setMotorDirection(LargeMotor.Chute, 1)


init()

act.turnToStack(Movement.Spin, stackOrder[0])
act.moveUptoStack(stackOrder[0])
act.alignCamera()
act.grabStack(stackOrder[0])
act.turnToPositionNearest(Movement.Spin, 0, 3)
act.sortStack()

act.turnToStack(Movement.Spin, stackOrder[1])
act.moveUptoStack(stackOrder[1])
act.alignCamera()
act.grabStack(stackOrder[1])
act.turnToPositionNearest(Movement.Spin, 4, 5)
act.sortStack()

act.turnToStack(Movement.Spin, stackOrder[2])
act.moveUptoStack(stackOrder[2])
act.alignCamera()
act.grabStack(stackOrder[2])
act.turnToPositionNearest(Movement.Spin, 3, 3)
act.sortStack()

# act.turnToStack(Movement.Spin,stackOrder[3])
# act.moveUptoStack(stackOrder[3])
# act.alignCamera()
# act.grabStack(stackOrder[3])
# act.sortStack()

# act.turnToStack(Movement.Spin, stackOrder[4])
# act.moveUptoStack(stackOrder[4])
# act.alignCamera()
# act.grabStack(stackOrder[4])
# act.sortStack()



act.turnToPositionNearest(Movement.Spin, 4, 2)
act.moveToPosition(4, 2, 1)
act.turnToBearngNearest(Movement.Spin, math.pi)
act.dropGround()

act.turnToPositionNearest(Movement.Spin, 4, 3.5)
act.moveToPosition(0.5, 2.5, 1)
act.turnToBearingNearest(Movement.Spin, math.pi)
# act.waitDrop()
act.dropPlatform()

camera.destroy()
