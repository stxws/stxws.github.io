---
title: 'POJ-1251 Jungle Roads'
date: 2020-04-08 16:47:21
categories: acm
tags: [acm,poj,最小生成树]
---
最小生成树问题-Kruskal算法
<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=1251>

# 题意
&emsp;&emsp;给出地图上的n个村庄，村庄之间存在一些双向路径，每条路径有一个权值。需要选出一些路径，使得所有的村庄之间可以相互连通，且选出路径的权值和要最小，求出最小的权值和。

# 题目解析
&emsp;&emsp;最小生成树的模板题，可以用Prim算法或者Kruskal算法求解，这里用的是Kruskal算法。
&emsp;&emsp;有个奇怪的问题，用c语言的`scanf()`来输入字符的话会Runtime Error，用c++的cin就没问题。

# 代码
```cpp
/* http://poj.org/problem?id=1251 */
/* AC 0MS 716K */
#include <stdio.h>
#include <iostream>
#include <algorithm>

using namespace std;

const int MAX_N = 30;

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

int main()
{
	int n, m;
	int i, j, k, w, ans;
	char a, b;
	edge e[MAX_N * MAX_N];

	// while(scanf("%d", &n) != EOF && n > 0)
	while(cin >> n && n > 0)
	{
		m = 0;
		for(i = 0; i < n - 1; i++)
		{
			// getchar();
			// scanf("%c %d", &a, &k);
			cin >> a >> k;
			for(j = 0; j < k; j++)
			{
				// getchar();
				// scanf("%c %d", &b, &w);
				cin >> b >> w;
				e[m] = (edge){a - 'A', b - 'A', w};
				m++;
			}
		}

		ans = kruskal(e, n, m);
		printf("%d\n", ans);
	}
	return 0;
}

/*
9
A 2 B 12 I 25
B 3 C 10 H 40 I 8
C 2 D 18 G 55
D 1 E 44
E 2 F 60 G 38
F 0
G 1 H 35
H 1 I 35
3
A 2 B 10 C 40
B 1 C 20
0

*/

```