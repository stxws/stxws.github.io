---
title: 'HDU-3085 Nightmare Ⅱ'
date: 2020-02-15 16:57:20
categories: acm
tags: [acm,搜索,hdu]
---
双向广度优先搜索
<!-- more -->

# 题目
&emsp;&emsp;地址：<http://acm.hdu.edu.cn/showproblem.php?pid=3085>

# 题意
&emsp;&emsp;给出一个n×m的迷宫，迷宫里有些地方是墙，有些地方是空地，迷宫里还有两只鬼，鬼可以分身，以每秒两步的速度向附近扩散，而且鬼可以穿墙。erriyue和他的女朋友在迷宫里面，erriyue每秒钟可以走3步，他的女朋友每秒钟可以走一步。问erriyue能否在在鬼抓到他或他女朋友之前，与他女朋友会合，如果可以输出最少需要的时间，否则输出-1。
* 墙用#表示
*  空地用.表示
*  鬼的初始位置用M表示
*  erriyue的初始位置用M表示
*  erriyue的女朋友初始位置用G表示

# 解题思路
&emsp;&emsp;以erriyue和他女朋友为原点，使用双向广度优先搜索路径，同时使用曼哈顿距离（也就是两个方向上的距离和）来判断会不会被鬼追上。双向的广度优先搜索相当单向的耗时少一点，用曼哈顿距离就可以不用把鬼加到队列里了，省了空间。

# 代码
```cpp
#include <stdio.h>
#include <string.h>
#include <queue>

using namespace std;

const int MAX_N = 800 + 10;
// const int MAX_N = 2 + 10;

typedef struct point
{
	int x, y;
} point;

int n, m;
char mp[MAX_N][MAX_N];
char book[2][MAX_N][MAX_N];
queue<point> que[2];
int dir[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

int abs(int a, int b)
{
	return (a > b) ? a - b : b - a;
}

int check_point(point p, point zs[], int t)
{
	if (abs(p.x, zs[0].x) + abs(p.y, zs[0].y) <= 2 * t || 
		abs(p.x, zs[1].x) + abs(p.y, zs[1].y) <= 2 * t)
	{
		return 1;
	}
	return 0;
}

int step_one(int mg, point zs[], int t)
{
	int i, pn;
	point front, tep;

	pn = que[mg].size();
	while(pn--)
	{
		front = que[mg].front();
		que[mg].pop();
		if(check_point(front, zs, t))
		{
			continue;
		}
		for(i = 0; i < 4; i++)
		{
			tep = front;
			tep.x += dir[i][0];
			tep.y += dir[i][1];
			if(tep.x < 0 || tep.x >= n || tep.y < 0 || tep.y >= m)
			{
				continue;
			}
			if(check_point(tep, zs, t) || mp[tep.x][tep.y] == 'X' || book[mg][tep.x][tep.y] == 1)
			{
				continue;
			}
			if(book[!mg][tep.x][tep.y] == 1)
			{
				return 1;
			}
			book[mg][tep.x][tep.y] = 1;
			que[mg].push(tep);
		}
	}
	return 0;
}

int solve(point ms, point gs, point zs[])
{
	int t;

	memset(book, 0, sizeof(book));
	book[0][ms.x][ms.y] = 1;
	book[1][gs.x][gs.y] = 1;
	que[0].push(ms);
	que[1].push(gs);
	t = 0;
	while(que[0].empty() == false || que[1].empty() == false)
	{
		t++;
		if(step_one(0, zs, t) == 1) return t;
		if(step_one(0, zs, t) == 1) return t;
		if(step_one(0, zs, t) == 1) return t;
		if(step_one(1, zs, t) == 1) return t;
	}
	return -1;
}

int main()
{
	int t, i, j, k, ans;
	point ms, gs, zs[2];

	scanf("%d", &t);
	while(t--)
	{
		scanf("%d %d", &n, &m);
		getchar();
		k = 0;
		for(i = 0; i < n; i++)
		{
			scanf("%s", mp[i]);
			for(j = 0; j < m; j++)
			{
				if(mp[i][j] == 'M')
				{
					ms = (point){i, j};
				}
				else if(mp[i][j] == 'G')
				{
					gs = (point){i, j};
				}
				else if(mp[i][j] == 'Z')
				{
					zs[k] = (point){i, j};
					k++;
				}
			}
		}

		while(que[0].empty() == false) que[0].pop();
		while(que[1].empty() == false) que[1].pop();		
		ans = solve(ms, gs, zs);
		printf("%d\n", ans);
	}
	return 0;
}
```