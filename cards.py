class Cards:

    def __init__(self, name, title, titleShort, spec, image):
        self.name = name
        #name is the character name.  
        #There can be duplicates of these, however they should still be used somewhat as an identifier. 
        #optimally if there are two it should ask which one you mean when you request a name and you can type in the full name then.
        #Examples are "Snootly", "Naalu", or "DankGoodHeals".
        self.title = title
        #title is the card specific description that describes the player in a funny or relevant way. 
        #This is always unique but shouldn't be the sole identifier. 
        #Examples are "Feeder of cats", "BIS healer", or "Casino owner"
        self.titleShort = titleShort
        #abriviation of title. 
        #Can be used instead of title to identify since those get long af
        #Examples are "FoC", "BH", or "CO"
        self.spec = spec
        #This is an array of all the specs the card can possibly be
        #Default/main is at [0]
        #This helps give some specs some extra spotlight and lets me draw less cards.
        #Specs should never share gear and should be treated seperetly. 
        #Specs decide on the powers
        #Examples are [Protection Paladin, Holy Paladin], [Restoration Shaman, Elemental Shaman], [Holy Paladin, Protection Paladin]
        self.image = image
        #card art. 
        #url. Not upload



        
