import sys
from math import log

def read_cli_input():
    """Prompt the user for initial schedule info via command line"""
    num_participants = int(input("How many people? "))
    timeslots = int(input("How many possible timeslots are there? "))

    schedules = dict()
    for num in range(num_participants):
        name = input("What's the %s name? " % generate_ordinal(num+1))
        schedules[name] = [False]*timeslots

        print("Which timeslots is %s busy?" % name)
        busy_slot = input()
        while busy_slot != '':
            # convert the text input to a zero-indexed position
            busy_slot = int(busy_slot) - 1
            if busy_slot < 0 or busy_slot >= len(schedules[name]):
                busy_slot = input()
                continue
            schedules[name][busy_slot] = True
            busy_slot = input()

    return (schedules, timeslots)

def read_doodle():
    """Read initial schedule data from an excel file exported by Doodle"""
    schedules = dict()
    # TODO: use OpenPyXl to read an excel file from doodle
    return schedules

def generate_yices_base(yices, schedules):
    """Generate yices code describing people's initial schedule constraints"""
    for (name, schedule) in schedules.items():
        types = ' '.join(["int"] * len(schedule))
        print("(define %s :: (tuple %s))" % (name, types), file=yices)
        for busy_slot in [i for i, v in enumerate(schedule) if v]:
            print("(assert (= (select %s %s) -1))" % (name, busy_slot + 1), file=yices)

def define_meetings(names):
    """Prompts user to define meeting participants and times via command line"""
    names = [name for name in names]
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

def generate_yices_meetings(yices, meetings, length):
    """Generate yices code describing how meetings must be scheduled"""
    for idx, meeting in enumerate(meetings):
        names = meeting[0]
        m_length = meeting[1]

        time_slots = ["(and %s)"
                      % ' '.join(["(= %s (select %s %s))"
                                  % (idx + 1, name, i + 1)
                                  for name in names])
                      for i in range(length)]
        meeting_times = ["\n\t(and %s)"
                         % ' '.join(time_slots[i:i + m_length])
                         for i in range(length - m_length + 1)]
        print("(assert (or %s))" % ''.join(meeting_times), file=yices)

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
    (schedules, length) = read_cli_input()
    meetings = define_meetings(schedules.keys())
    generate_yices_base(sys.stdout, schedules)
    generate_yices_meetings(sys.stdout, meetings, length)

driver()
