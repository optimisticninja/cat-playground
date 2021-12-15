def damereau_levenshtein_distance(s1: str, s2: str):
    s1_len = len(s1)
    s2_len = len(s2)
    # Build out algorithm to dynamically expand list type.
    # Feels weird man.
    d = [[0 for _ in range(s2_len + 1)] for _ in range(s1_len + 1)]

    for i in range(s1_len + 1):
        d[i][0] = i
    for j in range(s2_len + 1):
        d[0][j] = j
    for i in range(s1_len + 1):
        for j in range(1, s2_len + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            d[i][j] = min(
                d[i - 1][j] + 1,  # delete
                min(d[i][j - 1] + 1,  # insert
                    d[i - 1][j - 1] + cost)  # substitution
            )

            if (i > 1) and (j > 1) and (s1[i - 1] == s2[j - 2]) and (s1[i - 2] == s2[j - 1]):
                d[i][j] = min(
                    d[i][j],
                    d[i - 2][j - 2] + cost)  # transposition
    return d[s1_len][s2_len]
