import time

slots = ["S1","S2","S3","S4"]

domains = {
    "S1": ["A","B","C"],
    "S2": ["A","B","C"],
    "S3": ["A","B","C"],
    "S4": ["A","B"]   # C not allowed
}

assignment_count = 0

# ---------------- CONSTRAINT CHECK ----------------
def is_valid(assignment, var, value):

    # No back-to-back constraint
    if var == "S2" and assignment.get("S1") == value:
        return False
    if var == "S3" and assignment.get("S2") == value:
        return False
    if var == "S4" and assignment.get("S3") == value:
        return False

    return True


# ---------------- BACKTRACK ----------------
def backtrack(assignment):
    global assignment_count

    # Goal test
    if len(assignment) == len(slots):
        if set(assignment.values()) == {"A","B","C"}:
            return assignment
        return None

    # MRV heuristic
    var = min([v for v in slots if v not in assignment],
              key=lambda v: len(domains[v]))

    for value in domains[var]:
        if is_valid(assignment, var, value):
            assignment[var] = value
            assignment_count += 1

            result = backtrack(assignment)
            if result:
                return result

            del assignment[var]

    return None


# ---------------- MAIN ----------------
if __name__ == "__main__":
    start = time.time()

    result = backtrack({})

    end = time.time()

    print("\n===== CSP RESULT =====")
    print("Status:", "Success" if result else "Failure")
    print("Heuristic Used: MRV")
    print("Inference Method: Backtracking")
    print("Constraints:")
    print(" - No Back-to-Back")
    print(" - Slot4 != C")
    print(" - Minimum Coverage (A,B,C used)")
    print("Final Assignment:", result)
    print("Total Assignments Tried:", assignment_count)
    print("Time Taken:", end - start)
