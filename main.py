# # # # Selenium_PAA - v1.7 # # # # #

from functions.foxwd_new import GSearch as GSearch
from functions.tools import pickle_it, pickle2json, cp_load, cp_write
from functions.tools import load_json, append_json
from functions.constants import project_root, PICKLE_FILE, CHECKPOINT_FILE, project_name, JSON_FILE
from os.path import exists

# # # # # --> SET VARIABLES <-- # # # # # #
# project_name = 'NameOfProject' < Constants.py (until CLI integration)
input_questions = project_root + '/input/' + project_name + '-Questions.txt'
# # # # # # # # # # # # # # # # # # # # # #

# input_keys = project_root + '/input/test.csv'


# Look for error checkpoint
checkpoint = cp_load(CHECKPOINT_FILE)

with open(input_questions, 'r', encoding='UTF-8') as file:
    my_questions = [line.rstrip('\n') for line in file]

print('=== Total lines to be processed:', len(my_questions), '===')

for i in range(checkpoint, len(my_questions)):
    print(' ~ Getting Answer', i)
    print(' ~~ Question:', my_questions[i])
    try:
        data = []
        gs = GSearch(my_questions[i], 7).get_answer()
        data.append(gs)
        append_json(JSON_FILE, data)
        # pickle_it(PICKLE_FILE, data)
        # Clear table
        data.clear()  # Clear datatable
        cp_write(CHECKPOINT_FILE, i)
    except Exception as e:
        print(' -- Skipping Answer... -', my_questions[i])
        i = i + 1
        cp_write(CHECKPOINT_FILE, i)


# # Convert pickle to JSON
# if len(my_questions) == checkpoint:
#     pickle2json(PICKLE_FILE)
# else:
#     print('No Pickle > JSON conversion - job incomplete.')


print('=== Completed ===')

# # # # # # Stage 3 # # # # # #
# Take related output from Stage 2 and convert into simple JSON with Q & As.


# NOTES/TO DO:
# Switch pickle back to JSON + remove conversion
# Added length to the GSearch class - might have to update other files if inconsistent
# Remove clearing of datatable every loop? Not necessary after isolating crash issue to selenium tmp files
# Likely have to change JSON defined functions once structured JSON data better.
#
# Make next stages into Class/Functions then append to this script
