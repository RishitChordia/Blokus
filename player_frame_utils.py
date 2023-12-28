import tkinter
import random

color_list = ["red", "blue", "green", "yellow", "gray", "orange", "white"]

def show_piece(grid, piece, player):
    x0, y0 = piece.anchor
    for x_rel, y_rel in piece.coordinates:
        x1, y1 = x_rel - x0, y_rel - y0
        grid[x1][y1].configure(bg = color_list[player], fg = color_list[player], borderwidth = 0)
        
def flush_grid(grid):
    for button_row in grid:
        for button in button_row:
            button.configure(bg = "white")
            
            
def show_new_piece(grid, piece, player):
    flush_grid(grid)
    show_piece(grid, piece, player)


def initialize_frames(player_grids, pieces_in_hand):
    for player in player_grids.keys():
        for grid, piece in zip(player_grids[player], pieces_in_hand[player]):
            show_piece(grid, piece, player)
    for player_pieces in player_grids.values():
        for grids in player_pieces:
            for button_row in grids:
                for button in button_row:
                    button.update()
