---
title: 'HDU-2102 A计划'
date: 2020-02-26 19:36:55
categories: acm
tags: [acm,搜索,hdu]
---
简单搜索题
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=2102>

# 题意
&emsp;&emsp;中文题，就不解释了哈。

# 解题思路
&emsp;&emsp;从起点开始搜索四个方向就好了，用深度优先搜索和广度优先搜索都行，遇到#就搜索另一层。需要注意的是传送到另一层后，不只是要判断是不是墙，还要判断是不是#，因为按题意来说，这种情况会一直在两层之间传送，然后走不出去，如果不特判的话，会在另一层继续搜索。

# 代码
```cpp
#include <stdio.h>
#include <string.h>

const int MAX_N = 12;

typedef struct node
{
	int x, y, z;
	int t;
} node;

int n, m, t;
char map[2][MAX_N][MAX_N];

int solve()
{
	int i, j, front, back;
	int book[2][MAX_N][MAX_N];
	node que[2 * MAX_N * MAX_N];
	node tep;
	int dir[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

	que[0] = (node){0, 0, 0, 0};
	front = 0;
	back = 1;
	memset(book, 0, sizeof(book));
	book[0][0][0] = 1;
	while(front != back)
	{
		for(i = 0; i < 4; i++)
		{
			tep = que[front];
			tep.x += dir[i][0];
			tep.y += dir[i][1];
			tep.t++;
			if(tep.x < 0 || tep.x >= n || tep.y < 0 || tep.y >= m || tep.t > t)
			{
				continue;
			}
			if(map[tep.z][tep.x][tep.y] == '#')
			{
				tep.z = !tep.z;
			}
			if(map[tep.z][tep.x][tep.y] == '*' || map[tep.z][tep.x][tep.y] == '#' || book[tep.z][tep.x][tep.y] == 1)
			{
				continue;
			}
			if(map[tep.z][tep.x][tep.y] == 'P')
			{
				return tep.t;
			}
			book[tep.z][tep.x][tep.y] = 1;
			que[back] = tep;
			back++;
		}
		front++;
	}
	return 0;
}

int main()
{
	int c, i, ans;

	scanf("%d", &c);
	while(c--)
	{
		scanf("%d %d %d", &n, &m, &t);
		getchar();
		for(i = 0; i < n; i++)
		{
			scanf("%s", map[0][i]);
		}
		getchar();
		for(i = 0; i < n; i++)
		{
			scanf("%s", map[1][i]);
		}

		ans = solve();
		if(ans == 0)
		{
			printf("NO\n");
		}
		else
		{
			printf("YES\n");
		}
	}
	return 0;
}
```