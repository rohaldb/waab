def get_schedule(courses):
    pairs = unroll(courses)
    n = len(pairs)
    return find_order(n, pairs)

"""
eg. courses:
{ COMP3121: [COMP1917, COMP1927]}
"""
def unroll(courses):
    output = []
    for c in courses:
        for p in c:
            output.append([c, p])
    return output

"""
assumes input is:
[course, prereq]
"""
def find_order(n, pairs):
    graph = [[] for _ in range(n)]
    outdegree = [0] * n

    for course, pre in pairs:
        graph[course].append(pre)
        outdegree[pre] += 1

    bfs = [
        course
        for course in range(n)
        if outdegree[course] == 0 # This course is not a prereq for anything
    ]
    for course in bfs:
        for pre in graph[course]:
            outdegree[pre] -= 1
            if outdegree[pre] == 0:
                bfs.append(pre)

    return bfs[::-1] if len(bfs) == n else []
