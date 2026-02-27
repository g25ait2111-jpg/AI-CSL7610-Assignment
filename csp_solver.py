import time

# =====================================
# GLOBAL VARIABLES (filled from input)
# =====================================
slots = []
bots = []
domains = {}
assignment_count = 0


# =====================================
# READ INPUT FILE
# =====================================
def read_input(filename):

    global slots, bots, domains

    with open(filename, "r") as file:
        lines = file.readlines()

    bots = lines[0].split(":")[1].strip().split()
    slots = lines[1].split(":")[1].strip().split()

    # Create domains
    for s in slots:
        domains[s] = bots.copy()

    # Unary constraint: Slot4 != C
    if "S4" in domains and "C" in domains["S4"]:
        domains["S4"].remove("C")


# =====================================
# CONSTRAINT CHECK
# =====================================
def is_valid(assignment, var, value):

    # No Back-to-Back constraint
    index = slots.index(var)

    # Check previous slot
    if index > 0:
        prev_slot = slots[index - 1]
        if assignment.get(prev_slot) == value:
            return False

    # Check next slot
    if index < len(slots) - 1:
        next_slot = slots[index + 1]
        if assignment.get(next_slot) == value:
            return False

    return True


# =====================================
# MRV HEURISTIC
# =====================================
def select_unassigned_variable(assignment):
    unassigned = [v for v in slots if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))


# =====================================
# BACKTRACKING SEARCH
# =====================================
def backtrack(assignment):

    global assignment_count

    # Goal Test
    if len(assignment) == len(slots):

        # Minimum coverage constraint
        if set(assignment.values()) == set(bots):
            return assignment
        return None

    var = select_unassigned_variable(assignment)

    for value in domains[var]:

        if is_valid(assignment, var, value):

            assignment[var] = value
            assignment_count += 1

            result = backtrack(assignment)
            if result:
                return result

            del assignment[var]

    return None


# =====================================
# MAIN PROGRAM
# =====================================
if __name__ == "__main__":

    # Read CSP input
    read_input("csp_input.txt")

    print("===================================")
    print("CSP Problem: Security Bot Scheduling")
    print("Bots:", bots)
    print("Slots:", slots)
    print("Heuristic Used: MRV")
    print("Inference Method: Backtracking")
    print("Constraints Applied:")
    print(" - No Back-to-Back")
    print(" - Slot4 != C")
    print(" - Minimum Coverage (All bots used)")
    print("===================================")

    start_time = time.time()

    result = backtrack({})

    end_time = time.time()

    # Ordered output
    if result:
        ordered = {s: result[s] for s in slots}
        print("Status: Success")
        print("Final Assignment:", ordered)
    else:
        print("Status: Failure")

    print("Total Assignments Tried:", assignment_count)
    print("Total Time Taken:", round(end_time - start_time, 6), "seconds")