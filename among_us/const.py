"""Constants used in Among us board game simulator."""
CONF_ASSIGNMENTS = "assignments"
CONF_BODY_LOCATIONS = "body_locations"
CONF_DECK = "deck"
CONF_IMPOSTER_CHANCES = "imposter_chances"
CONF_POTENTIAL_ROOMS = "potential_rooms"
CONF_REWARD_CREW_TO_BODY = "reward_crew_to_body"
CONF_REWARD_IMPOSTER_TO_CREW = "reward_imposter_to_crew"
CONF_RISK_CREW_TO_IMPOSTER = "risk_crew_to_imposter"
CONF_RISK_CREW_TO_RIVAL = "risk_crew_to_rival"
CONF_SEED = "seed"


DEFAULT_PLAYERS = ["Player 1", "Player 2", "Player 3", "Player 4"]
DEFAULT_ASSIGNMENTS = ["Crew", "Crew", "Crew", "Imposter"]
DEFAULT_ROOMS = [
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

DEFAULT_POTENTIAL_ROOMS = {"Bedroom": 3, "Bathroom": 2}
DEFAULT_IMPOSTER_CHANCES = 5

DEFAULT_REWARD_IMPOSTER_TO_CREW = 10
DEFAULT_REWARD_CREW_TO_BODY = 1
DEFAULT_RISK_CREW_TO_IMPOSTER = 10
DEFAULT_RISK_CREW_TO_RIVAL = 5

# Genome Consts
VALID_GENOTYPE_LEN = 43
# Player Count is bitwise added from 0-15
# Base is 3 so values are 3-18
# index[0:4]
PLAYER_COUNT_0 = 0
PLAYER_COUNT_2 = 1
PLAYER_COUNT_4 = 2
PLAYER_COUNT_8 = 3

# Imposter is bitwise added from 0 to 7
# Base is 1 so values are 1-8
# index[4:7]
IMPOSTER_COUNT_0 = 4
IMPOSTER_COUNT_2 = 5
IMPOSTER_COUNT_4 = 6

# Body count is bitwise added from 0 to 7
# Base is 1 so values are 1-8
# index[7:10]
BODY_COUNT_0 = 7
BODY_COUNT_2 = 8
BODY_COUNT_4 = 9

# Room type count is bitwise from 0-7
# Describes the number of different types of rooms
# Base is 3 so values are 3-10
# index[10:13]
ROOM_TYPE_COUNT_0 = 10
ROOM_TYPE_COUNT_2 = 11
ROOM_TYPE_COUNT_4 = 12

# Card count by Room Type is the number of each room type in the deck
# is bitwise added from 0 to 15
# Base is 3 so values are 3-18
# index[13:17]
CARD_COUNT_BY_ROOM_0 = 13
CARD_COUNT_BY_ROOM_2 = 14
CARD_COUNT_BY_ROOM_4 = 15
CARD_COUNT_BY_ROOM_8 = 16

# Duplicate Rooms is Bitwise added from 0-7
# index[17:20]
DUPLICATE_ROOMS_0 = 17
DUPLICATE_ROOMS_2 = 18
DUPLICATE_ROOMS_4 = 19

# Duplicate Rooms Strategy is how the rooms are built and is Categorical.
# Default behavior is to build DUPLICATE_ROOM_STRATEGY_EQUAL  is Bitwise added from 0-15
# index[20:21]
DUPLICATE_ROOM_STRATEGY_EQUAL = (
    101  # All duplicate rooms will have the same number of rooms
)
DUPLICATE_ROOM_STRATEGY_LADDER = 20  # Duplicate Rooms will have growing number of room

# Duplicate room instensity determines the number of duplicate room is Bitwise added from 0-3
# Base is 1 so values are 1-4
# index[21:23]
DUPLICATE_ROOM_INTESITY_0 = 21
DUPLICATE_ROOM_INTESITY_2 = 22

# Imposter chances are bitwise added from 0-15.
# Base is 3 so values are 3-18
# index[23:27]
IMPOSTER_CHANCES_0 = 23
IMPOSTER_CHANCES_2 = 24
IMPOSTER_CHANCES_4 = 25
IMPOSTER_CHANCES_8 = 26

# Reward Imposter to Crew is bitwise added from 0 to 15
# index[27:31]
REWARD_IMPOSTER_TO_CREW_0 = 27
REWARD_IMPOSTER_TO_CREW_2 = 28
REWARD_IMPOSTER_TO_CREW_4 = 29
REWARD_IMPOSTER_TO_CREW_8 = 30

# Reward Crew to Body is bitwise added from 0 to 15
# index[31:34]
REWARD_CREW_TO_BODY_0 = 31
REWARD_CREW_TO_BODY_2 = 32
REWARD_CREW_TO_BODY_4 = 33
REWARD_CREW_TO_BODY_8 = 34

# Reward Crew to Imposter is bitwise added from 0 to 15
# index[35:39]
RISK_CREW_TO_IMPOSTER_0 = 35
RISK_CREW_TO_IMPOSTER_2 = 36
RISK_CREW_TO_IMPOSTER_4 = 37
RISK_CREW_TO_IMPOSTER_8 = 38

# Reward Crew to Rival is bitwise added from 0 to 15
# index[39:43]
RISK_CREW_TO_RIVAL_0 = 39
RISK_CREW_TO_RIVAL_2 = 40
RISK_CREW_TO_RIVAL_4 = 41
RISK_CREW_TO_RIVAL_8 = 42

# Other Invalid combinations
# Imposter Count Greater than or equal Players
# Body count greater than or equal to rooms
# Duplicate rooms can't be greater than room count

# fmt: off
ORIGINAL_GENOME = [
    1, 0, 0, 0,  # default 4 players
    0, 0, 0,  # default 1 imposter
    0, 0, 0,  # default 1 body
    0, 0, 1,  # 7 rooms
    0, 1, 0, 0,  # 5 cards per type (+1 for each duplicate intensity value)
    0, 1, 0,  # 2 duplicate rooms
    1,  # Use ladder
    1, 0,  # Default 2
    0, 1, 0, 0,  # 5 chances
    0, 1, 0, 1,  # 10 for reward
    1, 0, 0, 0,  # 1 for reward crew to body
    0, 1, 0, 1,  # 10 risk crew to imposter
    1, 0, 1, 0,  # 5 risk crew to rival
]
# fmt: on
