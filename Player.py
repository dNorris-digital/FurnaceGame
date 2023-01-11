from Game import Game
from Visualization.Render import RenderCards
from Visualization.Render import ShowCardImage

class Player(Game):
    def __init__(self):
        super(Player, self).__init__()

    def StartTurn(self):
        if self.TurnInProgress:
            print("You tried to start your turn but your turn is already in progress.")
            print("Continue playing your turn.")
            self.ShowHand(r=False)
            return

        self.TurnInProgress = True
        # Make sure all cards are marked as unused
        for i in self.cards.keys():
            self.cards[i][0] = False

        print("Your turn has started!")
        print("When you're finished, call FinishTurn()")
        self.ShowHand(r=True)

    def FinishTurn(self, force=False, f=False):
        if not self.TurnInProgress:
            print("You tried to finish your turn but your turn is not in progress!")
            return
        # Check if any cards have not been used yet
        unusedCards = []
        for i in self.cards.keys():
            if not self.cards[i][0]:
                unusedCards.append(i.value)
        if len(unusedCards):
            print("You still have {} cards that haven't been played yet".format(len(unusedCards)))
            print("Unused Cards: {}".format(unusedCards))
        if force or f or len(unusedCards) == 0:
            self.TurnInProgress = False
            self.lastCard = None
            print("Turn finished!")
        else:
            print("Turn NOT finished!")

    def PlayCard(self, *args, **kwargs):
        if self.TurnInProgress:
            self.PlayCardBase(*args, **kwargs)
            self.ShowRes()
        else:
            print("You cannot play a card until you have started your turn!")
            print("Call StartTurn() to start your turn.")

    def UnplayLastCard(self):
        status = self.UndoLastCardBase()
        if status:
            self.ShowRes()
            print('Card {} unplayed.'.format(self.lastCard))
            self.lastCard = None
        else:
            print("Unable to unplay last card '{}'.".format(self.lastCard))

    def AddResources(self, steel=0, coal=0, oil=0, tool=0, **kwargs):
        self.AddRes(steel=steel, coal=coal, oil=oil, tool=tool)

    def AddRes(self, steel=0, coal=0, oil=0, tool=0, **kwargs):
        self.steel += steel
        self.coal += coal
        self.oil += oil
        self.tool += tool

    def AddCard(self, *args):
        if self.TurnInProgress:
            print("You cannot add cards while your turn is in progress.")
            print("If you are done with your turn, call FinishTurn(). Then you can add new cards.")
            return
        for arg in args:
            if arg in self.cards.keys():
                print("Card {} is already in your deck!".format(arg))
                self.ShowHand(r=False)
            else:
                self.cards[arg] = [False, False]

    def ShowHand(self, r=True, scale = 0.8, **kwargs):
        cards = []
        items = list(self.cards.keys())
        for i in range(len(items)):
            if self.cards[items[i]][1]:
                cards.append('{}a'.format(items[i].value))
            else:
                cards.append(items[i].value)
        print('Current Hand: {}'.format(cards))
        if r:
            RenderCards(self.cards, scale=scale)
            ShowCardImage()

    def ShowRes(self):
        print('Coal: {}, Steel: {}, Oil: {}, Tool: {}, Coin: {}'.format(self.coal, self.steel, self.oil, self.tool, self.coin))

    def ShowResources(self):
        self.ShowRes()