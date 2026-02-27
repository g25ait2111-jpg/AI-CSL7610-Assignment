import time

# ===============================
# Read Input File
# ===============================

def read_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    bots = lines[0].split(":")[1].strip().split()
    slots_count = int(lines[1].split(":")[1].strip())

    slots = [f"S{i+1}" for i in range(slots_count)]

    domains = {slot: bots[:] for slot in slots}

    # Apply unary constraint (Slot4 != C)
    if "Slot4 != C" in lines[3]:
        domains["S4"].remove("C")

    return slots, domains


# ===============================
# CSP Solver
# ===============================

assignment_count = 0

def is_valid(assignment, var, value):
    idx = int(var[1]) - 1

    # No Back-to-Back constraint
    if idx > 0:
        prev_slot = f"S{idx}"
        if prev_slot in assignment and assignment[prev_slot] == value:
            return False

    return True


def forward_check(domains, var, value):
    idx = int(var[1]) - 1
    next_slot = f"S{idx+2}"

    if next_slot in domains:
        if value in domains[next_slot]:
            domains[next_slot] = [v for v in domains[next_slot] if v != value]
            if not domains[next_slot]:
                return False
    return True


def backtrack(assignment, slots, domains):
    global assignment_count

    if len(assignment) == len(slots):
        if set(assignment.values()) == {"A", "B", "C"}:
            return assignment
        return None

    # MRV heuristic
    unassigned = [v for v in slots if v not in assignment]
    var = min(unassigned, key=lambda v: len(domains[v]))

    for value in domains[var]:
        if is_valid(assignment, var, value):
            assignment[var] = value
            assignment_count += 1

            # Copy domains for forward checking
            new_domains = {k: domains[k][:] for k in domains}

            if forward_check(new_domains, var, value):
                result = backtrack(assignment, slots, new_domains)
                if result:
                    return result

            del assignment[var]

    return None


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    slots, domains = read_input()

    print("========================================")
    print("CSP Solver")
    print("Heuristic Used: MRV")
    print("Inference Method: Forward Checking")
    print("Constraints Applied:")
    print("- No Back-to-Back")
    print("- Slot4 != C")
    print("- All bots must be used at least once")
    print("========================================")

    start_time = time.time()
    result = backtrack({}, slots, domains)
    end_time = time.time()

    if result:
        print("Status: Success")
        print("Final Assignment:", result)
    else:
        print("Status: Failure")

    print("Total Assignments Tried:", assignment_count)
    print("Total Time Taken:", round(end_time - start_time, 5), "seconds")
