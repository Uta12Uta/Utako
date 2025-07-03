import sys, math
from scipy.spatial import KDTree
import functools
from common import read_input, print_tour

# --- 基本関数 ---
def distance(p1, p2):
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    return math.hypot(dx, dy)

def path_length(path):
    return sum(distance(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

# --- 分割統治によるTSP構築 ---
def divide_direction(buff):
    x_coords, y_coords = zip(*buff)
    return max(x_coords) - min(x_coords) > max(y_coords) - min(y_coords)

def divide(buff, comp):
    buff.sort(key=functools.cmp_to_key(comp))
    n = len(buff) // 2
    return buff[n], buff[:n+1], buff[n:]

def differ(p, c, q):
    return distance(p, c) + distance(c, q) - distance(p, q)

def search(x, buff):
    for i in range(len(buff)):
        if buff[i] == x:
            if i == 0: return len(buff) - 1, i, i + 1
            if i == len(buff) - 1: return i - 1, i, 0
            return i - 1, i, i + 1

def make_new_path(buff, c, succ):
    path = []
    i = c + succ
    while True:
        if i < 0: i = len(buff) - 1
        elif i >= len(buff): i = 0
        if i == c: break
        path.append(buff[i])
        i += succ
    return path

def merge(buff1, buff2, p):
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

def divide_merge(buff):
    if len(buff) <= 3:
        return buff
    else:
        if divide_direction(buff):
            p, b1, b2 = divide(buff, lambda x, y: x[0] - y[0])
        else:
            p, b1, b2 = divide(buff, lambda x, y: x[1] - y[1])
        b3 = divide_merge(b1)
        b4 = divide_merge(b2)
        return merge(b3, b4, p)

# --- 2-opt 最適化 ---
def vec(a, b, cities, order):
    x1, y1 = cities[order[a]]
    x2, y2 = cities[order[b]]
    return (x2 - x1, y2 - y1)

def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def exchange(cities, order):
    changed = False
    for i in range(len(order) - 1):
        for j in range(i + 2, len(order) - 1):
            a, b = order[i], order[i+1]
            c, d = order[j], order[j+1]
            ab = vec(i, i+1, cities, order)
            ac = vec(i, j, cities, order)
            ad = vec(i, j+1, cities, order)
            cd = vec(j, j+1, cities, order)
            ca = vec(j, i, cities, order)
            cb = vec(j, i+1, cities, order)
            cp1, cp2 = cross(ab, ac), cross(ab, ad)
            cp3, cp4 = cross(cd, ca), cross(cd, cb)
            if cp1 * cp2 < 0 and cp3 * cp4 < 0:
                order[i+1:j+1] = reversed(order[i+1:j+1])
                changed = True
    return changed

# --- 最終統合関数 ---
def solve_with_divide_and_opt(cities):
    path = divide_merge(cities)  # 座標順で並んだ初期経路
    order = [cities.index(p) for p in path]  # 順序をインデックスに変換
    while exchange(cities, order):  # 2-opt 最適化
        pass
    return order

# --- 実行 ---
if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
