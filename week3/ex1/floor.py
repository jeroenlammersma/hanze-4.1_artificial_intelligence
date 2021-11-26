import itertools

people = (
    'L',
    'M',
    'N',
    'E',
    'J'
)

for p in list(itertools.permutations(people)):
    # Loes does not live on top floor
    if p[4] == 'L': continue

    # Marja does not live on ground floor
    if p[0] == 'M': continue

    # Niels does not live on ground floor nor top floor
    if p[0] == 'N' or p[4] == 'N': continue

    # Erik lives atleast one floor above Marja
    if p.index('E') < p.index('M'): continue
    
    # Joep does not live on a floor underneath or above Niels
    idx_n = p.index('N')
    idx_j = p.index('J')
    if idx_j == idx_n - 1 or idx_j == idx_n + 1: continue

    # Niels does not live on a floor underneath or above Marja
    idx_m = p.index('M')
    if idx_n == idx_m - 1 or idx_n == idx_m + 1: continue

    # print floors
    floors = { i: p[i] for i in range(5) }
    print(floors)
