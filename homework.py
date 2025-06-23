import sys

from common import print_tour, read_input
from scipy.spatial import KDTree

#open_fileのやつはcites =[]dでリスト化しておく


def vec(a, b, cities, order):
    x1, y1 = cities[order[a]]
    x2, y2 = cities[order[b]]
    return (x2 - x1, y2 - y1)

def cross(v1, v2):
    return v1[0]*v2[1] - v1[1]*v2[0]

#open_fileのやつはcites =[]でリスト化しておく
def exchange(cities, order): #交差していたらそれを入れ替えるプログラム
  for i in range(len(order)-1):
    for j in range(i+2, len(order)-1):
        a, b = order[i], order[i+1]
        c, d = order[j], order[j+1]

            # ベクトルを作る
        ab = vec(i, i+1, cities, order)
        ac = vec(i, j, cities, order)
        ad = vec(i, j+1, cities, order)
        cd = vec(j, j+1, cities, order)
        ca = vec(j, i, cities, order)
        cb = vec(j, i+1, cities, order)

            # 外積で交差判定
        cp1 = cross(ab, ac)
        cp2 = cross(ab, ad)
        cp3 = cross(cd, ca)
        cp4 = cross(cd, cb)

        if cp1 * cp2 < 0 and cp3 * cp4 < 0:
           order[i+1:j+1] = reversed(order[i+1:j+1]) #交差したら反転させる
 



def solve(cities):
  order =[] #行く順番
  query_points =(cities[0][0],cities[0][1]) #スタートから始める
  order.append(0)
  new_points = cities.copy()
  while len(new_points)>1:
    new_points.remove(query_points) #new_pointsから取り除いてループする
    Tree = KDTree(new_points)
    distance,index = Tree.query(query_points)  #これにより一番近い点を見つける
    order.append(cities.index(new_points[index]))  #orderに入れていく
    query_points = new_points[index]  #調べたいポイント
  for _ in range(10):
    exchange(cities, order)
  return order#最後に一つ残るやつを入れる
#交差しているところがあれば入れ替える





 
    #貪欲法を用いる
#とにかくその時いちばん近いところに行く



#交差しているところがあれば入れ替える


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
