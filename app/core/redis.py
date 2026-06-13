# INF = 9999999
#
# nodes, lines = map(int, input().split())
# start_node = int(input())
#
# d_list = [[INF for _ in range(nodes)] for _ in range(nodes)]
#
# for i in range(lines):
#     st, ed, cost = map(int, input().split())
#     st, ed, cost = st - 1, ed - 1, cost
#
#     d_list[st][st] = 0
#     d_list[ed][ed] = 0
#
#     d_list[st][ed] = min(d_list[st][ed], cost)
#     d_list[ed][st] = min(d_list[ed][st], cost)
#
#
# for i in range(nodes):
#     k = INF
#     for j in range(nodes):
#         if d_list[i][j] != 0 and d_list < k:
#             k = d_list[i][j]
#
#     for j in range(nodes):
#
#
#
# for i in range(nodes):
#     for j in range(nodes):
#         print(d_list[i][j], end=' ')
#     print()