---
title: 'HUST-1017 Exact cover'
date: 2020-03-10 20:45:59
categories: acm
tags: [hust,舞蹈链,acm]
---
精确覆盖问题

<!-- more -->

# 题目
&emsp;&emsp;<http://www.hustoj.org/problem/1017>

# 题意
&emsp;&emsp;给出一个大小为n×m，只包含0和1的矩阵，需要选出矩阵中的某些行，使得这些行组成的子矩阵在每一列上有且只有一个1。

# 题目解析
&emsp;&emsp;这题是舞蹈链的模板题，标准的精确覆盖问题。第一次接触舞蹈链算法，参考大佬的博客才看懂的，关于舞蹈链算法，参考自<https://www.cnblogs.com/grenet/p/3145800.html>，大佬解释的非常详细了，在此感谢[万仓一黍](https://www.cnblogs.com/grenet/)大佬的解释，我比较懒，就不复述了。代码参考了<https://www.cnblogs.com/ZShogg/p/3288980.html>，也感谢[Hogg](https://www.cnblogs.com/ZShogg/)大佬的代码。

# 代码
```cpp
/* http://www.hustoj.org/problem/1017 */
/* 测试样例通过了，因为oj的问题（HUST OJ不支持特判），无法提交 */
#include <stdio.h>
#include <string.h>

const int MAX_N = 1000 + 10;
const int MAX_NODE = MAX_N * 100;

typedef struct node
{
	int u, d, l, r;
	int row, col;
} node;

int n, m, node_size;
node nd[MAX_NODE];
int row_head[MAX_N];

void init()
{
	int i;

	/* 初始化每一列的头节点 */
	for(i = 0; i <= m; i++)
	{
		nd[i].u = i;
		nd[i].d = i;
		nd[i].l = i - 1;
		nd[i].r = i + 1;
	}
	nd[0].l = m;
	nd[m].r = 0;
	node_size = m + 1;

	/* 初始化每一行的行指针 */
	memset(row_head, -1, sizeof(row_head));
}

void add_node(int row, int col)
{
	/* nd[node_size]为新添加的节点 */
	nd[node_size].row = row;
	nd[node_size].col = col;

	/* 将新添加的节点与其所在的列连接 */
	nd[node_size].u = col;
	nd[node_size].d = nd[col].d;
	nd[nd[col].d].u = node_size;
	nd[col].d = node_size;

	/* 将新添加的节点与其所在的行连接 */
	if(row_head[row] == -1)
	{
		row_head[row] = node_size;
		nd[node_size].l = node_size;
		nd[node_size].r = node_size;
	}
	else
	{
		int row_first = row_head[row];
		nd[node_size].r = row_first;
		nd[node_size].l = nd[row_first].l;
		nd[nd[row_first].l].r = node_size;
		nd[row_first].l = node_size;
	}
	node_size++;
}

void remove(int col)
{
	int i, j;

	/* 将第col列从十字链表里移除 */
	nd[nd[col].l].r = nd[col].r;
	nd[nd[col].r].l = nd[col].l;

	/* 将与第col列里节点有关的行移除 */
	for(i = nd[col].d; i != col; i = nd[i].d)
	{
		for(j = nd[i].r; j != i; j = nd[j].r)
		{
			nd[nd[j].u].d = nd[j].d;
			nd[nd[j].d].u = nd[j].u;
		}
	}
}

void resume(int col)
{
	int i, j;

	/* 将第col列从十字链表里恢复 */
	nd[nd[col].l].r = col;
	nd[nd[col].r].l = col;

	/* 将与第col列里节点有关的行恢复 */
	for(i = nd[col].d; i != col; i = nd[i].d)
	{
		for(j = nd[i].r; j != i; j = nd[j].r)
		{
			nd[nd[j].u].d = j;
			nd[nd[j].d].u = j;
		}
	}
}

int dfs(int ans[], int len)
{
	int i, j, res, select_col;

	/* 当前十字链表没有列 */
	if(nd[0].r == 0)
	{
		return len;
	}
	for(i = nd[0].r; i != 0; i = nd[i].r)
	{
		if(nd[i].d == i)
		{
			return -1;
		}
	}
	select_col = nd[0].r;
	remove(select_col);
	for(i = nd[select_col].d; i != select_col; i = nd[i].d)
	{
		ans[len] = nd[i].row;
		for(j = nd[i].r; j != i; j = nd[j].r)
		{
			remove(nd[j].col);
		}
		res = dfs(ans, len + 1);
		if(res >= 0)
		{
			return res;
		}
		for(j = nd[i].l; j != i; j = nd[j].l)
		{
			resume(nd[j].col);
		}
	}
	resume(select_col);
	return -1;
}

int main()
{
	int i, j, k, c, len;
	int ans[MAX_N];

	while(scanf("%d %d", &n, &m) != EOF)
	{
		init();
		for(i = 1; i <= n; i++)
		{
			scanf("%d", &c);
			for(j = 0; j < c; j++)
			{
				scanf("%d", &k);
				add_node(i, k);
			}
		}

		len = dfs(ans, 0);
		if(len < 0)
		{
			printf("NO\n");
		}
		else
		{
			printf("%d", len);
			for(i = 0; i < len; i++)
			{
				printf(" %d", ans[i]);
			}
			printf("\n");
		}
	}
	
	return 0;
}

/*

6 7
3 1 4 7
2 1 4
3 4 5 7
3 3 5 6
4 2 3 6 7
2 2 7

*/
```