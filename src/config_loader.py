import configparser
import logging
import os
import sys

class ConfigLoader:
    def __init__(self, file_name='config.ini'):
        config = configparser.ConfigParser()
        config.read(file_name, encoding='utf-8')

        def invalid_path(set_path, tested_path):
            logging.error(f"\"{tested_path}\" does not exist!\n\nThe path set in config.ini: \"{set_path}\"")
            input('\nPress any key to exit...')
            sys.exit(0)

        def check_missing_mantella_file(set_path):
            try:
                with open(set_path+'/_mantella__skyrim_folder.txt') as f:
                    check = f.readline().strip()
            except:
                logging.warn(f'''
Warning: Could not find _mantella__skyrim_folder.txt in {set_path}. 
If you have not yet casted the Mantella spell in-game you can safely ignore this message. 
If you have casted the Mantella spell please check that your 
MantellaSoftware/config.ini "skyrim_folder" has been set correctly 
(instructions on how to set this up are in the config file itself).
If you are still having issues, a list of solutions can be found here: 
https://github.com/art-from-the-machine/Mantella#issues-qa
''')

        def run_config_editor():
            try:
                import src.config_editor as configeditor

                logging.info('Launching config editor...')
                configeditor.start()
                logging.info(f'Config editor closed. Re-reading {file_name} file...')

                config.read(file_name)
            except Exception as e:
                logging.error('Unable to run config editor!')
                raise e

        try:
            # [Startup]
            # run config editor if config.ini has the parameter
            if int(config['Startup']['open_config_editor']) == 1:
                run_config_editor()

            # [Paths]
            self.game_path = config['Paths']['skyrim_folder']
            self.xvasynth_path = config['Paths']['xvasynth_folder']
            self.mod_path = config['Paths']['mod_folder']
            self.character_df_file = config['Paths']['character_df_file']

            # [Language]
            self.language = config['Language']['language']
            self.end_conversation_keyword = config['Language']['end_conversation_keyword']
            self.goodbye_npc_response = config['Language']['goodbye_npc_response']
            self.collecting_thoughts_npc_response = config['Language']['collecting_thoughts_npc_response']
            self.offended_npc_response = config['Language']['offended_npc_response']
            self.forgiven_npc_response = config['Language']['forgiven_npc_response']
            self.follow_npc_response = config['Language']['follow_npc_response']

            # [Microphone]
            self.mic_enabled = config['Microphone']['microphone_enabled']
            self.whisper_model = config['Microphone']['model_size']
            self.stt_language = config['Microphone']['stt_language']
            if (self.stt_language == 'default'):
                self.stt_language = self.language
            self.stt_translate = int(config['Microphone']['stt_translate'])
            self.whisper_process_device = config['Microphone']['process_device']
            self.whisper_type = config['Microphone']['whisper_type']
            self.whisper_url = config['Microphone']['whisper_url']
            self.audio_threshold = config['Microphone']['audio_threshold']
            self.pause_threshold = float(config['Microphone']['pause_threshold'])
            self.listen_timeout = int(config['Microphone']['listen_timeout'])

            # [Hotkey]
            self.hotkey = config['Hotkey']['hotkey']
            self.textbox_timer = config['Hotkey']['textbox_timer']

            # [LanguageModel]
            self.llm = config['LanguageModel']['model']
            self.max_response_sentences = int(config['LanguageModel']['max_response_sentences'])
            self.wait_time_buffer = float(config['LanguageModel']['wait_time_buffer'])
            self.alternative_openai_api_base = config['LanguageModel']['alternative_openai_api_base']
            self.maximum_local_tokens = config['LanguageModel']['maximum_local_tokens']
            self.temperature = float(config['LanguageModel']['temperature'])
            self.top_p = float(config['LanguageModel']['top_p'])
            self.frequency_penalty = float(config['LanguageModel']['frequency_penalty'])
            self.max_tokens = int(config['LanguageModel']['max_tokens'])
            self.BOS_token = config['LanguageModel']['BOS_token']
            self.EOS_token = config['LanguageModel']['EOS_token']
            self.message_signifier = config['LanguageModel']['message_signifier']
            self.message_seperator = config['LanguageModel']['message_seperator']
            self.message_format = config['LanguageModel']['message_format']
            self.system_name = config['LanguageModel']['system_name']
            self.user_name = config['LanguageModel']['user_name']
            self.assistant_name = config['LanguageModel']['assistant_name']
            stop_value = config['LanguageModel']['stop']
            if ',' in stop_value:
                # If there are commas in the stop value, split the string by commas and store the values in a list
                self.stop = stop_value.split(',')
            else:
                # If there are no commas, put the single value into a list
                self.stop = [stop_value]
            self.conversation_limit_pct = float(config['LanguageModel']['conversation_limit_pct'])
            self.experimental_features = True if config['LanguageModel']['experimental_features'] == '1' else False

            # [Speech]
            self.xvasynth_process_device = config['Speech']['tts_process_device']
            self.pace = float(config['Speech']['pace'])
            self.use_cleanup = int(config['Speech']['use_cleanup'])
            self.use_sr = int(config['Speech']['use_sr'])

            # [Cleanup]
            self.remove_mei_folders = config['Cleanup']['remove_mei_folders']

            # [Debugging]
            self.debug_mode = config['Debugging']['debugging']
            self.play_audio_from_script = config['Debugging']['play_audio_from_script']
            self.debug_character_name = config['Debugging']['debugging_npc']
            self.debug_use_mic = config['Debugging']['use_mic']
            self.default_player_response = config['Debugging']['default_player_response']
            self.debug_exit_on_first_exchange = config['Debugging']['exit_on_first_exchange']
            self.add_voicelines_to_all_voice_folders = config['Debugging']['add_voicelines_to_all_voice_folders']

            # [Prompt]
            self.prompt = config['Prompt']['prompt']
            self.multi_npc_prompt = config['Prompt']['multi_npc_prompt']

            # Other
            self.is_local = False
            pass
        except Exception as e:
            logging.error('Parameter missing/invalid in config.ini file!')
            raise e

        # don't trust; verify; test subfolders
        if not os.path.exists(f"{self.game_path}"):
            invalid_path(self.game_path, f"{self.game_path}")
        else:
            check_missing_mantella_file(self.game_path)

        if not os.path.exists(f"{self.xvasynth_path}\\resources\\"):
            invalid_path(self.xvasynth_path, f"{self.xvasynth_path}\\resources\\")
        if not os.path.exists(f"{self.mod_path}\\Sound\\Voice\\Mantella.esp"):
            invalid_path(self.mod_path, f"{self.mod_path}\\Sound\\Voice\\Mantella.esp")

        self.mod_path += "\\Sound\\Voice\\Mantella.esp"
