import sys

def read_cli_input():
    """Prompts the user for initial schedule info via command line"""
    num_participants = int(input("How many people? "))
    timeslots = int(input("How many possible timeslots are there?"))
    meeting_length = int(input("How many timeslots are required for a meeting? "))

    names = dict()
    for num in range(num_participants):
        name = input("What's the %s name? " % generate_ordinal(num+1))
        names[name] = [False]*timeslots

        print("What timeslots is %s busy (-1 to move on)?" % name)
        busy_slot = int(input())
        while busy_slot != -1:
            names[name][busy_slot - 1] = True 
            busy_slot = int(input())

    return (names, meeting_length)

def read_doodle():
    names = dict()
    # TODO: use OpenPyXl to read an excel file from doodle
    meeting_length = int(input("How many timeslots are required for a meeting? "))
    return (names, meeting_length)
        
def generate_ordinal(num):
    """Generates the ordinal equivalent of the given cardinal number"""
    last_1 = num % 10
    last_2 = num % 100
    if last_1 == 1 and not last_2 == 11:
        return "%sst" % num
    if last_1 == 2 and not last_2 == 12:
        return "%snd" % num
    if last_1 == 3 and not last_2 == 13:
        return "%srd" % num
    return "%sth" % num