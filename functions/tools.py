import pickle
from os.path import exists


def save_pickle(name, data):
    with open(name, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


# def checkpoint_check(CHECKPOINT_FILE):
#     checkpoint_exists = exists(checkpoint_file)
#     if checkpoint_exists is True:
#         with open(CHECKPOINT_FILE, 'r') as f:
#             checkpoint = int(f.readline())
#         print('Checkpoint found:', checkpoint)
#     else:
#         checkpoint = int(0)
