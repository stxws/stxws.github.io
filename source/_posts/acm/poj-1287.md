---
title: 'POJ-1287 Networking'
date: 2020-04-10 08:57:52
categories: acm
tags: [acm,poj,最小生成树]
---
最小生成树问题
<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=1287>

# 题意
&emsp;&emsp;给出P个节点和R条边的无向图，求最小生成树。

# 题目解析
&emsp;&emsp;最小生成树的模板题，可以用Prim算法或者Kruskal算法求解，Prim算法适合稠密图（点少边多），Kruskal算法适合稀疏图（点多边少）。

# 代码
Prim算法
```cpp
/* http://poj.org/problem?id=1287 */
/* AC 16MS 380K */
#include <stdio.h>
#include <string.h>

const int MAX_N = 50 + 10;

int prim(int mp[][MAX_N], int n)
{
	int i, j, k, min, ans;
	int book[MAX_N];
	int tree[MAX_N];
	int dist[MAX_N];

	for(i = 1; i < n; i++)
	{
		book[i] = 0;
		tree[i] = 0;
		dist[i] = mp[0][i];
	}
	book[0] = 1;
	tree[0] = -1;

	ans = 0;
	for(i = 1; i < n; i++)
	{
		min = 0x1f1f1f1f;
		k = -1;
		for(j = 1; j < n; j++)
		{
			if(book[j] == 0 && min > dist[j])
			{
				k = j;
				min = dist[j];
			}
		}
		if(k == -1)
		{
			return -1;
		}
		book[k] = 1;
		ans += mp[tree[k]][k];
		for(j = 1; j < n; j++)
		{
			if(book[j] == 0 && mp[k][j] < dist[j])
			{
				dist[j] = mp[k][j];
				tree[j] = k;
			}
		}
	}
	return ans;
}

int main()
{
	int n, m;
	int i, a, b, w, ans;
	int mp[MAX_N][MAX_N];

	while(scanf("%d", &n) != EOF && n > 0)
	{
		scanf("%d", &m);
		memset(mp, 0x1f, sizeof(mp));
		for(i = 0; i < m; i++)
		{
			scanf("%d %d %d", &a, &b, &w);
			a -= 1;
			b -= 1;
			if(w < mp[a][b])
			{
				mp[a][b] = w;
				mp[b][a] = w;
			}
		}

		ans = prim(mp, n);
		printf("%d\n", ans);
	}
	return 0;
}

```

Kruskal算法
```cpp
/* http://poj.org/problem?id=1287 */
/* AC 16MS 400K */
#include <stdio.h>
#include <algorithm>

using namespace std;

const int MAX_N = 50 + 10;

typedef struct edge
{
	int a, b, w;
} edge;

int cmp(edge a, edge b)
{
	return a.w < b.w;
}

int find_root(int set[], int i)
{
	if(set[i] != i)
	{
		set[i] = find_root(set, set[i]);
	}
	return set[i];
}

int kruskal(edge e[], int n, int m)
{
	int i, k, ar, br;
	int ans = 0;
	int set[MAX_N];

	sort(e, e + m, cmp);
	for(i = 0; i < MAX_N; i++)
	{
		set[i] = i;
	}
	k = 1;
	for(i = 0; i < m && k < n; i++)
	{
		ar = find_root(set, e[i].a);
		br = find_root(set, e[i].b);
		if(ar != br)
		{
			set[ar] = br;
			ans += e[i].w;
			k++;
		}
	}
	if(k < n)
	{
		return -1;
	}
	return ans;
}

int n, m;
edge e[MAX_N * MAX_N];

int main()
{
	int i, a, b, w, ans;

	while(scanf("%d", &n) != EOF && n > 0)
	{
		scanf("%d", &m);
		for(i = 0; i < m; i++)
		{
			scanf("%d %d %d", &a, &b, &w);
			e[i] = (edge){a, b, w};
		}

		ans = kruskal(e, n, m);
		printf("%d\n", ans);
	}
	return 0;
}

```