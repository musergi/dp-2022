import argparse
import pandas
import random
import json
from collections import Counter


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


def mdav(df, k):
    df = df.copy()
    clusters = []
    while len(df) >= 3 * k:
        farthest = get_max_dist(df, df.mean())
        other = get_max_dist(df, df.loc[farthest])
        farthest_group = get_closest(df, farthest, k - 1) + [farthest]
        other_group = get_closest(df, other, k - 1) + [other]
        clusters.append(farthest_group)
        clusters.append(other_group)
        df = df.drop(farthest_group + other_group)
    if len(df) >= 2 * k:
        farthest = get_max_dist(df, df.mean())
        farthest_group = get_closest(df, farthest, k - 1) + [farthest]
        clusters.append(farthest_group)
        df = df.drop(farthest_group)
        clusters.append(list(df.index))
    else:
        clusters.append(list(df.index))
    return clusters


parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)
parser.add_argument('--k', required=True, type=int)
parser.add_argument('--display', action='store_true')
args = parser.parse_args()

df = pandas.read_csv(args.file, index_col=0)

df = (df - df.mean()) / df.std()
dfc = df.copy()

if args.display:
    df = df.drop(df.columns[2:], axis=1)

clusters = mdav(df, args.k)

dfc['cluster'] = -1
for index, cluster in enumerate(clusters):
    dfc.loc[cluster] = dfc.loc[cluster].mean().values
    dfc.loc[cluster, 'cluster'] = index
    

dfc.drop('cluster', axis=1).to_csv(args.file + '.anon.csv')
cluster_filepath = args.file + '.cluster.csv'
dfc['cluster'].to_csv(cluster_filepath)

diff = (df - dfc.drop('cluster', axis=1))
sse = sum((diff * diff).sum())
diff = df - df.mean()
sst = sum((diff * diff).sum())

print(f'Cluster count: {len(clusters)}')
print(f'Clusters: {cluster_filepath}')
counter = Counter(list(map(len, clusters)))
print(f'Records in cluster:')
for size, count in counter.items():
    s = '' if count == 1 else 's'
    print(f'\t{count} cluster{s} with size {size}')

print(f'SSE: {sse}')
print(f'SST: {sst}')
print(f'Loss: {sse / sst}')

if args.display:
    import matplotlib.pyplot as plt
    dfc['c'] = 'black'
    for cluster in clusters:
        color = random.randint(0, 2 ** (8 * 3))
        c_str = f'#{color:06X}'
        dfc.loc[cluster, 'c'] = c_str
    dfc.plot.scatter(dfc.columns[0], dfc.columns[1], c='c')
    s = min(df[dfc.columns[0]].min(), df[dfc.columns[1]].min()) - 0.1
    e = max(df[dfc.columns[0]].max(), df[dfc.columns[1]].max()) + 0.1
    plt.xlim(s, e)
    plt.ylim(s, e)
    plt.show()
