import numpy as np
import torch
import random
from matplotlib import pylab as plt
from board import Board


def test_model(nn_model, display=True):
    j = 0
    test_game = Board(size=board_size)
    test_game.new_board()
    cur_state_ = test_game.board.reshape(1, board_cells) + np.random.rand(1, board_cells) / 10.0
    state = torch.from_numpy(cur_state_).float()
    if display:
        print("Initial State:")
        test_game.show()
    over = False
    while not over:
        cur_qval = nn_model(state)
        cur_qval_ = cur_qval.data.numpy()
        cur_action = np.argmax(cur_qval_)
        if display:
            print('Move #: %s; Taking action: %s' % (j, cur_action))
        cur_reward, over = test_game.step(action)
        cur_state_ = test_game.board.reshape(1, board_cells) + np.random.rand(1, board_cells) / 10.0
        state = torch.from_numpy(cur_state_).float()
        if display:
            test_game.show()
        if cur_reward != -1:
            if cur_reward > 0:
                if display:
                    print("Game won! Reward: %s" % cur_reward)
            else:
                if display:
                    print("Game LOST. Reward: %s" % cur_reward)
        j += 1
        if j > 15:
            if display:
                print("Game lost; too many moves.")
            break

    win = True if cur_reward == 1 else False
    return win


def show_stats(cur_losses):
    plt.figure(figsize=(10, 7))
    plt.plot(cur_losses)
    plt.xlabel("Epochs", fontsize=22)
    plt.ylabel("Loss", fontsize=22)
    plt.show()


board_size = (4, 4)
board_cells = board_size[0] * board_size[1]
board = Board(size=board_size)
board.new_board()

l1 = board_cells
l2 = 150
l3 = 100
l4 = 4

model = torch.nn.Sequential(
    torch.nn.Linear(l1, l2),
    torch.nn.ReLU(),
    torch.nn.Linear(l2, l3),
    torch.nn.ReLU(),
    torch.nn.Linear(l3, l4)
)
loss_fn = torch.nn.MSELoss()
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
gamma = 0.9
epsilon = 0.3

epochs = 100
losses = []
for i in range(epochs):
    game = Board(size=board_size)
    game.copy(board)
    state_ = game.board.reshape(1, board_cells) + np.random.rand(1, board_cells) / 10.0
    state1 = torch.from_numpy(state_).float()
    done = False
    while not done:
        qval = model(state1)
        qval_ = qval.data.numpy()
        if random.random() < epsilon:
            action = np.random.randint(0, 4)
        else:
            action = np.argmax(qval_)

        reward, done = game.step(action)
        state2_ = game.board.reshape(1, board_cells) + np.random.rand(1, board_cells) / 10.0
        state2 = torch.from_numpy(state2_).float()
        with torch.no_grad():
            newQ = model(state2.reshape(1, board_cells))
        maxQ = torch.max(newQ)
        if reward == -1:
            Y = reward + (gamma * maxQ)
        else:
            Y = reward
        Y = torch.Tensor([Y]).detach()
        X = qval.squeeze()[action]
        loss = loss_fn(X, Y)
        print(i, loss.item())
        optimizer.zero_grad()
        loss.backward()
        losses.append(loss.item())
        optimizer.step()
        state1 = state2
        if reward != -1:  # Q
            status = 0
    if epsilon > 0.1:  # R
        epsilon -= (1 / epochs)

show_stats(losses)
test_model(model)
