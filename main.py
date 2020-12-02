# Test main

from board import Board

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    brd = Board(size=(5, 8), walls=10, pits=4)
    brd.new_board()
    brd.show()

    while not brd.done:
        action = int(input("Your action:"))
        _, done, win = brd.step(action)
        brd.show()
        if done and win:
            print("You won!")
        elif done and not win:
            print("You lose!")
