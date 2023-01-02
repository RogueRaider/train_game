from enum import Enum
import random
from itertools import groupby

settings = {
    'staring_cars': 25,
    'board_name': 'test1'
}

class Colors(Enum):
    RED = 1
    YELLOW = 2
    PINK = 3
    WILD = 4

class Player(object):
    """
    Players of the game
    """
    def __init__(self, name: str, cars: int):
        self.name = name
        self.score = 0
        self.cars = cars
        self.hand = list()
        self.tickets = list()

    def choose_tickets(self, tickets):
        pass

    def turn_action(self, board):
        # Three options
        # 1. Pick up cards
        #   - pick up displayed or
        # 3. Pick up tickets
        # 4. Lay track
        pass

    def _display_hand(self) -> str:
        """
        A string showing the players card summary grouped by color
        :return:
        """
        hand = ''
        self.hand.sort(key=lambda x: x.color)
        for color, group in groupby(self.hand, lambda x: x.color):
            hand += f'{color} x{len(list(group))} '

        return hand

    def __repr__(self):
        return f'Name: {self.name}\n' \
               f'Score: {self.score}\n' \
               f'Hand: {self._display_hand()}\n' \
               f'Cars: {self.cars}'

class ConsolePlayer(Player):
    """
    Player that allows interaction using the console.
    """
    def __init__(self, name: str, cars: int):
        super().__init__(name, cars)

    def choose_tickets(self, tickets):
        print('Choose destination tickets from the options below.\nEnter the number of the ticket or "n" for no selection')
        for i, ticket in enumerate(tickets):
            print(i, ticket)
        selections = list()
        selections.append(input('Enter number to select first ticket:'))
        selections.append(input('Enter number to select second ticket:'))
        selections.append(input('Enter number to select third ticket:'))

        for selection in selections:
            if selection == 'n':
                continue
            if int(selection) in range(len(tickets)):
                self.tickets.append(tickets[int(selection)])
            else:
                print(f'"{selection}" not available')

    def turn_action(self, board):
        print(f'Player: {self.name}')
        print(f'Hand: {self._display_hand()}')
        print(board.get_state())
        action = input(f'Options:\n1 Pick Up Cards\n2 Lay Track\n3 Pick Up tickets\n')


class RandomPlayer(Player):
    def __init__(self, name: str, cars: int):
        super().__init__(name, cars)

    def choose_tickets(self, tickets):
        self.tickets = random.sample(tickets, random.choice([1,2,3]))


class Card(object):
    """
    Colors card
    """
    def __init__(self, color: Colors):
        self.color = color.name

    def __repr__(self):
        return f'Color: {self.color}'

class Route(object):
    """
    Connects two tickets
    """

    def __init__(self, city_one: str, city_two: str, cost: int, color: Colors):
        self.city_one = city_one
        self.city_two = city_two
        self.cost = cost
        self.color = color.name
        self.available = True

    def __repr__(self):
        return f'City One: {self.city_one}\n' \
               f'City Two: {self.city_two}\n' \
               f'Cost: {self.cost}\n' \
               f'Colors: {self.color}\n' \
               f'Available: {self.available}\n'

class Ticket(object):
    """
    Objective for the players to achieve
    """

    def __init__(self, city_one: str, city_two: str, value: int):
        self.city_one = city_one
        self.city_two = city_two
        self.value = value

    def __repr__(self):
        return f'{self.city_one} - {self.city_two}\n' \
               f'Value: {self.value}\n'

class Board(object):
    """
    Contains all the basic functional elements of the game.
    Is overloaded with the class containing the version of the game being played.
    """

    def __init__(self, players: list):
        self.players = players
        self.name = 'Empty'
        self.routes = list()
        self.available_cards = list()

    def get_state(self) -> str:
        """
        Returns a string showing board state for players to view.
        :return: str
        """
        state = f'Available Cards:\n'
        for card in self.available_cards:
            state += f'{str(card.color)} '
        state += f'\nAvailable Routes:\n'
        for route in self.routes:
            if route.available:
                state += str(route)
        return state

    def __repr__(self):
        return f'Name: {self.name}\n' \
               f'Route Count:{len(self.routes)}\n' \

class AustraliaBoard(Board):

    def __init__(self, players: list):
        super().__init__(players)
        self.name = 'Australia Board'

        # set up routes
        self.routes = list()
        self.routes.append(Route("Brisbane", "Adelaide", 5, Colors.RED))
        self.routes.append(Route("Brisbane", "Perth", 4, Colors.PINK))
        self.routes.append(Route("Brisbane", "Sydney", 3, Colors.RED))
        self.routes.append(Route("Sydney", "Perth", 3, Colors.WILD))
        self.routes.append(Route("Sydney", "Hobart", 3, Colors.RED))

        # set up playing deck
        self.deck = list()
        for color in Colors:
            for i in range(5):
                self.deck.append(Card(color))
        random.shuffle(self.deck)

        # set up destination cards
        self.tickets = list()
        self.tickets.append(Ticket('Brisbane', 'Sydney', 10))
        self.tickets.append(Ticket('Brisbane', 'Perth', 5))
        self.tickets.append(Ticket('Brisbane', 'Hobart', 6))
        self.tickets.append(Ticket('Brisbane', 'Adelaide', 20))
        self.tickets.append(Ticket('Brisbane', 'A', 20))
        self.tickets.append(Ticket('Brisbane', 'B', 20))
        self.tickets.append(Ticket('Brisbane', 'C', 20))
        self.tickets.append(Ticket('Brisbane', 'D', 20))
        random.shuffle(self.tickets)

        # set up players with starting hand and tickets
        for player in self.players:
            # give players starting hand
            for i in range(5):
                player.hand.append(self.deck.pop())
            # get players to choose destination tickets
            player.choose_tickets(self.tickets[-3:])
            # remove the chosen tickets from the available tickets
            self.tickets = list(set(self.tickets) - set(player.tickets))

        # set up board with cards
        for i in range(5):
            self.available_cards.append(self.deck.pop())


class GuiEvent(object):

    def update(self, board: Board):
        print(board)

class Game(object):
    """
    Single game containing a board
    """
    def __init__(self, name: str, board: Board, players: list):
        self.name = name
        self.board = board
        self.players = players
        self.turn_count = 0
        self.gui_event = GuiEvent()
        self._game_over = False

    def end_game(self):
        print(f"The game is over.")
        print(self)

    def run_game(self):

        # setting up game
        print(f"Starting game: {self.name}")

        # Each player gets a turn
        for player in self.players:
            print(f"Starting new turn for {player.name}")
            print(self.board.get_state())
            player.turn_action(self.board)
            print()
            self.turn_count += 1


        self.end_game()

    def __repr__(self):
        return f'Name: {self.name}\n' \
               f'Player Count: {len(self.players)}\n' \
               f'Turn Count: {self.turn_count}'



def main():

    # setup game and players

    players = list()
    players.append(ConsolePlayer('Rodney', settings['staring_cars']))
    players.append(RandomPlayer('James', settings['staring_cars']))


    b1 = AustraliaBoard(players)
    print(b1)

    g1 = Game('Test Game', b1, players)
    print(g1)
    g1.run_game()

    # every player takes a turn
    # player have action options 1 lay track 2 pick up cards



if __name__ == '__main__':
    main()

