---
title: 'POJ-1084 Square Destroyer'
date: 2020-03-27 09:40:48
categories: acm
tags: [acm,poj,舞蹈链]
mathjax: true
---
舞蹈链重复覆盖问题

<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=1084>

# 题意
&emsp;&emsp;给出一个用火柴拼成的$n \times n$的网格（一共需要$2n(n+1)$根火柴），按顺序给每个火柴编号，然后去掉其中$k$个火柴。问至少还需要去掉几个火柴，使得网格没有任何正方形。

# 题目解析
&emsp;&emsp;这题可以用舞蹈链的重复覆盖算法解决，也有大佬用迭代深搜AC了。用舞蹈链的话关键在于构建覆盖关系矩阵，可以将正方形作为列，火柴作为行，如果第j个正方形的完整依赖于第i根火柴，则第i行的第j列为1，否则为0。这样题目就转化为选择最少的火柴，使得这些火柴能覆盖所有正方形，最后用使用舞蹈链重复覆盖算法模板就可以了。
&emsp;&emsp;比较麻烦的是，遍历所有的正方形需要枚举正方形左上角顶点坐标，然后再枚举正方形的边长，最后还要转一圈，遍历组成该正方形的所有火柴，这循环写的我想哭/(ㄒoㄒ)/~~。然后就是题目在求解前要先删除一些火柴，对于每个要删除的火柴，删的时候关键不是要删除火柴所在的行，而是要删除火柴能覆盖的正方形所对应的列。

# 代码
```cpp
#include <stdio.h>
#include <string.h>

const int MAX_N = 8;

/* 舞蹈链算法，用于求重复覆盖问题 */
typedef struct dance_link_rep
{
	const static int MAX_ROWS = 2 * MAX_N * MAX_N;
	const static int MAX_COLS = 2 * MAX_N * MAX_N;

	typedef struct node
	{
		int u, d, l, r;
		int row, col;
	} node;

	int rows, cols, node_size;
	node nd[MAX_ROWS * MAX_COLS];
	int row_head[MAX_ROWS], col_nds[MAX_COLS];

	bool is_min_ans;
	int limit;
	int ans, *select_rows;

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

	/* 计算取得答案最少需要的行数 */
	int get_min_rows()
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

		/* 判断是否超过了界限 */
		int mr = get_min_rows();
		if(limit != -1 && len + mr > limit)
		{
			return -1;
		}
		if(is_min_ans == true && ans != -1 && len + mr >= ans)
		{
			return -1;
		}
		/* 当前十字链表没有列 */
		if(nd[0].r == 0)
		{
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
			if(select_rows != 0)
			{
				select_rows[len] = nd[i].row;
			}
			remove(i);
			for(j = nd[i].r; j != i; j = nd[j].r)
			{
				remove(j);
			}
			res = dfs(len + 1);
			if(res >= 0)
			{
				if(is_min_ans == false)
				{
					return res;
				}
				else if(ans < 0 || ans > res)
				{
					ans = res;
				}
			}
			for(j = nd[i].l; j != i; j = nd[j].l)
			{
				resume(j);
			}
			resume(i);
		}
		return ans;
	}

	/*
	bool is_min_ans: 是否求答案最小值，如果不是，得到一个可行解就返回，默认求最小值。
	int select_rows[]: 用于保存选择的行，取NULL时不保存，默认取NULL。
	int limit：答案的上限，取-1时无上限，默认为-1。
	*/
	int solve(bool is_min_ans = true, int select_rows[] = 0, int limit = -1)
	{
		this->is_min_ans = is_min_ans;
		this->select_rows = select_rows;
		this->limit = limit;
		ans = -1;
		ans = dfs(0);
		return ans;
	}

} dance_link_rep;


dance_link_rep dl;

int main()
{
	int t, n;
	int i, j, k, s, p, x, y, c, flag, ans;
	int rows, cols;
	int ds[2 * MAX_N], dst;
	int ms[2 * MAX_N][2 * MAX_N];
	int as[dl.MAX_ROWS * dl.MAX_COLS][2], ast;

	scanf("%d", &t);
	while(t--)
	{
		scanf("%d %d", &n, &dst);
		for(i = 0; i < dst; i++)
		{
			scanf("%d", &ds[i]);
		}
		memset(ms, 0, sizeof(ms));
		for(i = 0, c = 1; i <= 2 * n; i++)
		{
			for(j = !(i % 2); j <= 2 * n; j += 2)
			{
				ms[i][j] = c;
				for(s = 0; s < dst; s++)
				{
					if(c == ds[s])
					{
						ms[i][j] = -1;
						break;
					}
				}
				c++;
			}
		}

		c = 1;
		ast = 0;
		for(x = 0; x < 2 * n; x += 2)
		{
			for(y = 0; y < 2 * n; y += 2)
			{
				for(s = 1; s + x / 2 <= n && s + y / 2 <= n; s++)
				{
					k = ast;
					flag = 0;
					i = x;
					j = y + 1;
					for(p = 0; p < s; p++)
					{
						if(ms[i][j] == -1)
						{
							flag = -1;
						}
						as[k][0] = ms[i][j];
						as[k][1] = c;
						k++;
						j += 2;
					}
					i += 1;
					j -= 1;
					for(p = 0; p < s; p++)
					{
						if(ms[i][j] == -1)
						{
							flag = -1;
						}
						as[k][0] = ms[i][j];
						as[k][1] = c;
						k++;
						i += 2;
					}
					i -= 1;
					j -= 1;
					for(p = 0; p < s; p++)
					{
						if(ms[i][j] == -1)
						{
							flag = -1;
						}
						as[k][0] = ms[i][j];
						as[k][1] = c;
						k++;
						j -= 2;
					}
					i -= 1;
					j += 1;
					for(p = 0; p < s; p++)
					{
						if(ms[i][j] == -1)
						{
							flag = -1;
						}
						as[k][0] = ms[i][j];
						as[k][1] = c;
						k++;
						i -= 2;
					}
					if(flag != -1)
					{
						ast = k;
						c++;
					}
				}
			}
		}

		rows = 2 * n * (n + 1);
		cols = c - 1;
		dl.init(rows, cols);
		for(i = 0; i < ast; i++)
		{
			dl.add_node(as[i][0], as[i][1]);
		}

		ans = dl.solve(true, NULL, -1);
		printf("%d\n", ans);
	}
	return 0;
}

```