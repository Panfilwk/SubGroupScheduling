import sys

def read_cli_input():
    """Prompt the user for initial schedule info via command line"""
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
    """Read initial schedule data from an excel file exported by Doodle"""
    names = dict()
    # TODO: use OpenPyXl to read an excel file from doodle
    return names

def generate_yices_base(yices, names):
    """Generate yices code describing people's initial schedule constraints"""
    for (name, schedule) in names.items():
        print("(define %s :: (bitvector %s))" % (name, len(schedule)), file=yices)
        for busy_slot in [i for i, v in enumerate(schedule) if v]:
            print("(assert (not (bit %s %s)))" % (name, busy_slot), file=yices)

def define_meetings(names):
    """Prompts user to define meeting participants and times via command line"""
    num_meetings = 1
    meetings = list()
    while True:
        print("Who is involved in the %s meeting?" % generate_ordinal(num_meetings))
        print(["%s: %s" % (i+1, v) for i, v in enumerate(names)])
        members = set()

        member = input()
        while member != '':
            # convert the text input to a zero-indexed position
            member = int(member) - 1
            if member < 0 or member >= len(names):
                member = input()
                continue
            members.add(names[member])
            member = input()

        time_slots = int(input("How many timeslots are required for this meeting? "))

        meetings.append((members, time_slots))

        more = None
        while more != 'y' and more != 'n':
            more = input("Create another meeting? (y/n) ")
        if more == 'n':
            break
    return meetings

def generate_yices_meetings(yices, meetings):
    """Generate yices code describing how meetings must be scheduled"""
    for idx, meeting in enumerate(meetings):
        print("(define m%s :: int)" % idx, file=yices)
        names = ' '.join(meeting[0])
        print("(assert (= (bv-redand (bv-extract (+ m%s %s) m%s (bv-and %s))) 0b0))"
              % (idx, meeting[1], idx, names), file=yices)

def generate_ordinal(num):
    """Generate the ordinal equivalent of the given cardinal number"""
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
    # names = read_cli_input()
    # generate_yices_base(sys.stdout, names)
    meetings = define_meetings(['alice', 'bob', 'charlie'])
    generate_yices_meetings(sys.stdout, meetings)

driver()
