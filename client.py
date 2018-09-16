import json


def get_index_options(dict_in):
    return {str(index): option for index, option in enumerate(dict_in)}


def print_index_options(index_options):
    for index, option in index_options.items():
        print(f"{index}: {option}")


class Client:
    def __init__(self, data_path):
        self.data_path = data_path
        self.option = 0

    def run(self):
        print("\nWelcome to HS_Matchups!\n")
        with open(self.data_path) as matchups_file:
            self.matchups = json.load(matchups_file)
        self.handle_input_decks()

    def exit(self):
        print("Good luck out there!")
        with open(self.data_path, "w") as matchups_file:
            json.dump(self.matchups, matchups_file)

    def prompt(self):
        print("=" * 69)
        self.option = input(f"Select an option: ")
        print("=" * 69)

    def prompt_decks(self, deck_options):
        print("=" * 10)
        print("Your decks:")
        print_index_options(deck_options)
        print("=" * 10)
        print("Other options:")
        print(f"q: Quit")
        print(f"n: New deck!")
        print("=" * 10)
        self.prompt()

    def handle_input_decks(self):
        deck_options = get_index_options(self.matchups)
        self.prompt_decks(deck_options)
        while(self.option != "q"):
            if self.option == "n":
                self.handle_new_deck()
                deck_options = get_index_options(self.matchups)
            elif self.option in deck_options:
                deck_name = deck_options[self.option]
                self.handle_input_opponents(deck_name, self.matchups[deck_name])
            else:
                print("Unrecognized command, please try again!")
            self.prompt_decks(deck_options)
        self.exit()

    def handle_new_deck(self):
        deck_name = input(f"What deck are you adding? ")
        self.matchups.update({deck_name: {}})
        print(f"Deck {deck_name} added!")

    def prompt_opponents(self, deck_name, opponents_options):
        print("=" * 10)
        print(f"Here are the opponents {deck_name} has faced:")
        print_index_options(opponents_options)
        print("=" * 10)
        print("Other options:")
        print(f"b: Back")
        print(f"a: Print all stats")
        print(f"o: Print overall stats")
        print(f"fn: Filter by name")
        print(f"fs: Filter by speed")
        print(f"g: Remove filter")
        print(f"n: New opponent!")
        print("=" * 10)
        self.prompt()

    def handle_input_opponents(self, deck_name, opponents):
        opponents_options = get_index_options(opponents)
        self.prompt_opponents(deck_name, opponents_options)
        while(self.option != "b"):
            if self.option == "n":
                self.handle_new_opponent(deck_name)
                opponents_options = get_index_options(opponents)
            elif self.option == "a":
                self.print_all_stats(deck_name, opponents, opponents_options)
            elif self.option == "o":
                self.print_overall_stats(deck_name, opponents, opponents_options)
            elif self.option == "fn":
                filter = input("What name filter would you like to apply? ")
                opponents_options = get_index_options({
                    opponent_name: stats
                    for opponent_name, stats in opponents.items()
                    if filter.lower() in opponent_name.lower()
                })
                self.print_overall_stats(deck_name, opponents, opponents_options)
                print(f"Filtered by {filter}")
            elif self.option == "fs":
                speed = input("What speed decks would you like to see? ")
                opponents_options = get_index_options({
                    opponent: stats
                    for opponent, stats in opponents.items()
                    if stats["speed"].lower() == speed.lower()
                })
                self.print_overall_stats(deck_name, opponents, opponents_options)
                print(f"Showing {speed} decks")
            elif self.option == "g":
                opponents_options = get_index_options(opponents)
                print(f"Reverted to general display")
            elif self.option in opponents_options:
                opponent_name = opponents_options[self.option]
                self.handle_input_stats(opponent_name, opponents[opponent_name])
            else:
                print("Unrecognized command, please try again!")
            self.prompt_opponents(deck_name, opponents_options)
        print(f"Done with {deck_name}, going back to main menu...")

    def print_stats(self, opponent_name, stats):
        wins = stats["wins"]
        losses = stats["losses"]
        draws = stats["draws"]
        total = wins + losses + draws
        if total == 0:
            print(f"No games recorded against {opponent_name}")
            return
        win_percent = round(wins / total * 100, 2)
        loss_percent = round(losses / total * 100, 2)
        draw_percent = round(draws / total * 100, 2)
        print(f"{opponent_name}: {wins}-{losses}-{draws}, ({win_percent}, {loss_percent}, {draw_percent})")

    def print_all_stats(self, deck_name, opponents, opponents_options):
        print(f"Here is your matchup spread for {deck_name}:")
        for index, option in opponents_options.items():
            self.print_stats(option, opponents[option])

    def print_overall_stats(self, deck_name, opponents, opponents_options):
        wins = 0
        losses = 0
        draws = 0
        for index, option in opponents_options.items():
            wins += opponents[option]["wins"]
            losses += opponents[option]["losses"]
            draws += opponents[option]["draws"]
        total = wins + losses + draws
        if total == 0:
            print (f"No games recorded for {deck_name}")
            return
        win_percent = round(wins / total * 100, 2)
        loss_percent = round(losses / total * 100, 2)
        draw_percent = round(draws / total * 100, 2)
        print(f"Overall stats for {deck_name}: {wins}-{losses}-{draws}, ({win_percent}, {loss_percent}, {draw_percent})")

    def handle_new_opponent(self, deck_name):
        opponent_name = input(f"What opponent are you adding? (hit ENTER to cancel) ")
        if opponent_name == "":
            return
        if opponent_name in self.matchups[deck_name]:
            print(f"Opponent {opponent_name} already exists!")
            return
        speed = input(f"What speed is this opponent? (options are Aggro, Midrange, Control, and Combo) ")
        self.matchups[deck_name].update({opponent_name: {"wins": 0, "losses": 0, "draws": 0, "speed": speed}})
        print(f"{speed} opponent {opponent_name} added!")

    def prompt_stats(self, opponent_name, stats):
        print("=" * 10)
        print(f"Here are the stats against {opponent_name}:")
        self.print_stats(opponent_name, stats)
        print("=" * 10)
        print("Other options:")
        print(f"b: Back")
        print(f"w: Add wins")
        print(f"l: Add losses")
        print(f"d: Add draws")
        print("=" * 10)
        self.prompt()

    def handle_input_stats(self, opponent_name, stats):
        self.prompt_stats(opponent_name, stats)
        while(self.option != "b"):
            if self.option == "w":
                new_wins = int(input("Congrats! How many wins to add? "))
                stats["wins"] += new_wins
            elif self.option == "l":
                new_losses = int(input("How many losses to add? "))
                stats["losses"] += new_losses
            elif self.option == "d":
                new_draws = int(input("...Really?  Ok, how many draws to add? "))
                stats["draws"] += new_draws
            else:
                print("Unrecognized command, please try again!")
            self.prompt_stats(opponent_name, stats)
