import argparse
from re import A
import pandas
import random
import json

def get_max_dist(df, record):
    dist = (df - record)
    sq_dist = dist * dist
    sq_dist['distance'] = sq_dist.sum(axis=1)
    return int(sq_dist.distance.idxmax())

def get_closest(df, record_idx, n):
    record = df.loc[record_idx]
    df = df.drop(record_idx)
    dist = (df - record)
    sq_dist = dist * dist
    sq_dist['distance'] = sq_dist.sum(axis=1)
    return list(sq_dist.sort_values('distance').head(n).index)

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)
parser.add_argument('--k', required=True, type=int)
parser.add_argument('--display', action='store_true')
args = parser.parse_args()

df = pandas.read_csv(args.file, index_col=0)

df = (df - df.mean()) / df.std()

if args.display:
    df = df.drop(df.columns[2:], axis=1)

dfc = df.copy()

clusters = []

while len(df) >= 3 * args.k:
    farthest = get_max_dist(df, df.mean())
    other = get_max_dist(df, df.loc[farthest])
    farthest_group = get_closest(df, farthest, args.k - 1) + [farthest]
    other_group = get_closest(df, other, args.k - 1) + [other]
    clusters.append(farthest_group)
    clusters.append(other_group)
    df = df.drop(farthest_group + other_group)

if len(df) >= 2 * args.k:
    farthest = get_max_dist(df, df.mean())
    farthest_group = get_closest(df, farthest, args.k - 1) + [farthest]
    clusters.append(farthest_group)
    df = df.drop(farthest_group)
    clusters.append(list(df.index))
else:
    clusters.append(list(df.index))

print(f'Cluster count: {len(clusters)}')
print(f'Cluster: \n{json.dumps(clusters,indent=2)}')
print(f'Records in cluster: {list(map(len, clusters))}')

if args.display:
    import matplotlib.pyplot as plt
    dfc['c'] = 'black'
    for cluster in clusters:
        color = random.randint(0, 2 ** (8 * 3))
        c_str = f'#{color:06X}'
        dfc.loc[cluster, 'c'] = c_str
    dfc.plot.scatter(df.columns[0], df.columns[1], c='c')
    plt.show()