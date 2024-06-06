def decisionVariables(M, m, n, t, d, x, y, z, s):
    ''' decision variable: delta '''
    for i in range(n):
        d[i] = M.NewBoolVar("d%d" % (i))

    '''decision variable x'''
    for i in range(m):
        for j in range(n):
            x[i, j] = M.NewBoolVar('x%d,%d' % (i, j))

    '''decision variable y'''
    for i in range(m):
        for j in range(n + 1):  # +1 is for depot
            for k in range(t):
                y[i, j, k] = M.NewBoolVar('y%d,%d,%d' % (i, j, k))

    '''variable z'''
    for i in range(m):
        for j in range(n + 1):
            for l in range(n + 1):
                for k in range(t):
                    z[i, j, l, k] = M.NewBoolVar("z%d,%d,%d,%d" % (i, j, l, k))

    '''variable s'''
    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                s[i, j, k] = M.NewIntVar(0,10000,"s%d,%d,%d" % (i, j, k))