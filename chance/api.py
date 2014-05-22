# -*- coding: utf-8 -*-

"""
chance.api
~~~~~~~~~~~~

This module implements the Chance API. This work is heavily inspred by
`chancejs<https://github.com/victorquinn/chancejs>`_ authored by Victor Quinn

:copyright: (c) 2014 by Chandan Singh.
:license: Apache2, see LICENSE for more details.

"""

import os
import string
import random
import re
import time

MAX_INT = 9223372036854775806
MIN_INT = -MAX_INT
NUMBERS = string.digits
CHARS_LOWER = string.ascii_lowercase
CHARS_UPPER = string.ascii_uppercase
HEX_POOL = NUMBERS + 'abcdef'
SYMBOLS = "!@#$%^&*()[]-=+{}[]:;\"'?/<>,.~`\\|"


class ChanceRangeException(Exception):
    def __init__(self, errorMessage):
        self._errMsg = errorMessage

    def __str__(self):
        return repr(self._errMsg)


def testRange(test, errorMessage):
    if test:
        raise ChanceRangeException(errorMessage)


def boolean(likelihood=50):
    """For random boolean value (True or False)
    Returns `True` or `False`.

    :param likelihood: (optional) Likelihood of returning True. by default, it is 50 that means True or False have equal chances.

    Usage::

      >>> import chance
      >>> chance.bool()
      False
      >>> chance.bool(30) # In this case only 30% likelihood of `True`, and a 70% likelihood of `False`.
      True
    """

    testRange(
        likelihood < 0 or likelihood > 100,
        'Py-Chance: Likelihood accepts values from 0 to 100.'
    )

    return random.randint(1, 100) <= likelihood


def character(charSet='', isAlpha=False, isSymbol=False, casing=None):
    """Returns a string with random character from the following character-set
    `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()[]-=+{}[]:;"'?/<>,.~`\|`

    :param charSet: (optional) Character will be generated with characters only from `charSet`
    :param isAlpha: (optional) Only an alphanumeric character. (it will raise error `isAlpha` and `isSymbol` both are set `True` together)
    :param isSymbol: (optional) Only a symbol character. (it will raise error `isAlpha` and `isSymbol` both are set `True` together)
    :param casing: (optional) lowercase character will be returned if `lower`, uppercase character will be returned if `upper`; default is `None`.

      >>> import chance
      >>> chance.character()
      V
      >>> chance.character('charpool')
      h
      >>> chance.character(isAlpha=True) 
      5
      >>> chance.character(isSymbol=True)
      $
      >>> chance.character(casing='lower')
      w
      >>> chance.character(casing='upper')
      X
    """

    # TODO: Unicode character support
    testRange(
        isAlpha and isSymbol, 
        'Py-Chance: Cannot specify both isAlpha and isSymbol as True.'
    )
    
    letters = ''
    if casing == 'lower':
        letters = CHARS_LOWER + NUMBERS
    elif casing == 'upper':
        letters = CHARS_UPPER + NUMBERS
    else:
        letters = CHARS_UPPER + CHARS_LOWER + NUMBERS

    pool = letters + SYMBOLS;
    if charSet != '':
        pool = charSet

    if isAlpha:
        pool = ''.join([x for x in pool if x in letters])
    elif isSymbol:
        pool = ''.join([x for x in pool if x in SYMBOLS])

    return random.choice(pool)


def integer(start, end):
    '''Returns a random integer N such that start <= N <= end.
    Its an alias of random.randint(a,b)
    '''
    return random.randint(start, end)


def floating(start, end):
    '''Returns a random floating point number N such that start <= N <= end.
    Its an alias of random.uniform(a,b)
    '''
    return random.uniform(start, end)


def randstring(length, charSet='', isAlpha=False, isSymbol=False, casing=None):
    '''Returns a string of length `length`. 

    :param length: (optional) length of random string
    :param charSet: (optional) string will be generated with characters only from `charSet`
    :param isAlpha: (optional) string consist of alphanumeric character. (it will raise error `isAlpha` and `isSymbol` both are set `True` together)
    :param isSymbol: (optional) string consist of symbol characters. (it will raise error `isAlpha` and `isSymbol` both are set `True` together)
    :param casing: (optional) lowercase character will be returned if `lower`, uppercase character will be returned if `upper`; default is `None`.

    '''
    retString = ''
    while length > 0:
        retString += character(charSet, isAlpha, isSymbol, casing)
        length -= 1

    return retString


def syllable(length=0):
    '''Return a semi-speakable syllable 2 or 3 letters by default
    User can also specify length of a syllable

    :param length: (optional) length of syllable
    '''
    length = length or integer(2, 3)
    consonants = 'bcdfghjklmnprstvwz' # consonants except hard to speak ones
    vowels = 'aeiou'
    allChars = consonants + vowels
    text = ''
            
    for i in range(0, length):
        if i == 0: 
            # First character can be anything
            chr = character(charSet=allChars)
        elif chr not in consonants:
            # Last character was a vowel, now we want a consonant
            chr = character(charSet=consonants)
        else:
            # Last character was a consonant, now we want a vowel
            chr = character(charSet=vowels)
        
        text += chr

    return text


def word(length=0, syllables=0):
    '''Return a semi-pronounceable random (nonsense) word

    :param length: (optional) length of word
    :param length: (optional) number of syllables used in word

    Note: length and syllables should not be specified together
    '''
    testRange(
        length and syllables, 
        'length and syllables shall not be specified together'
    )

    syllables = syllables or integer(1,3)
    text = ''

    if length:
        # Either bound word by length
        while len(text) < length:
            text += syllable()
            
        text = text[:length]
    else:
        # Or by number of syllables
        while syllables > 0:
            syllables -= 1
            text += syllable()
            
    return text


def sentence(length=0, words=0):

    testRange(
        length and words, 
        'length and words shall not be specified together'
    )

    words = words or integer(12, 18)
    text = ''
    wordList = []

    if words:
        while words > 0:
            words -= 1
            wordList.append(word())
    else:
        while length > 0:
            newWord = ''
            if length < 5:
                newWord = word(length)
            else:
                newWord = word(integer(2, 8))
            
            length = length - len(newWord) - 1 # length of word plus space char

    text = ' '.join(wordList)
    text = text.capitalize() + '.'
    return text




