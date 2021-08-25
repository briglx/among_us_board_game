"""Constants for Game."""
import logging
import random

DEFAULT_PLAYERS = ["Player 1", "Player 2", "Player 3", "Player 4"]
DEFAULT_ASSIGNMENTS = ["Crew", "Crew", "Crew", "Imposter"]
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

POTENTIAL_ROOMS = {"Bedroom": 3, "Bathroom": 2}
IMPOSTER_CHANCES = 20

REWARD_IMPOSTER_TO_CREW = 10
REWARD_CREW_TO_BODY = 1
RISK_CREW_TO_IMPOSTER = 10
RISK_CREW_TO_RIVAL = 5


class Player:
    """Represent a player in the game."""

    def __init__(self, name, assignment, position=None):
        """Initialize the Player."""
        self._name = name
        self._assignment = assignment
        self._position = position

    @property
    def name(self):
        """Name of players."""
        return self._name

    @property
    def assignment(self):
        """Player assignment."""
        return self._assignment

    @property
    def position(self):
        """Position of players."""
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def is_imposter(self):
        """Check if player is imposter."""
        return self.assignment == "Imposter"

    def __repr__(self):
        """Pretty print Player."""
        return f"{self.name} ({self.assignment}, {self.position})"


def get_players(assignments=None):
    """Get players."""
    players = []
    for index, assignment in enumerate(assignments):
        players.append(Player(f"Player {index+1}", assignment))
    return players


class Simulation:
    """Simulator of board game."""

    def __init__(self, seed, assignments=None, body_location=None, deck=None):
        """Initialize the Game."""
        self._card_log = []
        self._ghosts = []
        self._game_over = False

        self._seed = seed
        random.seed(seed)

        # Make assignments
        if assignments is None:
            assignments = DEFAULT_ASSIGNMENTS.copy()
            random.shuffle(assignments)
        self._players = get_players(assignments)

        # Place Body
        self._body = Player("Body", "Body")
        if body_location is None:
            body_location = random.choice(ROOMS)
        self.move_to_room(self._body, body_location)

        if deck:
            self._deck = deck
        else:
            self._deck = ROOMS.copy()
            random.shuffle(self._deck)

        logging.debug("Enter players. %s", self._players)
        logging.debug("Assignments: %s ", assignments)
        logging.debug("Using Deck %s", self._deck)

    @property
    def ghosts(self):
        """List of ghosts."""
        return self._ghosts

    @property
    def players(self):
        """Players of the."""
        return self._players

    def draw_card(self):
        """Draw a card from the deck."""
        card = self._deck.pop(0)
        self._card_log.append(card)
        return card

    def imposter_has_killed(self):
        """Check if the imposter has killed."""
        return len(self._ghosts) > 0

    def kick_imposter_out(self):
        """Kick imposter into space."""
        for player in self._players:
            if player.assignment == "Imposter":
                player.position = "Space"

    def is_alive(self, player):
        """Check if player is alive."""
        return player not in self._ghosts

    def is_imposter_kicked_out(self):
        """Check if imposter is in space."""
        for player in self._players:
            if player.assignment == "Imposter":
                return player.position == "Space"
        return False

    def get_rivals_in_my_room(self, player):
        """Return rivals in same position of player."""
        rivals = []

        if player.position:
            for rival in self._players:
                if rival.name != player.name and rival.position == player.position:
                    rivals.append(rival)

            if self._body.position == player.position:
                rivals.append(self._body)

        return rivals

    def kill_player(self, player):
        """Kill the player."""
        if player not in self._ghosts:
            self._ghosts.append(player)
            player.position = "Grave"

    def active_players(self, players_this_round):
        """Return active players."""
        for player in players_this_round:
            # Skip players who are eliminated
            if player in self._ghosts:
                pass
            elif player.position == "Space":
                pass
            else:
                yield player

    def call_emergency_meeting(self):
        """Call emergency meeting."""
        logging.info("Calling emergency meeting")
        players_still_in_the_game = [
            player for player in self._players if player not in self._ghosts
        ]
        if self.imposter_has_killed() and len(players_still_in_the_game) > 1:
            # Kick Imposter out
            self.kick_imposter_out()
            # self._positions[self._imposter] = "Space"

    def take_action(self, player, is_entering):
        """Player takes action entering or leaving a room."""
        rivals = self.get_rivals_in_my_room(player)
        if len(rivals) > 0:
            if player.is_imposter():
                for rival in rivals:
                    if rival.name != "Body":
                        logging.debug("Imposter taking action.")
                        self.kill_player(rival)
                        logging.info("%s killed %s", player.name, rival.name)
                        break
            else:

                if is_entering:
                    # If Entering a room (Action after draw card)
                    # Check if there is an imposter and die
                    for rival in rivals:
                        if rival.assignment == "Imposter":
                            self.kill_player(player)
                            logging.info("%s killed %s", rival.name, player.name)

                # If Entering or Leaving a Room (Action before/after draw card)
                # Check if there is a body and a killer: Call meeting
                for rival in rivals:
                    if rival.name == "Body" and self.is_alive(player):
                        logging.debug("Crew taking action.")
                        logging.info("%s found a body!", player)
                        if len(self._ghosts) > 0:
                            self.call_emergency_meeting()

        else:
            logging.debug("No rivals in the room.")

    def rate_room_risk(self, player, room):
        """Rate the risk of the room."""
        if player.assignment == "Imposter":
            return 0

        room_risk = 0
        player_in_room = False
        imposter_in_room = False

        for rival in self.players:
            if rival.position == room:
                player_in_room = True
            if rival.assignment == "Imposter" and rival.position == room:
                imposter_in_room = True

        # Determine Risk
        if len(self._ghosts) > 0 and imposter_in_room:
            room_risk = room_risk + RISK_CREW_TO_IMPOSTER

        if len(self._ghosts) == 0 and player_in_room:
            room_risk = room_risk + RISK_CREW_TO_RIVAL

        return room_risk

    def rate_room_reward(self, player, room):
        """Rate the room reward score."""
        room_reward = 0

        if player.assignment == "Imposter":
            for rival in self.players:
                if rival != player and rival.position == room:
                    room_reward = room_reward + REWARD_IMPOSTER_TO_CREW

        if player.assignment == "Crew":
            if self._body.position == room:
                room_reward = room_reward + REWARD_CREW_TO_BODY

        return room_reward

    def find_optimal_room(self, player, potential_rooms):
        """Find optimal room based on risk and reward."""
        optimal_room = (-1, None)
        for room in potential_rooms:
            risk_score = self.rate_room_risk(player, room)
            reward_score = self.rate_room_reward(player, room)
            cur_score = reward_score - 2 * risk_score

            optimal_score, _ = optimal_room
            if cur_score > optimal_score:
                optimal_room = (cur_score, room)

        return optimal_room[1]

    def move_to_room(self, player, room):
        """Move player to room."""
        if room in POTENTIAL_ROOMS:
            potential_rooms = [room + str(x) for x in range(POTENTIAL_ROOMS[room])]
            ideal_room = self.find_optimal_room(player, potential_rooms)
            player.position = ideal_room
        else:
            player.position = room

    def reshuffle_deck(self):
        """Reshuffle the deck."""
        self._deck = ROOMS.copy()
        random.shuffle(self._deck)

    def calculate_winner(self, turn_count, imposter_reveal_turn):
        """Determine winner of simulation."""
        winner = None
        if self.is_imposter_kicked_out():
            winner = "Crew"
        elif turn_count + 1 == imposter_reveal_turn:
            winner = "Crew (Imposter ran out of turns)"
        elif len(self._players) == (len(self._ghosts) + 1):
            winner = "Imposter"
        else:
            winner = "No Winner"

        return winner

    def run(self):
        """Game loop for the game."""
        players_this_round = []
        turn_count = 0
        imposter_reveal_turn = None

        while len(self._deck) > 0 and not self._game_over:

            logging.info("Turn %s (%s)", turn_count + 1, imposter_reveal_turn)

            players_this_round = [
                player for player in self._players if player not in self._ghosts
            ]

            for player in self.active_players(players_this_round):

                if not self._game_over:
                    # Take Action
                    self.take_action(player, False)

                    if self.is_imposter_kicked_out():
                        self._game_over = True

                    if not self._game_over and self.is_alive(player):
                        room = self.draw_card()
                        logging.info("%s drew %s", player.name, room)
                        self.move_to_room(player, room)
                        # Take Action
                        self.take_action(player, True)

                        if self.is_imposter_kicked_out():
                            self._game_over = True

            # All players have played this turn.
            if self.imposter_has_killed():
                if not imposter_reveal_turn:
                    imposter_reveal_turn = turn_count + IMPOSTER_CHANCES + 1
                # imposter_chances = imposter_chances - 1

            if (turn_count + 1) == imposter_reveal_turn:
                break

            if len(self._players) == (len(self._ghosts) + 1):
                break

            if len(self._deck) <= (len(self._players) - len(self._ghosts)):
                self.reshuffle_deck()

            # Bump turn count
            turn_count = turn_count + 1

        logging.info("Ghosts %s", self._ghosts)

        winner = self.calculate_winner(turn_count, imposter_reveal_turn)

        logging.warning(
            "%s, %s, %s, %s, %s",
            self._seed,
            turn_count,
            winner,
            self._players,
            self._card_log,
        )

        return (turn_count, winner)
