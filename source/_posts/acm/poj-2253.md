---
title: 'POJ-2253 Frogger'
date: 2020-04-02 17:06:58
categories: acm
tags: [acm,poj,最短路]
---
单源最短路径变形-dijkstra算法
<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=2253>

# 题意
&emsp;&emsp;湖上有n个石头，青蛙Freddy坐在1号石头上，青蛙Fiona坐在2号石头上，青蛙Freddy想要到Fiona的2号石头上（应该是只绅士青蛙）。但是湖水被污染了，他要尽量避免游泳，因此他需要利用其他石头来中转，与普通的路径长度定义不同，这里路径的长度定义为相邻两个石头距离的最大值。题目要求找出一条最短的路径，输出路径长度。

# 题目解析
&emsp;&emsp;解题方法与使用dijkstra算法解决普通单源最短路径问题类似，但是因为路径长度的定义不同，所以在初始化起点到其他节点的路径长度，和更新到其他点的最短路径的时候需要改一下。

# 代码
```cpp
/* http://poj.org/problem?id=2253 */
/* AC 0MS 336K */
#include <stdio.h>
#include <math.h>

const int MAX_N = 200 + 10;

typedef struct point
{
	int x, y;
	double distance(point p)
	{
		return sqrt((x - p.x) * (x - p.x) + (y - p.y) * (y - p.y));
	}
} point;

int n;
point p[MAX_N];

double dijkstra(int start, int end)
{
	int i, j, k;
	double min, max;
	int book[MAX_N];
	double dist[MAX_N];

	for(i = 0; i <= n; i++)
	{
		dist[i] = p[start].distance(p[i]);
		book[i] = 0;
	}
	dist[start] = 0.0;
	book[start] = 1;

	for(i = 1; i < n; i++)
	{
		min = 1e10;
		for(j = 0; j < n; j++)
		{
			if(book[j] == 0 && dist[j] < min)
			{
				min = dist[j];
				k = j;
			}
		}
		if(k == end)
		{
			return dist[k];
		}
		book[k] = 1;
		for(j = 0; j < n; j++)
		{
			if(book[j] == 0)
			{
				/* 计算起点经过k点到达j点的路径最大值 */
				max = p[k].distance(p[j]);
				if(dist[k] > max)
				{
					max = dist[k];
				}
				if(dist[j] > max)
				{
					dist[j] = max;
				}
			}
		}
	}
	return -1;
}

int main()
{
	int i, t;
	double ans;

	for(t = 1; scanf("%d", &n) != EOF && n >= 2; t++)
	{
		for(i = 0; i < n; i++)
		{
			scanf("%d %d", &p[i].x, &p[i].y);
		}
		ans = dijkstra(0, 1);
		printf("Scenario #%d\n", t);
		printf("Frog Distance = %.3f\n\n", ans);
	}
	return 0;
}

```