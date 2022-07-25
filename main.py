# # # # Selenium_PAA - v1.5 # # # # #

from functions.foxwd_new import GSearch as GSearch
from functions.tools import load_pickle, save_pickle
from constants import PROJECT_DIR, PICKLE_FILE, CHECKPOINT_FILE, PROJECT_NAME
from os.path import exists

# # # # # --> SET VARIABLES <-- # # # # # #
# PROJECT_NAME = 'FreezeDried' < Constants.py (until CLI integration)
input_questions = PROJECT_DIR + '/input/' + PROJECT_NAME + '-Questions.txt'
checkpoint = 0  # placeholder
# # # # # # # # # # # # # # # # # # # # # #

print(input_questions)
# input_keys = PROJECT_DIR + '/input/test.csv'
print(CHECKPOINT_FILE)

# Check Pickle exist & load
pickle_exists = exists(PICKLE_FILE)
if pickle_exists is True:
    data = load_pickle(PICKLE_FILE)
else:
    data = []

# Check for error checkpoint
checkpoint_exists = exists(CHECKPOINT_FILE)
if checkpoint_exists is True:
    with open(CHECKPOINT_FILE, 'r') as f:
        checkpoint = int(f.readline())
    print('Checkpoint found:', checkpoint)
else:
    checkpoint = int(0)

with open(input_questions, 'r') as file:
    my_questions = [line.rstrip('\n') for line in file]

print('=== Total lines to be processed:', len(my_questions), '===')

for i in range(checkpoint, len(my_questions)):
    print(' ~ Getting Answer', i)
    print(' ~~ Question:', my_questions[i])
    try:
        gs = GSearch(my_questions[i]).get_answer()
        output = gs
        print(output)
        data.append(output)
        save_pickle(PICKLE_FILE, data)
    except Exception as e:
        print(' -- Skipping Answer... -', my_questions[i])
        i = i + 1
        f = open(CHECKPOINT_FILE, 'w')
        f.write(str(i))
        f.close()
    else:
        f = open(CHECKPOINT_FILE, 'w')
        f.write(str(i))
        f.close()


print('=== Completed ===')
