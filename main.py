# Test main

from board import Board, BoardException

if __name__ == '__main__':
    brd = Board(size=(6, 7), walls=20, pits=4)

    print("Start (yes, no): ", end=" ")
    choice = str(input())

    while choice != "no":
        try:
            brd.new_board()
        except BoardException as brerr:
            print(brerr.msg)
            break

        while not brd.done:
            brd.show()
            action = int(input("Your action: "))
            reward, done, win = brd.step(action)
            if done and win:
                print("You won!")
            elif done and not win:
                print("You lose!")
            print(f"Reward: {reward}, State: {brd.state()}")

        print("Continue (yes, no): ", end=" ")
        choice = str(input())


    
        


