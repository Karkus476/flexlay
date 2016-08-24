# Flexlay - A Generic 2D Game Editor
#
# ISC License
# Copyright (C) 2016 Karkus476 <karkus476@yahoo.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR ON SEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

class TextIterator:
    """A simple class for iterating over text

    This class is useful when creating a backend if you wish to iterate over
    text and find regular expressions.

    Members:
    The TextIterator has 5 key members:
    text - The text being iterated over
    char - The current character which the iterator is at
    index - The current index of the iterator.
            TextIterator.text[TextIterator.index] = TextIterator.char
    accepted - The most recently accepted string.
    done - Whether the iterator has finished.
    line_no - The current line number, starts at 1
    char_no - The current number of characters passed on this line, 
              starting at 1 the newline at the start of the line is 0.
    """
    def __init__(self, text):
        """Create a new TextIterator instance"""
        self.text = text
        self.char = ""
        self.index = 0
        self.accepted = ""
        self.done = False
        # Line number, starting at 1
        # Number of newlines passed + 1
        self.line_no = 1
        # Number of chars since last newline + 1
        # Character number on this line, starting at 1
        self.char_no = 1
        self.set_index(0)

    def set_index(self, index):
        """Set the current index in the text.

        Use this, to ensure that the iterator updates properly.
        Entering a value below 0 will raise an IndexError.
        Entering a value above len(text) will raise an IndexError.
        Entering the value len(text) will stop all iteration and set done to
        True
        """
        if not self.done:
            if len(self.text) > index and index >= 0:
                # Set line_no
                index_diff = index - self.index
                if index_diff > 0:
                    self.line_no += self.text[self.index:index].count("\n")
                elif index_diff < 0:
                    self.line_no -= self.text[index:self.index].count("\n")
                
                # Set char_no
                newline_index = self.text[index::-1].find("\n")
                
                if newline_index == -1:
                    self.char_no = index + 1
                else:
                    self.char_no = newline_index
                
                # Set index and char
                self.index = index
                self.char = self.text[index]
            elif index == len(self.text):
                self.done = True
                self.char = ""
                self.index = -1
                self.line_no = -1
                self.char_no = -1
            else:
                raise IndexError("TextIterator reached index outside of text"\
                                 " passed to it")

    def step(self):
        """Step to the next char in the text

        Stepping too far will raise an IndexError.
        """
        self.set_index(self.index + 1)

    def steps(self, number):
        """Step a number of times

        Negative numbers will step backwards.
        Stepping too far will raise an IndexError.
        """
        self.set_index(self.index + number)

    def step_back(self):
        """Equivalent to steps(-1)"""
        self.set_index(self.index - 1)

    def ignore_regex(self, regex):
        """Jump the index over and beyond a match to the regex.

        regex must be compiled using re.compile(string_pattern)
        "accepted" will not be updated. Use accept_regex() to store skipped text
        True will be returned if some match is found to ignore, otherwise False
        """
        match = regex.match(self.text[self.index:])
        if match is not None:
            self.set_index(match.end() + self.index)
            return True
        return False

    def accept_string(self, string):
        """Jump the index over and beyond a string, if next in the text

        If a match is found, string will be stored in "accepted".
        True will be returned if a match is found, otherwise False
        """
        does_match = True
        check_index = self.index
        for char in string:
            try:
                if char == self.text[check_index]:
                    check_index += 1
                else:
                    does_match = False
                    break
            except IndexError:
                does_match = False
                break
        if does_match:
            self.accepted = string
            self.set_index(check_index)
            return True
        return False

    def accept_regex(self, regex):
        """Jump the index over and beyond a regex match, if next in the text

        If a match is found, string will be stored in "accepted".
        True will be returned if a match is found, otherwise False
        """
        match = regex.match(self.text[self.index:])
        if match is not None:
            self.accepted = self.text[match.start() + self.index:
                                      match.end() + self.index]
            self.set_index(match.end() + self.index)
            return True
        return False
    
