from piece import Piece
import random
class PieceList:
    def __init__(self):
        self.piece_list = []
        piece_coordinates = open("piece_coordinates.txt", "r").readlines()
        for coordinate_str in piece_coordinates:
            coordinates = coordinate_str.strip().split(" ")
            coordinates = [i.strip().split(",") for i in coordinates]
            coordinates = [(int(a), int(b)) for a,b in coordinates]
            # coordinates.sort(key = lambda x: min(x[0], x[1]))
            new_piece = Piece(coordinates)
            self.piece_list.append(new_piece)
        # random.shuffle(self.piece_list)
    
    def __repr__(self):
        return f"{self.piece_list}"

if __name__ == "__main__":
    print(PieceList())

