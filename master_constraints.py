from ortools.sat.python import cp_model

def masterConstraints(M, d, x, y, m, n, t, q, q2, q3, Q, nN, f):
    '''constraint 2'''

    for j in range(n):
        constraint = sum([x[i,j] for i in range(m)]) == nN[j+1] * d[j]
        M.Add(constraint)

    '''constraint 2'''
    for j in range(n):
        constraint = sum(sum(y[i, j + 1, k] for k in range(t)) for i in range(m)) == nN[j+1] * f[j+1] * d[j]
        M.Add(constraint)
    '''constraint 3'''
    for i in range(m):
        for j in range(n):
            for k in range(t):
                M.Add(y[i, j + 1, k] <= x[i, j])

    '''constraint 4'''
    for i in range(m):
        for j in range(n):
            if q[j+1] != Q[i] and q2[j+1] != Q[i] and q3[j+1] != Q[i]:
                M.Add(x[i, j] == 0)


    '''constraint 5'''
    for i in range(m):
        for k in range(t):
            M.Add(y[i, 0, k] == 1)  # j = 0 for depot location
            M.Add(y[i, 0, k] == 1)


    '''constraint 6'''
    for i in range(m):
        for j in range(n):
            for k in range(t):
                for tou in range(1, (4 - (f[j+1]) + 1)):
                    if (k + tou) <= 4:
                        M.Add(y[i, j + 1, k] + y[i, j + 1, k + tou] <= 1)

