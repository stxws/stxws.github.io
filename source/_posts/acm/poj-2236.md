---
title: 'POJ-2236 Wireless Network'
date: 2020-04-03 10:31:09
categories: acm
tags: [acm,poj,并查集]
---
简单的并查集
<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=2236>

# 题意
&emsp;&emsp;网断了！要把网络修好，电脑是通过无线来通信的，通信范围是d。也就是如果两台电脑没坏，且之间的距离小于d，那这两台电脑就可以相互通信。
&emsp;&emsp;一共有n台电脑，初始时每台电脑都是坏的，首先给出每台电脑的坐标，然后每次可以进行两种操作：
&emsp;&emsp;&emsp;&emsp;1. 'O'操作，修好一台电脑
&emsp;&emsp;&emsp;&emsp;2. 'S'操作，测试两台电脑是否可以通信
&emsp;&emsp;输出所有的测试结果，如果可以通信输出“SUCCESS”，否则输出“FAIL”。

# 题目解析
&emsp;&emsp;简单的并查集问题，对于'O'操作，遍历所有已经修好的电脑，如果之间的距离小于d，就合并。对于'S'操作，判断两台电脑是否在一个集合里。
&emsp;&emsp;注意'O'和'S'的输入，会接收终端的换行符。

# 代码
```cpp
/* http://poj.org/problem?id=2236 */
/* AC 3329MS 328K */
#include <stdio.h>
#include <math.h>

const int MAX_N = 1000 + 10;

typedef struct point
{
	int x, y;
	double distance(point p)
	{
		return sqrt((x - p.x) * (x - p.x) + (y - p.y) * (y - p.y));
	}
} point;

int find_root(int set[], int i)
{
	if(set[i] != i)
	{
		set[i] = find_root(set, set[i]);
	}
	return set[i];
}

int main()
{
	int n, d;
	char opt;
	int i, j, a, b, ar, br;
	int set[MAX_N], book[MAX_N];
	point p[MAX_N];

	scanf("%d %d", &n, &d);
	for(i = 1; i <= n; i++)
	{
		scanf("%d %d", &p[i].x, &p[i].y);
		set[i] = i;
		book[i] = 0;
	}
	while(scanf("%c", &opt) != EOF)
	{
		if(opt == 'O')
		{
			scanf("%d", &a);
			ar = find_root(set, a);
			for(i = 1; i <= n; i++)
			{
				if(book[i] == 1 && p[i].distance(p[a]) <= (double)d)
				{
					br = find_root(set, i);
					set[br] = ar;
				}
			}
			book[a] = 1;
		}
		else if(opt == 'S')
		{
			scanf("%d %d", &a, &b);
			if(book[a] == 0 || book[b] == 0)
			{
				printf("FAIL\n");
				continue;
			}
			ar = find_root(set, a);
			br = find_root(set, b);
			if(ar == br)
			{
				printf("SUCCESS\n");
			}
			else
			{
				printf("FAIL\n");
			}
		}
	}
	return 0;
}

```
