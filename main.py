# main.py
from game.board import Minesweeper

game = Minesweeper(rows=8, cols=8, mines=10, seed=42)

print("Type moves like:  o 3 4   to open row 3 col 4")
print("Or:               f 3 4   to toggle a flag")
print("Rows and cols start at 0")
print()

game.print_board()

while True:
    cmd = input("\nMove (o r c | f r c | q): ").strip().lower()
    if not cmd:
        continue
    if cmd == "q":
        print("bye")
        break

    parts = cmd.split()
    if len(parts) != 3 or parts[0] not in ("o", "f"):
        print("format is: o r c  or  f r c")
        continue

    action, rs, cs = parts
    try:
        r, c = int(rs), int(cs)
    except ValueError:
        print("r and c must be integers")
        continue

    if action == "f":
        game.toggle_flag(r, c)
        game.print_board()
        continue

    # action == "o"
    alive = game.reveal(r, c)
    game.print_board()
    if not alive:
        print("\nyou hit a mine — game over")
        print("\nFull board:")
        game.print_board(reveal_all=True)
        break

    if game.is_won():
        print("\nnice — you cleared the board")
        print("\nFull board:")
        game.print_board(reveal_all=True)
        break
