class Piece:
    def __init__(self, piece_coordinates):
        self.coordinates = piece_coordinates
        self.anchor = (0,0)
    
    def __repr__(self):
        return f"Anchored at {self.anchor}, Piece : {self.coordinates}\n"
        