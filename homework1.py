import sys, math
from scipy.spatial import KDTree
import functools
from common import read_input, print_tour

import math

def split_4(points):#4つに分ける
    cx = sum(p[0] for p in points) / len(points) #xの重心座標
    cy = sum(p[1] for p in points) / len(points) #yの重心座標
    q1, q2, q3, q4 = [], [], [], []
    for p in points:
        if p[0] >= cx and p[1] >= cy: #第1象限
            q1.append(p)
        elif p[0] < cx and p[1] >= cy: #第2象限
            q2.append(p)
        elif p[0] < cx and p[1] < cy: #第3象限
            q3.append(p)
        else:                          #第4象限
            q4.append(p)
    return [q1, q2, q3, q4]


def distance(p1, p2):       #距離を測定する
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.hypot(dx, dy)  # sqrt(dx^2 + dy^2)


def greedy_tour(points):#貪欲法

    def solve(cities): #
        order = []
        query_point = cities[0]
        order.append(0)

        visited = [False] * len(cities)
        visited[0] = True

        while len(order) < len(cities):
            # 未訪問の点だけを使ってKDTreeを構築
            remaining_points = [p for i, p in enumerate(cities) if not visited[i]]
            Tree = KDTree(remaining_points)
            _, idx = Tree.query(query_point)
            next_point = remaining_points[idx]
            next_index = cities.index(next_point)

            order.append(next_index)
            visited[next_index] = True
            query_point = next_point

        return order
    return solve(points)



def two_opt(points, order): #2-opt、外積判断
    def vec(i, j): 
        x1, y1 = points[order[i]]
        x2, y2 = points[order[j]]
        return (x2 - x1, y2 - y1)

    def cross(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    changed = False
    for i in range(len(order) - 1):
        for j in range(i + 2, len(order) - 1):
            a, b = order[i], order[i + 1]
            c, d = order[j], order[j + 1]
            ab = vec(i, i + 1)
            ac = vec(i, j)
            ad = vec(i, j + 1)
            cd = vec(j, j + 1)
            ca = vec(j, i)
            cb = vec(j, i + 1)

            cp1, cp2 = cross(ab, ac), cross(ab, ad)
            cp3, cp4 = cross(cd, ca), cross(cd, cb)

            if cp1 * cp2 < 0 and cp3 * cp4 < 0:
                order[i + 1:j + 1] = reversed(order[i + 1:j + 1])
                changed = True
    return changed



def merge_subpaths(points, subpaths, shared_indices): #4分割を統合する
    
    def idx_to_coords(order):　
        return [points[i] for i in order]

    def coords_to_idx(path):
        return [points.index(p) for p in path]

    def search(p, buff):　　　　#共有点を見つける
        for i in range(len(buff)):
            if buff[i] == p:
                if i == 0: 
                  return len(buff) - 1, i, i + 1
                if i == len(buff) - 1: 
                  return i - 1, i, 0
                else:
                  return i - 1, i, i + 1

    def differ(p, c, q):　　#差分を求める
        return distance(p, c) + distance(c, q) - distance(p, q)

    def make_new_path(buff, c, succ):　#挿入するために新しい経路を作る
        path = []
        i = c + succ
        while True:
            if i < 0: i = len(buff) - 1
            elif i >= len(buff): i = 0
            if i == c: break
            path.append(buff[i])
            i += succ
        return path

    def merge_paths(buff1, buff2, p):　#4つに分割したものをつなげる
        p1, i1, n1 = search(p, buff1)
        p2, i2, n2 = search(p, buff2)
        d1 = differ(buff1[p1], p, buff2[p2])
        d2 = differ(buff1[n1], p, buff2[n2])
        d3 = differ(buff1[p1], p, buff2[n2])
        d4 = differ(buff1[n1], p, buff2[p2])
        d = max(d1, d2, d3, d4)
        if d1 == d:
            buff1[i1:i1] = make_new_path(buff2, i2, -1)
        elif d2 == d:
            buff1[n1:n1] = make_new_path(buff2, i2, -1)
        elif d3 == d:
            buff1[i1:i1] = make_new_path(buff2, i2, 1)
        else:
            buff1[n1:n1] = make_new_path(buff2, i2, 1)
        return buff1

    merged_path = [points[i] for i in subpaths[0]]
    for sp, shared_idx in zip(subpaths[1:], shared_indices[1:]):
        candidate = idx_to_coords(sp)
        shared_point = points[shared_idx]
        merged_path = merge_paths(merged_path, candidate, shared_point)

    return coords_to_idx(merged_path)

def solve(points):
    cx = sum(p[0] for p in points) / len(points)#重心を求める
    cy = sum(p[1] for p in points) / len(points)
    shared_point = min(points, key=lambda p: distance(p, (cx, cy)))#重心に一番近い都市を求める

    subregions = split_4(points)
           
    for region in subregions:
        if shared_point not in region:
                region.append(shared_point)

    shared_idx = points.index(shared_point)

    all_paths = []
    shared_indices = [shared_idx] * len(subregions)  

    for region in subregions:
        order = greedy_tour(region)
        while two_opt(region, order):
            pass

        order_indices = [points.index(region[i]) for i in order]
        all_paths.append(order_indices)


    merged_order = merge_subpaths(points, all_paths, shared_indices) # 距離の差分が小さい順に接続
    while two_opt(points, merged_order):  #統合したものに2-optを行う
        pass

    return merged_order


# --- 実行 ---
if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
