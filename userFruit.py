class UserFruit:
    
    def __init__ (self, fruit, star):
        self.fruit = fruit
        self.star = star

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, UserFruit):
            return (self.star == other.star) and (self.fruit == other.fruit)
        return False


    

        


