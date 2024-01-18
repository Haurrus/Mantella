import logging
import src.behaviors.base_behavior as base_behavior

class offended(base_behavior.BaseBehavior):
    def __init__(self, manager):
        super().__init__(manager)
        self.keyword = "Offended"
        self.description = "If {player} says something hurtful / offensive, begin your response with 'Offended:'."
        self.example = "'Have you washed lately?' 'Offended: How dare you!'"
    
    def run(self, run=False):
        if run:
            logging.info(f"The player offended the NPC")
            self.manager.conversation_manager.game_state_manager.write_game_info('_mantella_aggro', '1')
        return "offended"
        