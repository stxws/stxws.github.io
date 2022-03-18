---
title: 'HDU-3335 Divisibility'
date: 2020-04-02 17:01:49
categories: acm
tags: [acm,hdu,舞蹈链]
---
舞蹈链重复覆盖问题
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=3335>

# 题意
&emsp;&emsp;给出n个数，需要从里面选择一些出来，但是如果选择了某个数k的话，则能被k整除或k能整除的数都不能再选了，问最多能选择多少个数。

# 题目解析
&emsp;&emsp;这题原理不是太懂，参考网上大佬的解题方法AC的，方法如下：
&emsp;&emsp;首先建立一个n×n的整除关系矩阵，如果第i个数于第j个数有整除关系，则矩阵的第i行第j列为1，用这个矩阵来运行舞蹈链重复覆盖算法，取结果最大值作为答案。

# 代码
```cpp
/* http://acm.hdu.edu.cn/showproblem.php?pid=3335 */
/* AC 15MS 1252K */
#include <stdio.h>

const int MAX_N = 1000 + 10;

/* 舞蹈链算法，用于求重复覆盖问题 */
typedef struct dance_link_rep
{
	const static int MAX_ROWS = MAX_N;
	const static int MAX_COLS = MAX_N;

	typedef struct node
	{
		int u, d, l, r;
		int row, col;
	} node;

	int rows, cols, node_size;
	node nd[MAX_ROWS * MAX_COLS];
	int row_head[MAX_ROWS], col_nds[MAX_COLS];

	int ans;

	void init(int rows, int cols)
	{
		int i;

		this -> rows = rows;
		this -> cols = cols;
		/* 初始化每一列的头节点 */
		for(i = 0; i <= cols; i++)
		{
			nd[i].u = i;
			nd[i].d = i;
			nd[i].l = i - 1;
			nd[i].r = i + 1;
			col_nds[i] = 0;
		}
		nd[0].l = cols;
		nd[cols].r = 0;
		node_size = cols + 1;

		/* 初始化每一行的行指针 */
		for(i = 0; i <= rows; i++)
		{
			row_head[i] = -1;
		}
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
		col_nds[col]++;
		node_size++;
	}

	void remove(int col)
	{
		int i;
		for(i = nd[col].d; i != col; i = nd[i].d)
		{
			nd[nd[i].r].l = nd[i].l;
			nd[nd[i].l].r = nd[i].r;
		}
	}

	void resume(int col)
	{
		int i;
		for(i = nd[col].u; i != col; i = nd[i].u)
		{
			nd[nd[i].l].r = i;
			nd[nd[i].r].l = i;
		}
	}

	int get_rows()
	{
		int i, j, k, num = 0;
		bool v[MAX_COLS];
		
		for(i = nd[0].r; i != 0; i = nd[i].r)
		{
			v[i] = true;
		}
		for(i = nd[0].r; i != 0; i = nd[i].r)
		{
			if(v[i] == false)
			{
				continue;
			}
			num++;
			for(j = nd[i].d; j != i; j = nd[j].d)
			{
				for(k = nd[j].r; k != j; k = nd[k].r)
				{
					v[nd[k].col] = false;
				}
			}
		}
		return num;
	}

	int dfs(int len)
	{
		int i, j;
		int res, select_col;

		int mr = get_rows();
		if(ans != -1 && len + mr < ans)
		{
			return -1;
		}
		/* 当前十字链表没有列 */
		if(nd[0].r == 0)
		{
			if(ans < len)
			{
				ans = len;
			}
			return len;
		}
		select_col = nd[0].r;
		for(i = nd[0].r; i != 0; i = nd[i].r)
		{
			if(nd[i].d == i)
			{
				return -1;
			}
			if(col_nds[select_col] > col_nds[i])
			{
				select_col = i;
			}
		}
		for(i = nd[select_col].d; i != select_col; i = nd[i].d)
		{
			remove(i);
			for(j = nd[i].r; j != i; j = nd[j].r)
			{
				remove(j);
			}
			dfs(len + 1);
			for(j = nd[i].l; j != i; j = nd[j].l)
			{
				resume(j);
			}
			resume(i);
		}
		return ans;
	}

	int solve()
	{
		ans = -1;
		dfs(0);
		return ans;
	}

} dance_link_rep;

dance_link_rep dl;

int main()
{
	int t, n;
	int i, j, ans;
	long long a[MAX_N];

	scanf("%d", &t);
	while(t--)
	{
		scanf("%d", &n);
		for(i = 1; i <= n; i++)
		{
			scanf("%lld", &a[i]);
		}

		dl.init(n, n);
		for(i = 1; i <= n; i++)
		{
			for(j = 1; j <= n; j++)
			{
				if(a[i] % a[j] == 0 || a[j] % a[i] == 0)
				{
					dl.add_node(i, j);
				}
			}
		}
		ans = dl.solve();
		printf("%d\n", ans);
	}
	return 0;
}

```