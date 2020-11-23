from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import random
import syllables


class Haikudetector(BotPlugin):
    """Detects responses with haikus and returns a formatted haiku"""
    def callback_message(self, mess):
        """Runs on every message"""
        if syllables.estimate(mess.body) == 17 and mess.body.upper().replace(' ', '').find('FOO') != -1:
            return "You said a haiku"

    @arg_botcmd('word', type=str)
    def syllables(self, msg, word=None):
        return syllables.estimate(word)
