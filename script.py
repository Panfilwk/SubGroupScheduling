import sys

def read_cli_input():
    """Prompts the user for initial schedule info via command line"""
    num_participants = int(input("How many people? "))
    timeslots = int(input("How many possible timeslots are there? "))

    names = dict()
    for num in range(num_participants):
        name = input("What's the %s name? " % generate_ordinal(num+1))
        names[name] = [False]*timeslots

        print("Which timeslots is %s busy?" % name)
        busy_slot = input()
        while busy_slot != '':
            # convert the text input to a zero-indexed position
            busy_slot = int(busy_slot) - 1
            if busy_slot < 0 or busy_slot >= len(names[name]):
                busy_slot = input()
                continue
            names[name][busy_slot] = True 
            busy_slot = input()

    return names

def read_doodle():
    names = dict()
    # TODO: use OpenPyXl to read an excel file from doodle
    return names

def generate_yices_base(yices, names):
    """Generates a yices file representing people's initial schedules"""
    for (name, schedule) in names.items():
        print("(define %s :: (bitvector %s))" % (name, len(schedule)), file=yices)
        for busy_slot in [i for i, v in enumerate(schedule) if v]:
            print("(assert (not (bit %s %s)))" % (name, busy_slot), file=yices)
        
def generate_ordinal(num):
    """Generates the ordinal equivalent of the given cardinal number"""
    last_1 = num % 10
    last_2 = num % 100
    if last_1 == 1 and last_2 != 11:
        return "%sst" % num
    if last_1 == 2 and last_2 != 12:
        return "%snd" % num
    if last_1 == 3 and last_2 != 13:
        return "%srd" % num
    return "%sth" % num

def driver():
    names = read_cli_input()
    generate_yices_base(sys.stdout, names)

driver()