#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fallout 3 Terminal Hacker


def processwords(checkword, checknum, uncheckwords):
    wordsdata = {}
    matches = []
    for word in uncheckwords:
        worddata = {}
        diffs = [i for i, x in enumerate(zip(checkword, word)) if x[0] <> x[1]]
        matchnum = len(word) - len(diffs)
        if matchnum == checknum:
            matchnum_match = 1
        elif matchnum > checknum:
            matchnum_match = 2
        else:
            matchnum_match = 0
        if len(word) == len(checkword):
            matchlen = True
        else:
            matchlen = False
        if matchnum_match == 1 and matchlen:
            matchpos = True
            matches.append(word)
        else:
            matchpos = False
        worddata["diffs"] = diffs
        worddata["matchnum"] = matchnum
        worddata["matchnum_match"] = matchnum_match
        worddata["matchlen"] = matchlen
        worddata["matchpos"] = matchpos
        wordsdata[word] = worddata
    wordsdata["~matches~"] = matches
    return wordsdata


def compactdata(data):
    words = data.keys()
    for word in data["~matches~"]:
        words.remove(word)
    words.remove("~matches~")
    for word in words:
        del data[word]
    return data


class TextInterface():
    def __init__(self):
        self.verbose = 1
        self.highlight = True
        self.highlight_settings = {"match":[True, "\033[32m%s\033[00m"] , "diff":[True, "\033[31m%s\033[00m"]}
        self.data = None

    def booltoyn(self, var):
        if var == True:
            return "Yes"
        else:
            return "No"

    def askyn(self, message, yes="yes", no="no"):
        choice = raw_input(message).lower()
        while choice != yes and choice != no:
            if choice == "":
                return None
            print "Invalid selection, either %s or %s." % (yes, no, yes, no)
            choice = raw_input(message).lower()
        if choice == yes:
            choice = True
        else:
            choice = False
        return choice

    def asknum(self, message, nrange=None):
        if not nrange == None:
            text_range = " Number has to be between %i and %i." % (nrange[0], nrange[-1:][0])
        else:
            text_range = ""
        while True:
            number = raw_input(message)
            if number == "":
                return None
            if nrange == None and number.isdigit():
                break
            elif number.isdigit():
                if int(number) in nrange:
                    break
            else:
                print "Invaild number%s" % text_range
        return int(number)

    def printcompare(self, checkword, checknum, uncheckdata):
        wordlen = len(checkword)
        _matches = uncheckdata["~matches~"][:]
        if self.verbose >= 1:
            print "Checked word: %s (%s/%s)" % (checkword, checknum, wordlen)
        for (word, data) in uncheckdata.iteritems():
            # Skip ~matches~
            if word == "~matches~":
                continue
            if data["matchpos"] == True:
                matchtext = [True, "Yes", ]
            else:
                if not data["matchlen"]:
                    matchtext = [False, "Wrong length", "Is the word misspelled?"]
                elif data["matchnum_match"] == 2:
                    matchtext = [False, "No", "Too many letters match"]
                elif data["matchnum_match"] == 0:
                    matchtext = [False, "No", "Not enough letters match"]
            if self.highlight:
                if matchtext[0] and self.highlight_settings["match"][0]:
                    matchtext[1] = self.highlight_settings["match"][1] % matchtext[1]
                if not matchtext[0] and self.highlight_settings["diff"][0]:
                    matchtext[1] = self.highlight_settings["diff"][1] % matchtext[1]
            if self.verbose >= 2:
                displaytext = " - ".join(matchtext[1:3])
            else:
                displaytext = matchtext[1]
            if self.highlight and data["matchlen"]:
                displayword = self.highlight_diff(word, data["diffs"])
                if word in _matches:
                    _matches[_matches.index(word)] = displayword
            else:
                displayword = word
            if self.verbose >= 1:
                print "Word:  %s (%i/%i vs %i/%i) Possible match: %s" % (displayword, data["matchnum"], len(word), checknum, wordlen, displaytext)
        if self.verbose >= 0:
            if len(_matches) >= 1:
                print "Possible Match(es) (%i total): %s" % (len(_matches), " ".join(_matches))
            else:
                print "No matches found."
            if len(_matches) == 1:
                print "Password found!"

    def highlight_diff(self, word, diffs):
        output = list(word)
        if self.highlight_settings["match"][0]:
            # Create an inverse diff list to make a match list
            matches = range(len(word))
            for diff in diffs:
                matches.remove(diff)
            # Color the matches
            for match in matches:
                output[match] = self.highlight_settings["match"][1] % output[match]
        if self.highlight_settings["diff"][0]:
            # Color the diffs
            for diff in diffs:
                output[diff] = self.highlight_settings["diff"][1] % output[diff]
        return "".join(output)

    def prompt_checked(self, firstrun=True):
        while True:
            checked_word = raw_input("What word was tried? ").lower()
            if not firstrun and not checked_word in self.data.keys():
                print "%s doesn't exist in the list of words you gave." % checked_word
            else:
                break
        if not firstrun and len(self.data.keys()) <= 3:
            checked_num = -1
        else:
            checked_num = raw_input("How many letters were right? ")
            while True:
                if checked_num.isdigit():
                    checked_num = int(checked_num)
                    if not (checked_num >= len(checked_word) or checked_num < 0):
                        break
                print "The number has to be >= 0 and less than the number of characters in the word. (Unless, of course, %s is the answer.)" % checked_word
                checked_num = raw_input("How many letters were right? ")
        if firstrun:
            unchecked_words = raw_input("What were the other words? ").lower().split(" ")
        else:
            unchecked_words = self.data.keys()
            unchecked_words.remove(checked_word)
            unchecked_words.remove("~matches~")
        return (checked_word, checked_num, unchecked_words)

    def hack_loop(self):
        firstrun = True
        while True:
            if not firstrun:
                self.data = compactdata(self.data)
            (checked_word, checked_num, unchecked_words) = self.prompt_checked(firstrun)
            if checked_num < 0:
                print "If it's not %s, then it must be %s" % (checked_word, unchecked_words[0])
                break
            self.data = processwords(checked_word, checked_num, unchecked_words)
            self.printcompare(checked_word, checked_num, self.data)
            if len(self.data["~matches~"]) <= 1:
                break
            firstrun = False

    def setsettings(self):
        print "(Leave a setting blank to leave it unchanged)"
        # Verbosity
        verbose = self.asknum("Verbosity [%i]: " % self.verbose, range(0,3))
        if not verbose == None:
            self.verbose = verbose
        # Master Highlighting
        highlight = self.askyn("Highlighting [%s]: " % (self.booltoyn(self.highlight)))
        if not highlight == None:
            self.highlight = highlight
        # Highlight match
        highlight_match = self.askyn("Highlight Match [%s]: " % (self.booltoyn(self.highlight_settings["match"][0])))
        if not highlight_match == None:
            self.highlight_settings["match"][0] = highlight_match
        highlight_match_color = raw_input("Highlight Match Color [\"%s\"]: " % self.highlight_settings["match"][1])
        if not highlight_match_color == "":
            self.highlight_settings["match"][1] = highlight_match_color
        # Highlight diff
        highlight_diff = self.askyn("Highlight Diff [%s]: " % (self.booltoyn(self.highlight_settings["diff"][0])))
        if not highlight_diff == None:
            self.highlight_settings["diff"][0] = highlight_diff
        highlight_diff_color = raw_input("Highlight Diff Color [\"%s\"]: " % self.highlight_settings["diff"][1])
        if not highlight_diff_color == "":
            self.highlight_settings["diff"][1] = highlight_diff_color
        self.viewsettings()

    def viewsettings(self):
        print """Settings:
Verbose Level: %i
Highlighting: %s
Highlight match: %s %s
Highlight diff: %s %s""" % (self.verbose, self.booltoyn(self.highlight), self.booltoyn(self.highlight_settings["match"][0]),\
self.highlight_settings["match"][1] % "color", self.booltoyn(self.highlight_settings["diff"][0]),\
self.highlight_settings["diff"][1] % "color")

    def main(self):
        option_count = 4
        options = range(1, option_count + 1)
        while True:
            print """/------------------------\\
|    Terminal Hacker     |
|------------------------|
| 1. Hack Terminal       |
| 2. View Settings       |
| 3. Change Settings     |
| 4. Return to main menu |
\\------------------------/"""
            choice = raw_input("Choose a selection: ")
            while True:
                if choice.isdigit():
                    choice = int(choice)
                    if choice in options:
                        break
                print "Not a vaild option."
                choice = raw_input("Choose a selection: ")
            if choice == 1:
                try:
                    self.hack_loop()
                except KeyboardInterrupt:
                    print "\nReturning to menu..."
            elif choice == 2:
                try:
                    self.viewsettings()
                except KeyboardInterrupt:
                    print "\nReturning to menu..."
            elif choice == 3:
                try:
                    self.setsettings()
                except KeyboardInterrupt:
                    print "\nReturning to menu..."
            else:
                break
