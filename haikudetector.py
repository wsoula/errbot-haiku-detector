from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import syllables
import logging


class Haikudetector(BotPlugin):
    """Detects responses with haikus and returns a formatted haiku"""
    def callback_message(self, mess):
        """Runs on every message"""
        body_array = mess.body.replace('  ', ' ').split(' ')
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
        if syllable_count == 17 and mess.body.upper().replace(' ', '').find('FII') != -1:
            self.send_card(
                  in_reply_to=mess,
                  body=line_1+'\n'+line_2+'\n'+line_3,
                  title='You said a haiku!'
              )

    @arg_botcmd('word', type=str)
    def syllables(self, msg, word=None):
        return syllables.estimate(word)
