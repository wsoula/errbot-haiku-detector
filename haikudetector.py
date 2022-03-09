""" Detect when people talk in haiku """
import os
import logging
from errbot import BotPlugin, arg_botcmd, botcmd
import syllables

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODE = os.getenv('MODE', 'reaction')  # 'reaction' for just an emoji, 'message' for a message to be sent, 'all' for all
REACTION = os.getenv('REACTION', 'haiku')  # https://slackmojis.com/emojis/3545-haiku
PREFIX = os.getenv('PREFIX', '!')  # Only run for one tobor, if you have multiple with different prefixes


class Haikudetector(BotPlugin):
    """ Detects responses with haikus and returns a formatted haiku """
    def callback_message(self, mess):
        """Runs on every message"""
        bot_prefix = os.getenv('BOT_PREFIX')
        if PREFIX == bot_prefix:
            haiku_pieces = self.haiku_check(mess.body)
            if (haiku_pieces['syllable_count'] == 17 and haiku_pieces['line_1_syllables'] == 5 and
               haiku_pieces['line_2_syllables'] == 7 and haiku_pieces['line_3_syllables'] == 5):
                haiku_text = haiku_pieces['line_1']+'\n'+haiku_pieces['line_2']+'\n'+haiku_pieces['line_3']
                if MODE in ['message', 'all']:
                    self.send_card(
                        in_reply_to=mess, body=haiku_text, title='You might have said a haiku!')
                if MODE in ['reaction', 'all']:
                    self._bot.add_reaction(mess, REACTION)
                    logger.info('haiku=%s', haiku_text)
        else:
            logger.info('prefix=%s bot_prefix=%s not running haiku code', PREFIX, bot_prefix)

    def haiku_check(self, sentence):
        """ Check message and return formatted haiku """
        body_array = sentence.replace('  ', ' ').split(' ')
        line_1 = ''
        line_1_syllables = 0
        line_2 = ''
        line_2_syllables = 0
        line_3 = ''
        line_3_syllables = 0
        syllable_count = 0
        for word in body_array:
            word_syllables = syllables.estimate(word)
            syllable_count = syllable_count + word_syllables
            if line_1_syllables + word_syllables <= 5:
                line_1_syllables = line_1_syllables + word_syllables
                line_1 = line_1 + ' ' + word
            elif line_2_syllables + word_syllables <= 7 and line_1_syllables == 5:
                line_2_syllables = line_2_syllables + word_syllables
                line_2 = line_2 + ' ' + word
            elif line_3_syllables + word_syllables <= 5 and line_1_syllables == 5 and line_2_syllables == 7:
                line_3_syllables = line_3_syllables + word_syllables
                line_3 = line_3 + ' ' + word
        return {'syllable_count': syllable_count, 'line_1_syllables': line_1_syllables, 'line_1': line_1,
                'line_2_syllables': line_2_syllables, 'line_2': line_2,
                'line_3_syllables': line_3_syllables, 'line_3': line_3}

    @arg_botcmd('word', type=str)
    def syllables(self, msg, word=None):
        """ Return the syllable count for a word """
        logger.info('msg=%s', msg)
        return syllables.estimate(word)

    @botcmd
    def haiku(self, msg, args):
        """ Check if the passed sentence is a haiku and return it formatted """
        logger.info('args=%s msg=%s', args, msg)
        haiku_pieces = self.haiku_check(' '.join(args))
        logger.info('haiku_pieces=%s', haiku_pieces)
        if (haiku_pieces['syllable_count'] == 17 and haiku_pieces['line_1_syllables'] == 5 and
           haiku_pieces['line_2_syllables'] == 7 and haiku_pieces['line_3_syllables'] == 5):
            haiku_text = haiku_pieces['line_1']+'\n'+haiku_pieces['line_2']+'\n'+haiku_pieces['line_3']
            return haiku_text
        return 'Not a haiku'
