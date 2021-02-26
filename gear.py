class Gear:

    def __init__ (self, name, GS, specs, piece, weight, image):
        self.name = name
        #name of the gear
        self.GS = GS
        #Gear Score of the item, a number representation of how good it is and how rare it is.
        self.specs = specs
        #array of what specs can claim the item.
        #invalid ones are unable to roll at all
        self.piece = piece
        #neck, ring, trinket, or mainhand
        self.weight = weight
        #number based on how rare it is. Will probably pass in a variable in the object creation.
        self.image = image
        #url of image with border on rarity.
        #Uld = green, ToC = Blue, ICC/RS = Purple ICCH/RSH = Gold
