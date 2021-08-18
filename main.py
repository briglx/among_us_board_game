#!/usr/bin/python
"""Main script for Game Simulator."""
import argparse
import logging
import random
import sys

ROOMS = [
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Bedroom",
    "Office",
    "Office",
    "Office",
    "Office",
    "Office",
    "Bathroom",
    "Bathroom",
    "Bathroom",
    "Bathroom",
    "Bathroom",
    "Kitchen",
    "Kitchen",
    "Kitchen",
    "Kitchen",
    "Kitchen",
    "Garage",
    "Garage",
    "Garage",
    "Garage",
    "Garage",
    "Back Patio",
    "Back Patio",
    "Back Patio",
    "Back Patio",
    "Back Patio",
    "Living Room",
    "Living Room",
    "Living Room",
    "Living Room",
    "Living Room",
    "Fancy Room",
    "Fancy Room",
    "Fancy Room",
    "Fancy Room",
    "Fancy Room",
    "TV Room",
    "TV Room",
    "TV Room",
    "TV Room",
    "TV Room",
]
DEFAULT_PLAYERS = ["Player 1", "Player 2", "Player 3", "Player 4"]
DEFAULT_ASSIGNMENTS = ["Crew", "Crew", "Crew", "Imposter"]

# Global Variables
PLAYERS = []
ASSIGNMENTS = []
BODY_LOCATION = None
DECK = []


discard_pile = []

players_this_round = []
cur_player_idx = 0
ghosts = []


positions = {}
imposter = None
imposter_chances = 5
game_over = False

card_log = []


# logging.basicConfig(stream=sys.stdout, level=logging.WARN)
logging.basicConfig(filename="game.log", level=logging.WARN)


# def create_deck():

#     for _ in range(NUM_ROOM_CARDS):
#         for room in rooms:
#             deck.append(room)


def draw_card():
    global DECK
    global discard_pile
    global card_log

    card = DECK.pop(0)
    discard_pile.append(card)
    card_log.append(card)
    return card


def move_to_room(player, room):
    global positions
    positions[player] = room


def is_imposter(player):
    global PLAYERS
    global ASSIGNMENTS

    idx = PLAYERS.index(player)
    return ASSIGNMENTS[idx] == "Imposter"


def get_player_in_my_room(player):
    global positions

    targets = []

    if player in positions:
        my_room = positions[player]

        for p, r in positions.items():
            if r == my_room and p != player:
                targets.append(p)

    return targets


def kill_player(player):
    global ghosts
    global positions

    if player not in ghosts:
        ghosts.append(player)
        positions[player] = "Grave"


def call_emergency_meeting():
    global positions

    logging.info("Calling emergency meeting")
    active_players = [player for player in PLAYERS if player not in ghosts]
    if imposter and len(active_players) > 1:
        positions[imposter] = "Space"


def take_action(player):
    global imposter
    global positions


    if player in positions:

        targets = get_player_in_my_room(player)
        if len(targets) > 0:
            if is_imposter(player):
                if targets[0] != "Body":
                    logging.debug("Imposter taking action.")
                    kill_player(targets[0])
                    imposter = player
                    logging.info("%s killed %s", player, targets[0])
            else:
                if targets[0] == "Body":
                    logging.debug("Crew taking action.")
                    logging.info("%s found a body!", player)
                    if len(ghosts) > 0:
                        call_emergency_meeting()

        else:
            logging.debug("No target in the room.")

    else:
        logging.debug("%s not in a room.", player)


def active_players(players_this_round):
    global ghosts
    global positions

    for player in players_this_round:
        # Skip players who are eliminated
        if player in ghosts:
            pass
        elif imposter and player == imposter and (positions[imposter] == "Space"):
            pass
        else:
            yield player


def reset_game():
    global PLAYERS 
    PLAYERS = []
    global ASSIGNMENTS 
    ASSIGNMENTS = []
    global BODY_LOCATION 
    BODY_LOCATION= None
    global DECK 
    DECK = []
    discard_pile = []
    players_this_round = []
    cur_player_idx = 0
    global ghosts 
    ghosts = []
    global positions 
    positions = {}
    global imposter 
    imposter = None
    imposter_chances = 5
    global game_over 
    game_over = False
    card_log = []

def main():
    global game_over
    global DECK
    global ghosts
    global positions
    global imposter

    logging.debug("Enter players. %s", PLAYERS)
    logging.debug("Assignments: %s ", ASSIGNMENTS)
    logging.debug("Using Deck %s", DECK)

    logging.debug("Add body to game %s", BODY_LOCATION)
    move_to_room("Body", BODY_LOCATION)

    turn_count = 0
    imposter_reveal_turn = None
    while len(DECK) > 0 and not game_over:

        logging.info("Turn %s (%s)", turn_count + 1, imposter_reveal_turn)

        players_this_round = [player for player in PLAYERS if player not in ghosts]

        for player in active_players(players_this_round):

            if not game_over:
                # Take Action
                take_action(player)

                room = draw_card()
                logging.info("%s drew %s", player, room)
                move_to_room(player, room)

                # Take Action
                take_action(player)

                if imposter and (positions[imposter] == "Space"):
                    game_over = True

        # All players have played this turn.
        # update
        logging.debug("Positions after Turn")
        logging.debug(positions)

        if imposter:
            if not imposter_reveal_turn:
                imposter_reveal_turn = turn_count + imposter_chances + 1
            # imposter_chances = imposter_chances - 1

        if (turn_count + 1) == imposter_reveal_turn:
            break

        if len(PLAYERS) == (len(ghosts) + 1):
            break

        # Bump turn count
        turn_count = turn_count + 1

    logging.info("Ghosts %s", ghosts)

    winner = None
    if imposter and (positions[imposter] == "Space"):
        winner = "Crew!!"
    elif imposter and turn_count + 1 == imposter_reveal_turn:
        winner = "Crew!! Imposter ran out of turns"
    elif len(PLAYERS) == (len(ghosts) + 1):
        winner = "Imposter!!"
    else:
        winner = "No Winner"

    # logging.info(
    #     "%s with: \nplayers: %s\nassignments: %s\ndeck: %s\npositions: %s\nghosts: %s",
    #     winner,
    #     PLAYERS,
    #     ASSIGNMENTS,
    #     card_log,
    #     positions,
    #     ghosts,
    # )
    logging.warning(
        "%s, %s, %s, %s, %s", winner, PLAYERS, ASSIGNMENTS, positions, card_log
    )


if __name__ == "__main__":
    logging.debug("Starting script")

    parser = argparse.ArgumentParser(
        description="Among Us Board Game Simulator.",
        add_help=True,
    )
    parser.add_argument(
        "--players",
        "-p",
        help="Players",
    )
    parser.add_argument(
        "--assignments",
        "-a",
        help="Player assignments",
    )
    parser.add_argument(
        "--body_location",
        "-b",
        help="Room location of.",
    )
    parser.add_argument(
        "--deck",
        "-d",
        help="Shuffled Deck",
    )

    args = parser.parse_args()


    for _ in range(100):
        
        reset_game()

        if args.players:
            PLAYERS = args.players.split(",")
        else:
            PLAYERS = DEFAULT_PLAYERS
        if args.assignments:
            ASSIGNMENTS = args.assignments.split(",")
        else:
            ASSIGNMENTS = DEFAULT_ASSIGNMENTS.copy()
            random.shuffle(ASSIGNMENTS)
        if args.deck:
            DECK = args.deck.split(",")
        else:
            DECK = ROOMS.copy()
            random.shuffle(DECK)
        BODY_LOCATION = args.body_location or random.choice(ROOMS)

        main()
