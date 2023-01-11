from Player import Player
from Game import Card

import numpy as np
import cv2

from Render import RenderCards
from Render import ShowCardImage

# p=Player()
# p.AddCard(Card.p3, Card.s11, Card.o1, Card.c12)
# p.StartTurn()
# p.PlayCard(Card.p3, Card.o1)
# RenderCards(p.cards, scale = 1.0)
# ShowCardImage()

def makeGrayImage():
    path = r'Icons\tool.png'
    img = cv2.imread(path, -1)
    intensity = img.sum(axis=2)
    print(intensity[200])
    clampVal = 200
    for i in range(len(intensity)):
        newVal = 255
        if intensity[i] < clampVal:
            newVal = 0
        # get the X axis

        # Get the Y axis

        # Update the pixel
        # img[y][x][0] = newVal
        # img[y][x][1] = newVal
        # img[y][x][2] = newVal
    cv2.imshow('image', img)
    cv2.waitKey(0)

def makeGrayImage2(intensity = 200):
    path = r'Icons\tool.png'
    img = cv2.imread(path, -1)
    print(img)
    def exp(red, green, blue, alpha):
        r = int(red)
        g = int(green)
        b = int(blue)
        sm = r + g + b
        if sm < intensity:
            return 0
        return 255
    bla = np.zeros(img.shape[:2])
    for a in range(img.shape[0]):
        for b in range(img.shape[1]):
            bla[a,b] = exp(*img[a,b])
    print(bla)
    # res = np.linalg.norm(np.stack(
    #     img[:,:,0] - img[]
    # ))
    cv2.imshow('image', bla)
    cv2.waitKey(0)

makeGrayImage2()
