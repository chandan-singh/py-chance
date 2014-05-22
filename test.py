import unittest
import chance
from chance import *
import string

MAX_INT = 9223372036854775806
MIN_INT = -MAX_INT
NUMBERS = string.digits
CHARS_LOWER = string.ascii_lowercase
CHARS_UPPER = string.ascii_uppercase
HEX_POOL = NUMBERS + 'abcdef'
SYMBOLS = "!@#$%^&*()[]-=+{}[]:;\"'?/<>,.~`\\|"

class ChanceTest(unittest.TestCase):
    def setUp(self):
        pass


    def test_boolean(self):
        '''
        Tests boolean() method
        '''
        self.assertFalse(boolean(0))
        self.assertTrue(boolean(100))
        self.assertIn(boolean(), (False, True))
        self.assertIn(boolean(50), (False, True))
        self.assertRaises(ChanceRangeException, boolean, -1)
        self.assertRaises(ChanceRangeException, boolean, 101)


    def test_character(self):
        ''' Tests character() method
        '''
        self.assertIn(character(), CHARS_LOWER+CHARS_UPPER+SYMBOLS+NUMBERS)
        self.assertIn(character('asdFG'), 'asdFG')
        self.assertIn(character(CHARS_LOWER), CHARS_LOWER)
        self.assertIn(character(CHARS_UPPER), CHARS_UPPER)
        self.assertIn(character(SYMBOLS), SYMBOLS)
        self.assertIn(character(casing='lower', isAlpha=True), CHARS_LOWER+NUMBERS)
        self.assertIn(character(casing='upper', isAlpha=True), CHARS_UPPER+NUMBERS)

        self.assertIn(character(isSymbol=True), SYMBOLS)
        self.assertIn(character(casing='lower'), CHARS_LOWER+SYMBOLS+NUMBERS)
        self.assertIn(character(casing='upper'), CHARS_UPPER+SYMBOLS+NUMBERS)
        self.assertIn(character(isAlpha=True), CHARS_LOWER+CHARS_UPPER+NUMBERS)
        self.assertIn(character('asdASD123!@#', casing='lower', isAlpha=True), 'asd123')
        self.assertIn(character('asdASD123!@#', casing='upper', isAlpha=True), 'ASD123')
        self.assertIn(character('asdASD123!@#', isSymbol=True), '!@#')
        self.assertNotIn(character('asd', casing='lower'), 'ASD')
        self.assertNotIn(character('ASD', casing='upper'), 'asd')

        self.assertRaises(ChanceRangeException, character, '', True, True)


    def test_randstring(self):
        ''' Tests randstring() method
        '''
        self.assertIn(randstring(1), CHARS_LOWER+CHARS_UPPER+SYMBOLS+NUMBERS)
        for c in randstring(5):
            self.assertIn(c, CHARS_LOWER+CHARS_UPPER+SYMBOLS+NUMBERS)
        
        self.assertEqual(5, len(randstring(5)))
        self.assertEqual(5000, len(randstring(5000)))

        self.assertRaises(ChanceRangeException, randstring, 5, '', True, True)


    def test_syllable(self):
        self.assertIn(len(syllable()), (2,3))
        self.assertEqual(len(syllable(5)), 5)
        #print syllable()

    def test_word(self):
        self.assertLess(len(word()), 10)
        self.assertEqual(len(word(5)), 5)
        self.assertLessEqual(len(word(syllables=5)), 15)
        self.assertRaises(ChanceRangeException, word, 5, 4)
        #print word()


    def test_sentence(self):
        self.assertLess(len(sentence()), 500)

if __name__ == '__main__':
    unittest.main()