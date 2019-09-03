'''
The Witch's Cat
Original Prompt: Text-based Adventure Game

TODO:
- what to render if healing exceeds max hp? this is already handled in process, but not reflected in render.
- reintroduce -5 HP penalty for "keep walking"
- descriptions for items?
- view skills, view inventory
'''

# notes for dist: must have python3 and colorama installed
import pickle, os, time, colorama
from witchcattext import *
from colorama import Fore, Style
    
def find(keyword, ls):
    '''
    Consumes an keyword, matches it to its Object (either an Item, Skill, or an Opponent) from a list,
    and returns the Object whose name attribute matches the keyword.
        Args:
            keyword (String): the name of the Object
            ls ([]): the list of Objects to search
        Returns:
            Object: the Item, Skill, or Opponent whose name matches keyword.
    '''
    for obj in ls:
        if keyword == obj.name:
            return obj
    return None
        
def calcDMG(hp, amount):
    '''
    Consumes a number and subtracts it from hp, not dropping below zero. Returns the result.
        Args:
            hp(Int): the quantity to be subtracted from.
            amount(Int): the amount to be subtracted from hp.
        Returns:
            Int: the end result.
    '''
    if hp - amount > 0:
        return hp - amount
    else:
        return 0
    
def listsaves():
    '''
    Consumes nothing and returns a string displaying the names and timestamps of save files.
        Args:
            None
        Returns:
            str: formatted names and last modified time of the save files in the current directory
    '''
    output = ""
    names = []
    timestamps = []
    with os.scandir() as files:
        for f in files:
            if f.name[-2:] == ".p":
                names.append(f.name[:-2])
                timestamps.append(os.path.getmtime(f.name))
    if len(names) > 0:
        output += "\nSaved games:"
    i = 0
    while(i < len(names)):
        output += "\n{}  {:>12}".format(names[i], "(last saved " + time.ctime(timestamps[i]) + ")")
        i += 1
    return output

class Skill:
    '''
    Attributes:
        name (String): The name of the skill.
        power (Int): The damage dealt by the skill.
    '''
    def __init__(self, skill_name, skill_power):
        self.name = skill_name
        self.power = skill_power
    
    def __repr__(self):
        '''
        Consumes nothing and produces a String representing the skill.
            Args:
                self (Skill): the instance of Skill.
            Returns:
                str: the String to be printed.
        '''
        return str(vars(self))
    

# Obtainable by Player
SCRATCH = Skill("SCRATCH", 10)
ETERNAL_NIGHT = Skill("ETERNAL NIGHT", 30)
HEAL = Skill("HEAL", 50) # heal CANNOT damage, but instead replenishes 50 hp
SKY_BLESSING = Skill("SKY\'S BLESSING", 50)
RAIN = Skill("RAIN", 70)

# Not Obtainable by Player, but I felt like keeping 'em in. Easter eggs? Future plans?
BITE = Skill("BITE", 20)
HAUNT = Skill("HAUNT", 100)

class Item:
    '''
    Attributes:
        name (String): The name of this item.
        damage (Int): The multiplier of the damage dealt to the opponent's hp.
        defense (Int): The multiplier of the damage dealt by an opponent (between 0 and 1).
        healing (Int): The amount by which this item adds to the player's hp.
    '''
    def __init__(self, item_name, dmg, dfns, heal):
        self.name = item_name
        self.damage = dmg
        self.defense = dfns
        self.healing = heal
        
    def __repr__(self):
        '''
        Consumes nothing and produces a String representing the item.
            Args:
                self (Item): the instance of Item.
            Returns:
                str: the String to be printed.
        '''
        return str(vars(self))
        
HAT = Item("WITCH\'S HAT", 0, 0, 0)
PEARL = Item("PEARL OF PROTECTION", 0, 5, 0)
# BACKPACK: isn't actually an item, but sets backpack_status to True
HEART = Item("HEART OF DARKNESS", 5, 0, 0)
HERBS = Item("HERBS", 0, 0, 5)
DOLL = Item("CAT DOLL", 0, 0, 0)
TUNA = Item("CAN OF TUNA", 2, 2, 2)
SWORD = Item("ENERGY SWORD", 20, 0, 0)

ITEMS = [HAT, PEARL, HEART, HERBS, DOLL, TUNA, SWORD]
# all items that can be possibly be collected in the world
# this is a global CONSTANT for the sake of convienience

class Inventory:
    '''
    Attributes:
        backpack_status (Boolean): Whether this inventory is a backpack.
        items (Item[]): The item(s) in the inventory. 
                        If the inventory is not a backpack, there can only be one item in the inventory at a time.            
                        Otherwise, storage is unlimited.
        equipped (Item): The item that is currently equipped.
    '''
    def __init__(self, pack_status, some_items, equip):
        self.backpack_status = pack_status
        self.items = some_items
        self.equipped = equip
        
    def __repr__(self):
        '''
        Consumes nothing and produces a String representing the inventory.
            Args:
                self (Inventory): the instance of Inventory.
            Returns:
                str: the String to be printed.
        '''
        return str(vars(self))
        

class Player:
    '''
    Attributes:
        location (String): The player's current location.
        skills (Skill[]): The player's skills.
        last_used (Skill): The last skill the player used.
        hp (Int): The player's health points.
        inventory (Inventory): The player’s inventory.
        pawprints (dict str:bool): Keeps track of whether player has made a choice with respect
                                   to a character that is crucial to the narrative (CRYING GIRL not included),
                                   influencing the ending they get
    '''
    PLAYER_MAX_HP = 100
    
    def __init__(self, the_location, some_skills, the_inventory):
        self.location = the_location
        self.skills = some_skills
        self.last_used = None
        self.hp = self.PLAYER_MAX_HP
        self.inventory = the_inventory
        self.pawprints = {"CHURCH GRIM":False, "BAT":False, "CROW":False, "GHOST CAT":False}
                
    def addToHP(self, amount):
        '''
        Consumes an amount of hp and adds that amount to the player's hp, not exceeding the maximum.
            Args:
                self(Player): the instance of Player.
                amount(Int): the amount of hp to be added.
            Returns:
                None
        '''
        if amount + self.hp < self.PLAYER_MAX_HP:
            self.hp = self.hp + amount
        else:
            self.hp = self.PLAYER_MAX_HP
            
    def __repr__(self):
        '''
        Consumes nothing and produces a String representing the player.
            Args:
                self (Player): the instance of Player.
            Returns:
                str: the String to be printed.
        '''
        return str(vars(self))
        
        
class Opponent:
    '''
    Attributes:
        name (String): The name of the opponent.
        hp (Int): The opponent's hp.
        maxhp (Int): The opponent's maximum hp.
        skills (Skill[]): The opponent’s skills.
        desc (String): The personalized line that appears during battle.
    '''
    def __init__(self, op_name, op_health, op_max, op_skills, op_desc):
        self.name = op_name
        self.hp = op_health
        self.maxhp = op_max
        self.skills = op_skills
        self.desc = op_desc
        
    def addToHP(self, amount):
        '''
        Consumes an amount of hp and adds that amount to the opponent's hp, not exceeding the maximum.
            Args:
                self(Opponent): the instance of Opponent.
                amount(Int): the amount of hp to be added.
            Returns:
                None
        '''
        if amount + self.hp < self.maxhp:
            self.hp = self.hp + amount
        else:
            self.hp = self.maxhp

# CHARACTERS = [GRIM, BAT, CROW, GIRL, GHOST]
# the names of all CHARACTERS that can possibily be encountered in the world
# only here for reference


SPECIAL_COMMANDS = ["I will help you", "Keep walking",
                    "I don't want to hurt you", "Give cat doll", "I'm sorry"] # "good" choices
BATTLE_COMMANDS = ["You are trying to trick me", "Fight your way through",
                   "I am pretty hungry", "Hiss", "Let me through"] # "bad" choices

LOCATIONS = ["alley", "graveyard", "cave", "field", "road", "porch"]
# global constant: for processing user input to go to a new location


class World:
    '''
    Attributes:
        player (Player): The player character's information
        game_status (String): The current state of the game: either
                              "playing", "tutorial", "encounter", "battle", "won", "lost", or "quit".
        encounters (String[]): The names of the characters that have been interacted with.
        opponents (Opponent[]): The list of opponents that have been engaged in battle.
    '''
    
    def __init__(self):
        self.player = Player("alley", [SCRATCH], Inventory(False, [HAT], HAT))
        self.game_status = "playing"
        self.encounters = []
        self.opponents = []
        
    def update(self, new_player, new_status, new_encounters, new_opponents):
        '''
        Consumes self and the new attributes of the World and updates the World, returning nothing.
            Args:
                self (World): the current instance of World.
                new_player (Player): the updated instance of Player.
                new_status (str): the updated game status.
                new_encounters (String[]): the updated encounters list.
                new_opponents (Opponent[]): the updated opponents list.
            Returns:
                None
        '''
        self.player = new_player
        self.game_status = new_status
        self.encounters = new_encounters
        self.opponents = new_opponents
        
    def save(self):
        '''
        Consumes self and saves the game based on user input, returning nothing.
            Args:
                self (World): the instance of World.
            Returns:
                None
        '''
        name = input("\nWhat will the name of this saved game be? ")
        if name in listsaves():
            if not (input("This file will be overwritten. Is that ok? [y/n] ").lower() == "y"):
                return
        save_game = open(name + ".p", "wb")
        pickle.dump(self, save_game)
        print("\nSave Successful.")
        
    def load(self):
        '''
        Consumes self and loads the game based on user input, returning nothing.
        Args:
            self (World): the instance of World.
        Returns:
            None
        '''
        print(listsaves())
        name = input("\nPlease enter the name of your saved game: ")
        try:
            load_game = open(name + ".p", "rb")
            load_world = pickle.load(load_game)
            self.update(load_world.player, load_world.game_status, load_world.encounters, load_world.opponents)
            load_game.close()
            print("\nLoad Successful.")
        except(FileNotFoundError):
            print("\nSave file not found.")
            
    def is_done(self):
        '''
        Consumes nothing and returns a Boolean indicating whether the game should end.
            Args:
                self (World): the instance of World.
            Returns:
                bool: True if the game should end
        '''
        return self.game_status in ["won", "lost", "quit"]
        
    def is_good(self):
        '''
        Consumes nothing and returns a Boolean indicating whether the world state is valid.
            Args:
                self (World): the instance of World.
            Returns:
                bool: True if world state is valid.
        '''
        return True
    
    def battle_message(self):
        '''
        Consumes nothing and returns a personalized String depending on whether
        the battle has just started or is currently in progress.
            Args:
                self (World): the instance of World.
            Returns:
                str: the String to be passed to render_battle.
        '''
        current_opponent = self.opponents[-1]
        player_msg = ""
        
        if isinstance(self.player.last_used, Skill):
            current_equipped = self.player.inventory.equipped
            if self.player.last_used == HEAL:
                player_msg += "\nYou use HEAL and recovered " + str(HEAL.power) + " hp."
            else:
                player_msg += ("\nYou use " + self.player.last_used.name + " and deal "
                            + str(self.player.last_used.power + current_equipped.damage)
                            + " damage to " + current_opponent.name + "!")
            if current_equipped.healing > 0:
                player_msg += "\nYou recover " + str(current_equipped.healing) + " hp from your " + current_equipped.name + "."
            
            if current_opponent.name == "BAT":
                op_msg = "BAT uses HEAL and recovers " + str(HEAL.power) + " hp."
            elif current_opponent.name == "PUMPKIN":
                op_msg = "PUMPKIN stares at you blankly and deals 0 damage to you."
            # these two have unique behavior
            else:
                opponent_skill = current_opponent.skills[0]
                op_msg = (current_opponent.name + " uses " + opponent_skill.name + " and deals "
                        + str(opponent_skill.power - current_equipped.defense) + " damage to you.")
                
            return "\n" + player_msg + "\n" + op_msg + "\n"
        else:
            return "\nYou have entered battle with " + current_opponent.name + ".\n"
        
    def locate_chara(self):
        '''
        Consumes nothing and returns a string representing the name of the character
        that should be encountered at the current location.
            Args:
                self (World): the instance of World.
            Returns:
                str: the name of a character.
        '''
        loc = self.player.location
        
        if loc == "alley":
            return ""
        elif loc == "graveyard":
            return "CHURCH GRIM"
        elif loc == "cave":
            return "BAT"
        elif loc == "field":
            return "CROW"
        elif loc == "road":
            return "GHOST CAT"
        else: # porch
            return "CRYING GIRL"
        
    def check_chara(self, chara_name):
        '''
        Consumes a character name and returns a Boolean that depends on whether
        the user's attempt to talk to a character at a location is valid.
            Args:
                self(World): the instance of World.
                chara_name(str): the user's input.
            Returns:
                bool: True if the character talk option is accessible.
        '''
        loc = self.player.location
        final_enc_invalid = (loc == "road" and len(self.encounters) < 4 and "CRYING GIRL" not in self.encounters)
        
        if chara_name != "" and chara_name not in self.encounters and self.locate_chara() == chara_name:
            if not final_enc_invalid:
                return True
        return False
        
    def render_post_battle(self):
        '''
        Consumes nothing and returns the string for the user to read after a battle.
            Args:
                self (World): the instance of World.
            Returns:
                str: the string to be passed to render.
        '''
        chara_name = self.encounters[-1]
        
        if self.locate_chara() != chara_name:
            return ""
        if chara_name == "CRYING GIRL": # note: no actual battle takes place
            return GIRL_OUTCOME
        
        loc = self.player.location
        opponent_name = self.opponents[-1].name
        
        if loc == "graveyard":
            if opponent_name == "CHURCH GRIM":
                return GRIM_OUTCOME
            else:
                return PUMPKIN_OUTCOME
        elif loc == "cave":
            if opponent_name == "BAT":
                return BAT_OUTCOME
            else:
                return MONSTER_OUTCOME
        else: # field: same render, but ultimately different results in the ending.
            return CROW_OUTCOME
    
    def render_battle(self):
        '''
        Consumes nothing and returns a String to print to the console during battle mode.
            Args:
                self (World): the instance of World.
            Returns:
                str: the text to be passed to render.
        '''
        if self.game_status == "tutorial":
            return README
        current_opponent = self.opponents[-1]
        return (self.battle_message() + "\nYOUR HP: " + str(self.player.hp) + "\n" + current_opponent.name
                + "'S HP: " + str(current_opponent.hp) + "\n" + current_opponent.desc)
    
        
    def list_options(self, items, chara_name):
        '''
        Consumes a list of Items and an Opponent and returns a String of player options.
            Args:
                self (World): the instance of World.
                items (Item[]): the list of Items that can potentially be picked up.
                chara (Opponent): the opponent that can potentially be encountered.
            Returns:
                str: the text to be passed to render_location.
        '''
        options = ""
        message = "\nCurrently, you have " + self.player.inventory.equipped.name + " equipped."
        inv = self.player.inventory
        itemnames = []
        
        for item in inv.items:
            itemnames.append(item.name)
            
        backpack = inv.backpack_status
        loc = self.player.location
        final_enc_invalid = (loc == "road" and len(self.encounters) < 4 and "CRYING GIRL" not in self.encounters)
        if loc == "graveyard":
            if not backpack:
                options += "\nPick up backpack"
            else:
                message += "\nYou have picked up the magic backpack, which allows you to store any number of items!"
        for item in items:
            if backpack and item.name not in itemnames:
                options += ("\nPick up " + item.name)
            if item in inv.items:
                message += ("\nYou have picked up " + item.name + ", which offers " + str(item.damage)
                            + " damage, " + str(item.defense) + " defense, and " + str(item.healing) + " healing.")
        if chara_name != "" and chara_name not in self.encounters:
            if not final_enc_invalid:
                options += ("\nTalk to " + chara_name)
        
        return options + "\n" + message
            
    def render_location(self):
        '''
        Consumes nothing and returns a String to print to the console based on the current location.
            Args:
                self (World): the instance of World.
            Returns:
                str: the text to be passed to render.
        '''
        loc = self.player.location
        if len(self.opponents) > 0:
            msg = self.render_post_battle() + "\n"
        else:
            msg = ""
            
        if loc == "alley":
            msg += ALLEY_PROMPT + self.list_options([PEARL], "")
        
        elif loc == "graveyard":
            msg += GRAVEYARD_PROMPT + self.list_options([], "CHURCH GRIM")
        
        elif loc == "cave":
            msg += CAVE_PROMPT + self.list_options([HEART], "BAT")
        
        elif loc == "field":
            msg += FIELD_PROMPT + self.list_options([HERBS], "CROW")
        
        elif loc == "road":
            msg += ROAD_PROMPT + self.list_options([DOLL, SWORD], "GHOST CAT")
        
        elif loc == "porch":
            msg += PORCH_PROMPT + self.list_options([TUNA], "CRYING GIRL")
            
        else:
            msg += "\nError. Please let Pine know!"
            
        return msg
        
    def render_dialogue(self):
        '''
        Consumes nothing and returns a String to print to the console when dialogue
        between the player and a character is taking place, including options.
            Args:
                self (World): the instance of World.
            Returns:
                str: the text to be passed to render.
        '''
        chara_name = self.encounters[-1]
        if chara_name == "CHURCH GRIM":
            return GRIM_DIAG + SPECIAL_COMMANDS[0] + "\n" + BATTLE_COMMANDS[0]
        elif chara_name == "BAT":
            return BAT_DIAG + SPECIAL_COMMANDS[1] + "\n" + BATTLE_COMMANDS[1]
        elif chara_name == "CROW":
            return CROW_DIAG + SPECIAL_COMMANDS[2] + "\n" + BATTLE_COMMANDS[2]
        elif chara_name == "CRYING GIRL":
            if find("CAT DOLL", self.player.inventory.items):
                return GIRL_DIAG + SPECIAL_COMMANDS[3] + "\n" + BATTLE_COMMANDS[3]
            else:
                return GIRL_DIAG + "Back\n" + BATTLE_COMMANDS[3]
        else: # GHOST CAT
            return GHOST_DIAG + SPECIAL_COMMANDS[4] + "\n" + BATTLE_COMMANDS[4]
        
    def render(self):
        '''
        Consumes nothing and returns a String to print to the console.
            Args:
                self (World): the instance of World.
            Returns:
                str: the text to be printed to the console.
        '''
        if self.game_status == "battle":
            return self.render_battle()
        elif self.game_status == "tutorial":
            return README
        else:
            if self.game_status == "encounter":
                return self.render_dialogue()
            else:
                return self.render_location()
            
            
    def check_location_items(self, location, usr_input, itemnames):
        '''
        Consumes a location, user input, and a list of item names and produces a boolean
        depending on whether the user input matches one of the item names.
            Args:
                self(World): the instance of World.
                location(str): the location being tested.
                usr_input(str): the input being tested.
                itemnames(str[]): the list being looked through.
            Returns:
                bool: True if the usr_input == one of the itemnames.
        '''
        if self.player.location == location:
            if usr_input in itemnames:
                return True
        return False
    
    def check_locations(self, location, usr_input, other_locations):
        '''
        Consumes a location, user input, and a list of available locations and produces a boolean
        depending on whether the user input matches one of the locations.
            Args:
                self(World): the instance of World.
                location(str): the location being tested.
                usr_input(str): the input being tested.
                other_locations(str[]): the list being looked through.
            Returns:
                bool: True if the usr_input == one of the locations.
        '''
        if self.player.location == location:
            if usr_input in other_locations:
                return True
        return False
    
    def item_scan(self, usr_input):
        '''
        Consumes a user input and produces a boolean.
            Args:
                self(World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                bool: True if player picks up an item in the right location.
        '''
        itemname = usr_input.upper()[8:]
        if self.check_location_items("alley", itemname, ["PEARL OF PROTECTION"]):
            return True
        elif not self.player.inventory.backpack_status and self.check_location_items("graveyard", itemname, ["BACKPACK"]):
            return True
        elif self.check_location_items("cave", itemname, ["HEART OF DARKNESS"]):
            return True
        elif self.check_location_items("field", itemname, ["HERBS"]):
            return True
        elif self.check_location_items("road", itemname, ["CAT DOLL", "ENERGY SWORD"]):
            return True
        elif self.check_location_items("porch", itemname, ["CAN OF TUNA"]):
            return True
        else:
            return False
            
    def location_scan(self, usr_input):
        '''
        Consumes a user input and produces a boolean.
            Args:
                self(World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                bool: True if player inputs a location that can be accessed from the current one.
        '''
        inpt = usr_input.lower()
        if self.check_locations("alley", inpt, ["graveyard"]):
            return True
        elif self.check_locations("graveyard", inpt, ["alley", "field", "cave"]):
            return True
        elif self.check_locations("cave", inpt, ["graveyard"]):
            return True
        elif self.check_locations("field", inpt, ["graveyard", "road"]):
            return True
        elif self.check_locations("road", inpt, ["field", "porch"]):
            return True
        elif self.check_locations("porch", inpt, ["road"]):
            return True
        else:
            return False
        
    
    def is_input_good(self, usr_input):
        '''
        Consumes a String (the user's input) and produces a Boolean on validity of input.
            Args:
                self (World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                bool: True if the user's input is valid.
        '''
        inpt = usr_input.lower()
        options = ["quit", "help", "save", "load"]
        
        if self.game_status == "battle": # Use SKILLNAME
            if isinstance(find(inpt[4:].upper(), self.player.skills), Skill):
                return True
            elif inpt in options:
                return True
            else:
                return False
        else:
            if inpt in options:
                return True
            
            if inpt.startswith("pick up"):
                if self.player.inventory.backpack_status or inpt == "pick up backpack":
                    return self.item_scan(inpt)
                else:
                    return False
            
            if inpt.startswith("equip"):
                for item in self.player.inventory.items:
                    if usr_input.upper()[6:] == item.name:
                        return True
                return False
            
            if inpt.startswith("talk to"):
                return self.check_chara(inpt[8:].upper())
            
            if inpt.startswith("give"):
                return DOLL in self.player.inventory.items
            
            if inpt.capitalize() in BATTLE_COMMANDS or inpt.capitalize() in SPECIAL_COMMANDS:
                return True
            if inpt == "back" and self.player.location == "porch" and self.encounters[-1] == "CRYING GIRL":
                return True
            
            return self.location_scan(inpt)
        
        
    def get_opponent(self, name):
        '''
        Consumes the name of the opponent and returns the Opponent object.
            Args:
                self (World): the instance of World.
                name(str): the name of the Opponent to be created.
            Returns:
                Opponent: the Opponent object that is created to to correspond with name.
        '''
        if name == "CHURCH GRIM":
            return Opponent(name, 20, 20, [BITE], "CHURCH GRIM looks like he's about to cry...")
        elif name == "PUMPKIN":
            return Opponent(name, 20, 20, [], "A strange aura exudes from PUMPKIN. A shudder runs down your spine...")
        elif name == "BAT":
            return Opponent(name, 30, 30, [HEAL], "BAT hovers calmly in place in front of you...")
        elif name == "CAVE MONSTER":
            return Opponent(name, 30, 30, [SCRATCH], "Saliva drips from CAVE MONSTER's fangs. It looks at you hungrily...")
        elif name == "CROW":
            return Opponent(name, 50, 50, [ETERNAL_NIGHT], "CROW hops around you and caws racously. It's really getting on your nerves...")
        else: # GHOST CAT
            return Opponent("GHOST CAT", 100, 100, [RAIN], "There is an incredible sadness in GHOST CAT's eyes...")
            
            
    def process_dialogue(self, usr_input):
        '''
        Consumes a String (the user's input) and updates the world state based on the dialogue choice.
            Args:
                self (World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                None
        '''
        chara_name = self.encounters[-1]
        self.game_status = "battle"
        cmd = usr_input.lower().capitalize()
        if cmd in BATTLE_COMMANDS:
            if cmd == "Hiss":
                self.game_status = "lost"
            else:
                self.opponents.append(self.get_opponent(chara_name))
        else:
            self.handle_special_response(cmd)
                
    def handle_special_response(self, cmd):
        '''
        Consumes a String and updates the world state based on the special dialogue choice.
            Args:
                self (World): the instance of World.
                cmd(str): user input tring modified by process_dialogue.
            Returns:
                None
        '''
        chara_name = self.encounters[-1]
        if chara_name in self.player.pawprints:
            self.player.pawprints[chara_name] = True
        if chara_name == "CHURCH GRIM":
            self.opponents.append(self.get_opponent("PUMPKIN"))
        elif chara_name == "BAT":
            self.opponents.append(self.get_opponent("CAVE MONSTER"))
        elif chara_name == "CRYING GIRL":
            if cmd == "Back":
                self.encounters.remove("CRYING GIRL")
                self.player.location = "porch"
            else:
                self.player.skills.append(RAIN)
            self.game_status = "playing"
            # no fight, no call to get_opponent--she is not an opponent
        else:
            self.opponents.append(self.get_opponent(chara_name))
                
    def get_skill(self, name):
        '''
        Consumes the name of an Opponent and returns the skill the player gets by defeating that opponent.
            Args:
                self (World): the instance of World.
                name(str): the name of the Opponent.
            Returns:
                Skill: the skill offered by the opponent.
        '''
        if name in ["CHURCH GRIM", "PUMPKIN"]:
            return ETERNAL_NIGHT
        elif name in ["BAT", "CAVE MONSTER"]:
            return HEAL
        else: # CROW
            return SKY_BLESSING
               
    def process_battle(self, usr_input):
        '''
        Consumes a String (the user's input) and updates the world state accordingly FOR BATTLE MODE.
            Args:
                self (World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                None
        '''
        inpt = usr_input.lower()
        if inpt == "quit":
            self.game_status = "quit"
            return
        if inpt == "help":
            self.game_status = "tutorial"
            return
        if inpt == "save":
            self.save()
            return
        if inpt == "load":
            self.load()
            return
        
        opponent = self.opponents[-1]
        
        self.player.last_used = find(usr_input[4:].upper(), self.player.skills)
        current_equipped = self.player.inventory.equipped
            
        self.player.addToHP(current_equipped.healing)
        if self.player.last_used == HEAL:
            self.player.addToHP(self.player.last_used.power)
        else:
            opponent.hp = calcDMG(opponent.hp, (self.player.last_used.power + current_equipped.damage))
                
        if opponent.hp == 0:
            if opponent.name == "GHOST CAT":
                self.game_status = "won"
            else:
                self.game_status = "playing"
                self.player.skills.append(self.get_skill(opponent.name))
                self.player.hp = self.player.PLAYER_MAX_HP
                self.player.last_used = None
        
    def process(self, usr_input):
        '''
        Consumes a String (the user's input) and updates the world state accordingly.
            Args:
                self (World): the instance of World.
                usr_input(str): the user's input.
            Returns:
                None
        '''
        
        inpt = usr_input.lower()
        
        if self.game_status == "battle":
            self.process_battle(usr_input)
            return
        elif inpt == "quit":
            self.game_status = "quit"
        elif inpt == "help":
            self.game_status = "tutorial"
        elif inpt == "save":
            self.save()
        elif inpt == "load":
            self.load()
        else:
            if self.game_status == "tutorial":
                self.game_status = "playing"
            
            inv = self.player.inventory
            
            if inpt.startswith("pick up"):
                if usr_input.upper()[8:] == "BACKPACK":
                    inv.backpack_status = True
                else:
                    inv.items.append(find(usr_input.upper()[8:], ITEMS))
                    
            elif inpt.startswith("equip"):
                inv.equipped = find(usr_input.upper()[6:], inv.items)
                
            elif inpt.startswith("talk to"):
                self.encounters.append(usr_input.upper()[8:])
                self.game_status = "encounter"
                
            elif inpt in LOCATIONS:
                self.player.location = inpt
                
            else:
                self.process_dialogue(inpt)
    
    def tick(self):
        '''
        Updates the world state without direct user input.
            Args:
                self (World): the instance of World.
            Returns:
                None
        '''
        # use for enemy turns in battle
        if self.game_status == "battle":
            current_opponent = self.opponents[-1]
            if current_opponent.hp == 0:
                return
            if not isinstance(self.player.last_used, Skill):
                return
            if current_opponent.skills == []:
                return
            current_equipped = self.player.inventory.equipped
            if current_opponent.name == "BAT":
                self.opponents[-1].addToHP(current_opponent.skills[0].power)
            else:
                self.player.hp = calcDMG(self.player.hp, (current_opponent.skills[0].power - current_equipped.defense))
            if self.player.hp == 0:
                self.game_status = "lost"
    
    def render_start(self):
        '''
        Consumes nothing and produces a String to initially print to the console for the beginning of the game.
           Args:
               self (World): the instance of World.
           Returns:
               str: the String to be printed.
        '''
        return "The Witch's Cat by Emma Adelmann\nType HELP for controls.\n"
    
    def render_bad_end(self):
        '''
        Consumes nothing and produces a String to render one of two bad endings.
            Args:
                self (World): the instance of World.
            Returns:
                str: the String to be passed to render_ending.
        '''
        if self.player.hp == 0:
            return self.battle_message() + DEFEAT_END
        else:
            return MISTAKES_END

    def render_good_end(self):
        '''
        Consumes nothing and produces a String to render one of the "good" endings
        depending on the values in opponents.
            Args:
                self (World): the instance of World.
            Returns:
                str: the String to be passed to render_ending.
        '''
        endgame = self.player.pawprints
        trueend = {"CHURCH GRIM": True, "BAT": True, "CROW": True, "GHOST CAT": True}
        
        # True Ending
        if endgame == trueend:
            return TRUE_END
        
        # Tier I Endings
        elif endgame["CHURCH GRIM"] and endgame["BAT"]:
            return RECLUSE_END
        elif endgame["CHURCH GRIM"] and endgame["CROW"]:
            return LIGHTNING_END
        elif endgame["CHURCH GRIM"] and endgame["GHOST CAT"]:
            return GRAVE_END
        elif endgame["BAT"] and endgame["CROW"]:
            return WING_END
        elif endgame["BAT"] and endgame["GHOST CAT"]:
            return DARK_END
        elif endgame["CROW"] and endgame["GHOST CAT"]:
            return ICARUS_END
        
        # Tier II Endings
        elif endgame["GHOST CAT"]:
            return RAIN_END
        elif endgame["CHURCH GRIM"]:
            return GUARDIAN_END
        elif endgame["BAT"]:
            return DEPTHS_END
        elif endgame["CROW"]:
            return WIND_END
        else:
            return REJECTION_END

    def render_ending(self):
        '''
        Consumes nothing and produces a String to render the ending.
            Args:
                self (World): the instance of World.
            Returns:
                str: the String to be printed.
        '''
        if self.game_status == "quit":
            return "\nThanks for playing The Witch's Cat! Hope you come back soon!"
        elif self.game_status == "won":
            return self.render_good_end()
        else:
            return self.render_bad_end()
            
    def __repr__(self):
        '''
        Consumes nothing and produces a String representing the world.
            Args:
                self (World): the instance of World.
            Returns:
                str: the String to be printed.
        '''
        return str(vars(self))
 

# Command Paths to give to the unit tester
WIN_PATH = ["graveyard", "pick up backpack", "talk to church grim", "i will help you",
            "use scratch", "use scratch", "cave", "talk to bat", "keep walking",
            "use eternal night", "graveyard", "field", "talk to crow", "i don't want to hurt you",
            "use eternal night", "use eternal night", "road", "pick up cat doll",
            "porch", "talk to crying girl", "give cat doll", "road", "talk to ghost cat",
            "i'm sorry", "use rain", "use eternal night"]
LOSE_PATH = ["graveyard", "talk to church grim", "you are trying to trick me",
             "use scratch", "use scratch", "cave", "talk to bat", "fight your way through",
             "use eternal night", "graveyard", "field", "talk to crow", "i am pretty hungry",
             "use eternal night", "use eternal night", "road", "porch", "hiss"]

def main():
    colorama.init()
    world = World()
    print(world.render_start())
    while not world.is_done():
        if not world.is_good():
            raise ValueError("The world is in an invalid state.", world)
        print(world.render())
        is_input_good = False
        while not is_input_good:
            print(Fore.CYAN, end = '')
            user_input = input()
            print(Style.RESET_ALL)
            is_input_good = world.is_input_good(user_input)
        world.process(user_input)
        world.tick()
    print(world.render_ending())
    input("\nPress enter to close...")

if __name__ == "__main__":
    main()
