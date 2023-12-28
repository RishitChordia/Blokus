import time
import tkinter
from player_frame_utils import initialize_frames, show_new_piece
from blokus_board import BlokusBoard

color_list = ["red", "blue", "green", "yellow", "gray", "orange", "white"]

class BlokusViewController(BlokusBoard):
    def __init__(self, players=2, size=20):
        super().__init__(players, size)
        self.piece_held = None
        self.toplevel = None
        self.game_frame = None
        self.board_buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.player_frame_container = None
        self.player_grids = dict()
        self.highlighted_coordinates = []
        
    def create_gui(self):
        
        self.toplevel = tkinter.Toplevel()
        self.toplevel.title("game")
        self.toplevel.geometry('1200x1000')
        self.toplevel.config(bg="#3f525a")

        self.game_frame = tkinter.Frame(self.toplevel, highlightthickness=10, highlightbackground="#1f292d")
        self.game_frame.grid(column=0, row=0, padx=20, pady=20, rowspan=4)


        for i in range(self.size):
            for j in range(self.size):
                button = tkinter.Button(self.game_frame, height=1, width=2, bd=0, command=lambda a=i, b=j: self.piece_placed((a,b)), highlightthickness=0, borderwidth=1, bg = "white")
                button.bind('<Enter>', lambda event, x=i, y=j: self.handle_hover((x,y)))
                button.bind('<Leave>', lambda event:  self.dehighlight_coordinates())
                button.grid(column=j, row=i)
                self.board_buttons[i][j] = button
                
        self.player_frame_container = tkinter.Frame(self.toplevel, highlightthickness=5, highlightbackground="#1f292d")
        self.player_frame_container.grid(column=1, row=0, padx=10, pady=5, rowspan=4)

        for player in range(self.players):
            self.player_grids[player] = []
            player_frame = tkinter.Frame(self.player_frame_container, highlightthickness=2, highlightbackground="#1f292d")
            player_frame.grid(column=1, row=player * 5 + 1, padx=0, pady=0)

            for piece_number in range(4):
                new_grid = [[None for _ in range(4)] for _ in range(4)]
                grid_frame = tkinter.Frame(player_frame, highlightthickness=0, highlightbackground="#1f292d")
                grid_frame.grid(column=piece_number, row=0, padx=4, pady=4)
                
                for i in range(4):
                    for j in range(4):
                        button = tkinter.Button(grid_frame, height=1, width=2, bd=0,
                                            command=lambda a=i, b=j, n=piece_number, p=player: self.piece_clicked(p, n, (a,b)),
                                            highlightthickness=0, borderwidth=0, bg = "white")
                        button.grid(column=piece_number + j, row=i)
                        new_grid[i][j] = button
                self.player_grids[player].append(new_grid)
                
        initialize_frames(self.player_grids, self.pieces_in_hand)

        self.toplevel.mainloop()
        
        
    def piece_clicked(self, player, piece_index, new_anchor = (0,0)):
        if self.turn == player:
            self.piece_held = piece_index
            self.pieces_in_hand[player][piece_index].anchor = new_anchor
            
    
    def piece_placed(self, coordinates):
        # print(f"{self.piece_held}\n\n\n{self.pieces_in_hand}\n\n\n{coordinates}")
        target_coordinates = self.make_move(self.piece_held, coordinates)
        if target_coordinates:
            self.update_coordinates(target_coordinates)
            show_new_piece(self.player_grids[self.turn][self.piece_held], self.pieces_in_hand[self.turn][self.piece_held], self.turn)
            self.piece_held = None
            self.change_turn()
        
    
    
    def update_coordinates(self, target_coordinates):
        for x,y in target_coordinates:
            self.board_buttons[x][y].configure(bg = color_list[self.board[x][y].player])
            
    def change_turn(self):
        if super().change_turn():
            self.game_frame.configure(highlightbackground= color_list[self.turn])
            self.game_frame.update()
        else:
            self.end_game_animation()
    
    
    def end_game_animation(self):
        print("game over")
        print(self.board)
        winners = self.determine_winners()
        
        self.game_frame.configure(highlightbackground="#1f292d")
        self.game_frame.update()
        for i, button_row in enumerate(self.board_buttons):
            for j, button in enumerate(button_row):
                if self.board[i][j].player not in winners:
                    button.configure(bg = "white")
                    button.update()
                    time.sleep(3/(self.size*self.size))
                    
    
    def handle_hover(self, coordinates):
        if self.piece_held == None:
            return
        target_coordinates = self.get_target_coordinates(self.pieces_in_hand[self.turn][self.piece_held], coordinates)
        if self.valid_piece_position(target_coordinates):
            self.highlighted_coordinates = target_coordinates
            self.highlight_coordinates()
    
    
    def dehighlight_coordinates(self):
        for x,y in self.highlighted_coordinates:
            if self.board[x][y].player == -1:
                self.board_buttons[x][y].configure(bg = "white")
        self.highlighted_coordinates = []
        
        
    def highlight_coordinates(self):
        for x,y in self.highlighted_coordinates:
            self.board_buttons[x][y].configure(bg = "light green")


if __name__ == "__main__":
    b = BlokusViewController(3, 27)

    b.create_gui()
