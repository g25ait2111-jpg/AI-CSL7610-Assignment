import time

slots = ["S1","S2","S3","S4"]
domains = {
    "S1": ["A","B","C"],
    "S2": ["A","B","C"],
    "S3": ["A","B","C"],
    "S4": ["A","B"]   # C not allowed in Slot4
}

def is_valid(assignment, var, value):
    if var == "S2" and "S1" in assignment and assignment["S1"] == value:
        return False
    if var == "S3" and "S2" in assignment and assignment["S2"] == value:
        return False
    if var == "S4" and "S3" in assignment and assignment["S3"] == value:
        return False
    return True

def backtrack(assignment):
    if len(assignment) == len(slots):
        if set(assignment.values()) == {"A","B","C"}:
            return assignment
        return None

    var = min([v for v in slots if v not in assignment],
              key=lambda v: len(domains[v]))

    for value in domains[var]:
        if is_valid(assignment, var, value):
            assignment[var] = value
            result = backtrack(assignment)
            if result:
                return result
            del assignment[var]
    return None

if __name__ == "__main__":
    start = time.time()
    result = backtrack({})
    print("Solution:", result)
    print("Time:", time.time()-start)