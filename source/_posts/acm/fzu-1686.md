---
title: 'FZU-1686 神龙的难题'
date: 2020-03-19 19:00:07
categories: acm
tags: [acm,舞蹈链]
mathjax: true
---
舞蹈链重复覆盖问题
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.fzu.edu.cn/problem.php?pid=1686>

# 题意
&emsp;&emsp;中文题，又可以偷懒了！

# 题目解析
&emsp;&emsp;计算出地图上所有怪物的个数，假设为$K$个，给怪物从1到K进行编号。然后枚举每一种神龙攻击的情况，也就是枚举神龙攻击范围的左上角坐标，行坐标一共有$n-n1+1$种情况，列坐标一共有$m-m1+1$种情况，所以一共有$(n-n1+1) \times (m-m1+1)$种攻击情况，假设为$P=(n-n1+1) \times (m-m1+1)$。然后构建一个$P \times K$的矩阵$M$，然后第$i$种攻击情况能攻击到第$j$个怪物，则$M$的第$i$行的第$j$个元素为$1$，否则为$0$。最后用舞蹈链对$M$求重复覆盖问题就好了。

# 代码
```cpp
/* http://acm.fzu.edu.cn/problem.php?pid=1686 */
#include <stdio.h>
#include <string.h>

const int MAX_N = 17;

typedef struct dance_link
{
	const static int MAX_ROWS = MAX_N * MAX_N;
	const static int MAX_COLS = MAX_N * MAX_N;

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

	void remove_rep(int col)
	{
		int i;
		for(i = nd[col].d; i != col; i = nd[i].d)
		{
			nd[nd[i].r].l = nd[i].l;
			nd[nd[i].l].r = nd[i].r;
		}
	}

	void resume_rep(int col)
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

	int dfs_rep(int len)
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
			if(select_rows != NULL)
			{
				select_rows[len] = nd[i].row;
			}
			remove_rep(i);
			for(j = nd[i].r; j != i; j = nd[j].r)
			{
				remove_rep(j);
			}
			res = dfs_rep(len + 1);
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
				resume_rep(j);
			}
			resume_rep(i);
		}
		return ans;
	}

	/*
	bool is_min_ans: 是否求答案最小值，如果不是，得到一个可行解就返回，默认求最小值。
	int select_rows[]: 用于保存选择的行，取NULL时不保存，默认取NULL。
	int limit：答案的上限，取-1时无上限，默认为-1。
	*/
	int solve(bool is_min_ans = true, int select_rows[] = NULL, int limit = -1)
	{
		this->is_min_ans = is_min_ans;
		this->select_rows = select_rows;
		this->limit = limit;
		ans = -1;
		ans = dfs_rep(0);
		return ans;
	}

} dance_link;

dance_link dl;

int main()
{
	int n, m, n1, m1;
	int i, j, k, x, y, ans;
	int map[MAX_N][MAX_N];

	while(scanf("%d %d", &n, &m) != EOF)
	{
		k = 0;
		for(i = 0; i < n; i++)
		{
			for(j = 0; j < m; j++)
			{
				scanf("%d", &map[i][j]);
				if(map[i][j] != 0)
				{
					k++;
					map[i][j] = k;
				}
			}
		}
		scanf("%d %d", &n1, &m1);

		dl.init((n - n1 + 1) * (m - m1 + 1), k);
		k = 0;
		for(x = 0; x + n1 <= n; x++)
		{
			for(y = 0; y + m1 <= m; y++)
			{
				for(i = x; i < x + n1; i++)
				{
					for(j = y; j < y + m1; j++)
					{
						if(map[i][j] != 0)
						{
							dl.add_node(k + 1, map[i][j]);
						}
					}
				}
				k++;
			}
		}

		ans = dl.solve(true);
		printf("%d\n", ans);
	}
	return 0;
}

```