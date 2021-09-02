"""Constants for Game."""
import logging
import random

from .const import (
    CONF_ASSIGNMENTS,
    CONF_BODY_LOCATIONS,
    CONF_DECK,
    CONF_IMPOSTER_CHANCES,
    CONF_POTENTIAL_ROOMS,
    CONF_REWARD_CREW_TO_BODY,
    CONF_REWARD_IMPOSTER_TO_CREW,
    CONF_RISK_CREW_TO_IMPOSTER,
    CONF_RISK_CREW_TO_RIVAL,
    CONF_SEED,
    DEFAULT_ASSIGNMENTS,
    DEFAULT_IMPOSTER_CHANCES,
    DEFAULT_POTENTIAL_ROOMS,
    DEFAULT_REWARD_CREW_TO_BODY,
    DEFAULT_REWARD_IMPOSTER_TO_CREW,
    DEFAULT_RISK_CREW_TO_IMPOSTER,
    DEFAULT_RISK_CREW_TO_RIVAL,
    DEFAULT_ROOMS,
    WINNER_CREW,
    WINNER_CREW_TURNS,
    WINNER_IMPOSTER,
    WINNER_UNKNOWN,
)


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

    def __init__(
        self,
        config,
    ):
        """Initialize the Game."""
        self._card_log = []
        self._ghosts = []
        self._bodies = []
        self._game_over = False

        # Set Config settings
        self._config = config.copy()

        random.seed(self._config.get(CONF_SEED))

        assignments = self._config.get(CONF_ASSIGNMENTS)
        if assignments is None:
            assignments = DEFAULT_ASSIGNMENTS.copy()
            random.shuffle(assignments)
        self._players = get_players(assignments)

        self._deck = self._config.get(CONF_DECK)
        if self._deck is None:
            self._deck = DEFAULT_ROOMS.copy()
            random.shuffle(self._deck)

        # Set default values
        if self._config.get(CONF_POTENTIAL_ROOMS) is None:
            self._config[CONF_POTENTIAL_ROOMS] = DEFAULT_POTENTIAL_ROOMS

        if self._config.get(CONF_IMPOSTER_CHANCES) is None:
            self._config[CONF_IMPOSTER_CHANCES] = DEFAULT_IMPOSTER_CHANCES

        if self._config.get(CONF_REWARD_IMPOSTER_TO_CREW) is None:
            self._config[CONF_REWARD_IMPOSTER_TO_CREW] = DEFAULT_REWARD_IMPOSTER_TO_CREW

        if self._config.get(CONF_REWARD_CREW_TO_BODY) is None:
            self._config[CONF_REWARD_CREW_TO_BODY] = DEFAULT_REWARD_CREW_TO_BODY

        if self._config.get(CONF_RISK_CREW_TO_IMPOSTER) is None:
            self._config[CONF_RISK_CREW_TO_IMPOSTER] = DEFAULT_RISK_CREW_TO_IMPOSTER

        if self._config.get(CONF_RISK_CREW_TO_RIVAL) is None:
            self._config[CONF_RISK_CREW_TO_RIVAL] = DEFAULT_RISK_CREW_TO_RIVAL

        # Place Body
        body_locations = self._config.get(CONF_BODY_LOCATIONS)
        if body_locations is None:
            body_locations = [random.choice(self._deck)]

        for i, location in enumerate(body_locations):
            body = Player(f"Body{i}", "Body")
            self.move_to_room(body, location)
            self._bodies.append(body)

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
        return (
            len(
                [
                    player
                    for player in self._players
                    if player.assignment == "Imposter" and player.position == "Space"
                ]
            )
            > 0
        )

    def get_rivals_in_my_room(self, player):
        """Return rivals in same position of player."""
        rivals = []

        if player.position:
            for rival in self._players:
                if rival.name != player.name and rival.position == player.position:
                    rivals.append(rival)

            for body in self._bodies:
                if body.position == player.position:
                    rivals.append(body)

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
            self.kick_imposter_out()

    def take_action(self, player, is_entering):
        """Player takes action entering or leaving a room."""
        rivals = self.get_rivals_in_my_room(player)
        if len(rivals) > 0:
            if player.is_imposter():
                for rival in rivals:
                    if rival.name not in [body.name for body in self._bodies]:
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
                    if rival.name in [
                        body.name for body in self._bodies
                    ] and self.is_alive(player):
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
            room_risk = room_risk + self._config.get(CONF_RISK_CREW_TO_IMPOSTER)
        if len(self._ghosts) == 0 and player_in_room:
            room_risk = room_risk + self._config.get(CONF_RISK_CREW_TO_RIVAL)

        return room_risk

    def rate_room_reward(self, player, room):
        """Rate the room reward score."""
        room_reward = 0

        if player.assignment == "Imposter":
            for rival in self.players:
                if rival != player and rival.position == room:
                    room_reward = room_reward + self._config.get(
                        CONF_REWARD_IMPOSTER_TO_CREW
                    )

        if player.assignment == "Crew":
            for body in self._bodies:
                if body.position == room:
                    room_reward = room_reward + self._config.get(
                        CONF_REWARD_CREW_TO_BODY
                    )

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
        if room in self._config.get(CONF_POTENTIAL_ROOMS):
            potential_rooms = [
                f"{room}.{x}"
                for x in range(self._config.get(CONF_POTENTIAL_ROOMS)[room])
            ]
            ideal_room = self.find_optimal_room(player, potential_rooms)
            player.position = ideal_room
        else:
            player.position = room

    def reshuffle_deck(self):
        """Reshuffle the deck."""
        self._deck = DEFAULT_ROOMS.copy()
        random.shuffle(self._deck)

    def calculate_winner(self, turn_count, imposter_reveal_turn):
        """Determine winner of simulation."""
        if self.is_imposter_kicked_out():
            return WINNER_CREW

        if turn_count + 1 == imposter_reveal_turn:
            return WINNER_CREW_TURNS

        if len(self._players) == (len(self._ghosts) + 1):
            return WINNER_IMPOSTER

        return WINNER_UNKNOWN

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
                    imposter_reveal_turn = (
                        turn_count + self._config.get(CONF_IMPOSTER_CHANCES) + 1
                    )
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

        logging.info(
            "%s, %s, %s, %s, %s",
            self._config.get(CONF_SEED),
            turn_count,
            winner,
            self._players,
            self._card_log,
        )

        return (turn_count, winner)
