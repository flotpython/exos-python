from graphs import shortest_path1, planar1

N = 30
P = planar1(N)
print(shortest_path1(P, (1, 1), (N, N)))
