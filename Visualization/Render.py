from Deck import CardDeck
from Deck import Card

import cv2
import os

import numpy as np

from PIL import Image

# directory = r'C:\Users\danno\Documents\FurnaceProgram\Visualization\Icons'
cDir = os.getcwd()
directory = os.path.join(cDir, r'Visualization\Icons')
cardImagePath = os.path.join(cDir, r'HandImage.png')

sysDebug = False

def checkAdvancedString(s, kwa):
    # Check if it is advanced
    adv = 'advanced'
    if adv in kwa.keys():
        a = kwa[adv]
        if not a:
            pSplit = s.split('.')
            s = '{}G.{}'.format(pSplit[0], pSplit[1])
    return s

def oilPath(**kwargs):
    path = r'oil.png'
    path = checkAdvancedString(path, kwargs)
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 1.0

def coalPath(**kwargs):
    path = r'coal.png'
    path = checkAdvancedString(path, kwargs)
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 0.55

def coinPath(**kwargs):
    arg = 'count'
    default = r'coin.png'
    scale = 0.6
    if arg in kwargs:
        val = kwargs[arg]
        vals = [2, 4, 5, 6, 7]
        if val in vals:
            path = r'coin{}.png'.format(val)
            scale = 0.75
        else:
            path = default
    else:
        path = default
    path = checkAdvancedString(path, kwargs)
    if not directory == None:
        path = os.path.join(directory, path)
    return path, scale

def steelPath(**kwargs):
    path = r'steel.png'
    path = checkAdvancedString(path, kwargs)
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 0.9

def toolPath(**kwargs):
    path = r'tool.png'
    path = checkAdvancedString(path, kwargs)
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 0.5

def checkPath(**kwargs):
    path = r'check.png'
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 2

def arrowPath(**kwargs):
    arg = 'count'
    if arg in kwargs:
        val = kwargs[arg]
        if val == 'inf':
            path = r'infArrow.png'
        elif val == None or val == 0:
            path = r'arrow.png'
        else:
            if val > 9:
                val = 9
            if val < 1:
                val = 1
            path = r'arrow{}.png'.format(val)
    else:
        path = r'arrow.png'
    return os.path.join(directory, path), 0.5

def numberPath(**kwargs):
    arg = 'count'
    if arg in kwargs:
        val = kwargs[arg]
        path = r'{}.png'.format(val)
        if not directory == None:
            path = os.path.join(directory, path)
        return path, 0.5
    return ''

def flipPath(**kwargs):
    path = r'flip.png'
    if not directory == None:
        path = os.path.join(directory, path)
    return path, 0.4

def getBackground(size):
    path = r'background.png'
    if not directory == None:
        path = os.path.join(directory, path)
    img = cv2.imread(path)
    h = img.shape[0]
    w = img.shape[1]
    dim = (int(w * size), int(h * size))
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

def getIcon(iconSize, pathFn, count = None, advanced = False):
    path, scl = pathFn(count = count, advanced = advanced)
    if sysDebug:
        print('getIcon....pathFn: {}, path: {}, scale: {}, count: {}, advanced: {}'.format(pathFn, path, scl, count, advanced))
    iconSize *= scl
    img = cv2.imread(path, -1)
    oDims = img.shape
    h = oDims[0]
    w = oDims[1]

    dim = (int(w * (iconSize / w)), int(h * (iconSize / h)))
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

def compileSequence(Resource, iconSize, advanced=True):
    '''
    Takes in an instance of Res class and outputs a list of icon images for each object represented in instance.
    :param Resource: Res instance
    :return: list of icon images
    '''
    outData = []
    if Resource.oil:
        icon = getIcon(iconSize, oilPath, advanced=advanced)
        for i in range(Resource.oil):
            outData.append(icon)
    if Resource.coal:
        icon = getIcon(iconSize, coalPath, advanced=advanced)
        for i in range(Resource.coal):
            outData.append(icon)
    if Resource.steel:
        icon = getIcon(iconSize, steelPath, advanced=advanced)
        for i in range(Resource.steel):
            outData.append(icon)
    if Resource.tool:
        icon = getIcon(iconSize, toolPath, advanced=advanced)
        for i in range(Resource.tool):
            outData.append(icon)
    if Resource.coin:
        icon = getIcon(iconSize, coinPath, Resource.coin, advanced=advanced)
        outData.append(icon)
    return outData

def overlay(background, image, coord=(0.5, 0.5)):
    '''
    Overlays the image into the backgroud and returns the new image
    :param background: Background image to overlay onto
    :param image: Image to add
    :param coord: 0-1 scalar coordinates the image will be placed on
    :return: The superimposed image
    '''
    ihy = image.shape[0] / 2
    ihx = image.shape[1] / 2
    yOfs = int(background.shape[0] * coord[0] - ihy)
    xOfs = int(background.shape[1] * coord[1] - ihx)
    if yOfs < 0: yOfs = 0
    if xOfs < 0: xOfs = 0
    y1, y2 = yOfs, yOfs + image.shape[0]
    x1, x2 = xOfs, xOfs + image.shape[1]
    iAlpha = image[:, :, 3] / 255.0
    bAlpha = 1.0 - iAlpha

    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (iAlpha * image[:, :, c] + bAlpha * background[y1:y2, x1:x2, c])

    return background

def overlaySimple(background, image, coord=(0, 0)):
    background[coord[0]: coord[0] + image.shape[0], coord[1]: coord[1] + image.shape[1]] = image
    return background

def overlayList(background, images, rowCoord):
    tween = 0.1
    totalSpace = tween * (len(images) - 1)
    c = (1.0 - totalSpace) * 0.5
    for i in range(len(images)):
        overlay(background, images[i], coord=(rowCoord, c))
        c += tween
    return background

def overlayLines(background, lines = [], color = (100, 100, 255, 0.1), thickness = 2, sequence=False, **kwargs):
    '''
    Draws a series of lines on the image and returns the new version of it.
    :param background: Image to draw on
    :param color: Color the lines should be
    :param lines: list of line points in format of 0-1 scalars that will be applied to the image resolution
    :param sequence: Boolean whether or not the images should be drawn in a sequence or separate lines for each set of two coordinates
    :return: New version of the image
    '''
    dims = background.shape
    i = 0
    while i < len(lines) - 1:
        # Determine the coordinates
        x1 = int(dims[1] * lines[i][0])
        y1 = int(dims[0] * lines[i][1])
        i += 1
        x2 = int(dims[1] * lines[i][0])
        y2 = int(dims[0] * lines[i][1])
        # Draw the line
        background = cv2.line(background, (x1, y1), (x2, y2), color, thickness)
        if not sequence:
            i += 1
    return background

def IsPersonalCard(Card):
    return 'p' in Card.value

def RenderCard(card, advanced = False, played = False, cardSize = 0.9, *args, **kwargs):
    iconSize = 65 * cardSize
    bg = getBackground(cardSize)

    # Lay resource icons along the top
    cData = CardDeck[card]
    resIcons = []
    resIcons.extend(compileSequence(cData['ResourceSource'], iconSize))
    if cData['ResourceSource'].IsNotEmpty() and cData['ResourceValue'].IsNotEmpty():
        resIcons.append(getIcon(iconSize, arrowPath))
        # pass
    resIcons.extend(compileSequence(cData['ResourceValue'], iconSize))
    # Add the resource icons
    img = overlayList(bg, resIcons, 0.075)

    # Add the card code
    ty = int(img.shape[0] * 0.26)
    tx = int(img.shape[1] * 0.75)
    img = cv2.putText(img, card.name, (ty, tx), cv2.FONT_HERSHEY_SIMPLEX, 2 * cardSize, (0, 0, 0), int(4 * cardSize), cv2.LINE_AA)

    # If played, add the checkmark
    if played:
        img = overlay(img, getIcon(iconSize, checkPath), (0.475, 0.5))

    # Check if it's a personal card and render the tool if it is
    isPersonal = IsPersonalCard(card)
    if isPersonal:
        img = overlay(img, getIcon(iconSize, toolPath), (0.7, 0.5))

    # Set first trade data
    trade1Icons = []
    trade1Icons.extend(compileSequence(cData['PrimarySource'], iconSize))
    if cData['PrimarySource'].IsNotEmpty() and cData['PrimaryValue'].IsNotEmpty():
        trade1Icons.append(getIcon(iconSize, arrowPath, cData['PrimaryCount']))
        # pass
    trade1Icons.extend(compileSequence(cData['PrimaryValue'], iconSize))
    # Add the resource icons
    img = overlayList(img, trade1Icons, 0.8)

    # Set second trade data
    trade2Icons = []
    trade2Icons.extend(compileSequence(cData['AdvancedSource'], iconSize, advanced)) # Source
    if cData['AdvancedSource'].IsNotEmpty() and cData['AdvancedValue'].IsNotEmpty():
        trade2Icons.append(getIcon(iconSize, arrowPath, cData['AdvancedCount'])) # Arrow
        # pass
    trade2Icons.extend(compileSequence(cData['AdvancedValue'], iconSize, advanced)) # Value
    if IsPersonalCard(card):
        trade2Icons.append(getIcon(iconSize, arrowPath, 'inf'))
        trade2Icons.append(getIcon(iconSize, flipPath))
    # Add the resource icons
    img = overlayList(img, trade2Icons, 0.9)

    # If the card is advanced, draw a red X over the second trade
    if not advanced and not isPersonal:
        x1 = 0.3
        x2 = 0.7
        y1 = 0.85
        y2 = 0.95
        lines = [(x1, y1), (x2, y2), (x2, y1), (x1, y2)]
        overlayLines(img, lines=lines)
    return img

def SaveCardImage(img):
    cv2.imwrite(cardImagePath, img)

def ShowCardImage():
    # Check if the image exists, if not, return False
    if os.path.exists(cardImagePath):
        im = Image.open(cardImagePath)
        im.show()
        return True
    return False

def RenderCards(Cards, scale=1.0, **kwargs):
    '''
    Takes the dictionary containing the cards in your hand and generates an image showing all cards
    :param Cards:
    :param args:
    :param kwargs:
    :return:
    '''
    cardCount = len(Cards)
    # Determine the size of the background
    if 'scale' in kwargs:
        scale = kwargs['scale']
    bg = getBackground(scale)
    ty = int(bg.shape[0])
    tx = int(bg.shape[1] * cardCount)
    # Create the image
    img = np.zeros((ty, tx, 3), dtype=np.uint8)
    cards = []
    cardItems = list(Cards.items())
    for a in range(cardCount):
        cardImage = RenderCard(cardItems[a][0], cardItems[a][1][1], cardItems[a][1][0], scale)
        cards.append(cardImage)
    coord = 0
    for i in range(len(cards)):
        img = overlaySimple(img, cards[i], (0, int(coord)))
        coord += bg.shape[1]
    # Save the card and return the path
    SaveCardImage(img)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)

# RenderCards(Card.s12, Card.s11, Card.p2, Card.s12, Card.c3, Card.p2, scale = 1.63)
# RenderCard(Card.s12, 0.7)
# FixArrow()

