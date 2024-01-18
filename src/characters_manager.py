import logging
import src.character_manager as character_manager # Character class
import src.utils as utils
class Characters:
    def __init__(self, conversation_manager):
        self.active_characters = {}
        self.conversation_manager = conversation_manager

    @property
    def active_characters_list(self): # Returns a list of all active characters
        characters = []
        for character in self.active_characters:
            characters.append(self.active_characters[character])
        return characters
    
    @property
    def bios(self): # Returns a paragraph comprised of all active characters bios
        bios = ""
        for character in self.active_characters_list:
            bios += character.bio
            if character != self.active_characters_list[-1]:
                bios += "\n\n"
        logging.info("Active Bios: " + bios)
        return bios
    
    @property
    def names(self): # Returns a list of all active characters names
        return [character.name for character in self.active_characters_list]
    
    @property
    def names_w_player(self): # Returns a list of all active characters names with the player's name included
        names = self.names
        names.append(self.conversation_manager.player_name)
        return names
    
    @property
    def relationship_summary(self): # Returns a paragraph comprised of all active characters relationship summaries
        if len(self.active_characters) == 0:
            logging.warning("No active characters, returning empty relationship summary")
            return ""
        if len(self.active_characters) == 1:
            logging.info("Only one active character, returning SingleNPC style relationship summary")
            perspective_player_name, perspective_player_description, trust = self.active_characters_list[0].get_perspective_player_identity()
            relationship_summary = perspective_player_description
        else:
            logging.info("Multiple active characters, returning MultiNPC style relationship summary")
            relationship_summary = ""
            for character in self.active_characters_list:
                perspective_player_name, perspective_player_description, trust = character.get_perspective_player_identity()
                relationship_summary += perspective_player_description
                if character != self.active_characters_list[-1]:
                    relationship_summary += "\n\n"
        logging.info("Active Relationship Summary: " + relationship_summary)
        return relationship_summary

    @property
    def replacement_dict(self): # Returns a dictionary of replacement values for the current context -- Dynamic Variables
        time_group = utils.get_time_group(self.conversation_manager.current_in_game_time) # get time group from in-game time before 12/24 hour conversion
        time = f"{self.conversation_manager.current_in_game_time}"
        ampm = None
        if self.conversation_manager.current_in_game_time <= 12:
            ampm = "AM"
        elif time > 12:
            time = f"{self.conversation_manager.current_in_game_time-12}" # Convert to 12 hour time because asking the AI to convert to 12 hour time is unreliable. Example: half the time they say 15 in the afternoon instead of 3pm.
            ampm = "PM"
        if len(self.active_characters) == 1: # SingleNPC style context
            replacement_dict = self.active_characters_list[0].replacement_dict
        else: # MultiNPC style context
            replacement_dict = {
                "conversation_summaries": self.get_conversation_summaries(),
                "names": self.names,
                "relationship_summary": self.relationship_summary,
            }
        replacement_dict["names_w_player"] = self.names_w_player
        replacement_dict["time"] = self.conversation_manager.current_in_game_time
        replacement_dict["ampm"] = ampm
        replacement_dict["time_group"] = time_group
        replacement_dict["location"] = self.conversation_manager.current_location
        replacement_dict["player_name"] = self.conversation_manager.player_name
        replacement_dict["player_race"] = self.conversation_manager.player_race
        replacement_dict["player_gender"] = self.conversation_manager.player_gender
        replacement_dict["behavior_summary"] = self.conversation_manager.behavior_manager.get_behavior_summary()
        replacement_dict["language"] = self.conversation_manager.language_info['language']

        return replacement_dict

    def active_character_count(self): # Returns the number of active characters as an int
        return len(self.active_characters)
    
    def get_raw_prompt(self):
        if len(self.active_characters) == 1:
            logging.info("Only one active character, returning SingleNPC style context")
            prompt = self.conversation_manager.config.single_npc_prompt
        else:
            logging.info("Multiple active characters, returning MultiNPC style context")
            prompt = self.conversation_manager.config.multi_npc_prompt
        return prompt

    def get_system_prompt(self): # Returns the current context for the given active characters as a string
        if len(self.active_characters) == 0:
            logging.warning("No active characters, returning empty context")
            return ""

        prompt = self.get_raw_prompt()

        system_prompt = prompt.format(**self.replacement_dict)
        # logging.info("System Prompt: " + system_prompt)
        return system_prompt

    def get_character(self, info, is_generic_npc=False):
        character = character_manager.Character(self, info, is_generic_npc)
        return character