'''objective funtion - 1'''
def objectiveFunction(M,d,n):
    M.Maximize(sum([d[j] for j in range(n)]))
