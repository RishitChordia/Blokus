from square import Square
from piece_list import PieceList
from piece import Piece
import random

class BlokusBoard:
    def __init__(self, players = 2, size = 20):
        self.size = size
        self.board = [[Square() for _ in range(self.size)] for _ in range(self.size)]
        self.players = players
        self.piece_lists = [PieceList() for _ in range(players)]
        self.first_moves = [True for _ in range(players)]
        self.turn = 0
        self.pieces_in_hand = dict()
        self.initialize_pieces_in_hand()
        
    
    def initialize_pieces_in_hand(self):
        for player in range(self.players):
            random.shuffle(self.piece_lists[player].piece_list)
            # self.piece_lists[player].piece_list += self.piece_lists[player].piece_list
            self.pieces_in_hand[player] = self.piece_lists[player].piece_list[:4]
            self.piece_lists[player].piece_list = self.piece_lists[player].piece_list[4:]
        

    def in_board(self, coordinates):
        x, y = coordinates
        return (-1 < x < self.size) and (-1 < y < self.size)
    
    
    def check_diagonal(self, coordinates):
        x, y = coordinates
        for x_dir, y_dir in ((1,1), (-1,1), (1,-1), (-1,-1)):
            x1, y1 = x + x_dir, y + y_dir
            if self.in_board((x1, y1)) and self.turn == self.board[x1][y1].player:
                return True
        return False
            
        
    def check_adjacent(self, coordinates):
        x, y = coordinates
        for x_dir, y_dir in ((1,0), (-1,0), (0,-1), (0,1)):
            x1, y1 = x + x_dir, y + y_dir
            if self.in_board((x1, y1)) and self.turn == self.board[x1][y1].player:
                return False
        return True
    
        
    def valid_piece_position(self, target_coordinates):            
        own_neighbors = False
        for x, y in target_coordinates:
            if not self.in_board((x, y)):
                return False
            if self.board[x][y].player != -1:
                return False
            if not self.check_adjacent((x, y)):
                return False
            if not own_neighbors and not self.first_moves[self.turn]:
                own_neighbors = own_neighbors or self.check_diagonal((x, y))
            if not own_neighbors and self.first_moves[self.turn]:
                if x in {0, self.size-1} and y in {0, self.size-1}:
                    own_neighbors = True
        return own_neighbors
    
    
    def make_move(self, piece_index, coordinates):
        target_coordinates = self.get_target_coordinates(self.pieces_in_hand[self.turn][piece_index], coordinates)
        if not self.valid_piece_position(target_coordinates):
            return ()
        for x, y in target_coordinates:
            self.board[x][y].player = self.turn
        
        self.first_moves[self.turn] = False
        
        if not self.piece_lists[self.turn].piece_list:
            self.piece_lists[self.turn] = PieceList()
            random.shuffle(self.piece_lists[self.turn].piece_list)
    
        new_piece = self.piece_lists[self.turn].piece_list.pop()
        new_piece.anchor = (0,0)
        self.pieces_in_hand[self.turn][piece_index] = new_piece
        return target_coordinates  
        
        
    def get_target_coordinates(self, piece, coordinates):
        x0, y0 = piece.anchor
        x, y = coordinates
        target_coordinates = []
        for x_rel, y_rel in piece.coordinates:
            x1, y1 = x + x_rel - x0, y + y_rel - y0
            target_coordinates.append((x1,y1))
        return target_coordinates
         
         
    def change_turn(self):
        self.turn = (self.turn + 1)%self.players 
        if not self.out_of_moves():
            return True
        for _ in range(self.players):
            self.turn = (self.turn + 1)%self.players   
            if not self.out_of_moves():
                return True
        return False
        
        
    def out_of_moves(self):
        for piece in self.pieces_in_hand[self.turn]:
            for i in range(self.size):
                for j in range(self.size):
                    target_coordinates = self.get_target_coordinates(piece, (i,j))
                    if self.valid_piece_position(target_coordinates):
                        return False
        return True
                    
            
    def determine_winners(self):
        scores = {i:0 for i in range(self.players)}
        best_score = 0
        winners = {}
        for i in self.board:
            for j in i:
                if j.player != -1:
                    scores[j.player] += 1
                    if scores[j.player] > best_score:
                        best_score = scores[j.player]
                        winners = {j.player}
                    elif scores[j.player] == best_score:
                        winners.add(j.player)
        return winners



    
    
    
# to make a move, i need to check:
# if any diagonally adjacent has same player
# if any adjacent doesnt have same player
# if all squares are vacant

# iterate through all squares
# check if vacant, if not, flash it
# check if adjacency issue, if any, flash it
# finally after iterating, see if diagonal was satisfied atleast once

# board = BlokusBoard()
# for i in board.board:
#     print(i)
# board.make_move(board.piece_lists[0].piece_list[4], (10,10))
# print("made move")
# for i in board.board:
#     print(i)

# b = BlokusBoard()
# print(b.pieces_in_hand)