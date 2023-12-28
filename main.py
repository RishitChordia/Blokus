import tkinter
from blokus_gui import BlokusViewController


def start_game(num_players_entry, grid_size_entry):
    try:
        num_players = max(int(num_players_entry.get()), 2)
    except:
        num_players = 2
    try:
        board_size = min(max(int(grid_size_entry.get()), 10), 28)
    except:
        board_size = 20
    b = BlokusViewController(num_players, board_size)
    b.create_gui()


def launch_game():
    root = tkinter.Tk()
    root.title("Game Setup")

    root.geometry("300x200")
    root.resizable(False, False)
    root.configure(bg="#FFFFFF")

    label_players = tkinter.Label(root, text="Number of Players:", bg="#FFFFFF")
    label_players.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")

    num_players_entry = tkinter.Entry(root, width=10)
    num_players_entry.insert(0, "2")
    num_players_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

    label_size = tkinter.Label(root, text="Grid Size:", bg="#FFFFFF")
    label_size.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    grid_size_entry = tkinter.Entry(root, width=10)
    grid_size_entry.insert(0, "20")
    grid_size_entry.grid(row=1, column=1, padx=10, pady=5)

    start_button = tkinter.Button(root, text="Start Game", command= lambda : start_game(num_players_entry, grid_size_entry), bg="#4CAF50", fg="white")
    start_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))

    root.mainloop()


if __name__ == "__main__":
    launch_game()