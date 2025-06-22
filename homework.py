import sys

from common import print_tour, read_input
from scipy.spatial import KDTree

#open_fileのやつはcites =[]dでリスト化しておく


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


  return order#最後に一つ残るやつを入れる




 
    #貪欲法を用いる
#とにかくその時いちばん近いところに行く



#交差しているところがあれば入れ替える


if __name__ == '__main__':
    tour = solve(read_input("input_0.csv"))
    print_tour(tour)
