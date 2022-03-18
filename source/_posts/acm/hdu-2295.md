---
title: 'HDU-2295 Radar'
date: 2020-03-19 18:58:57
categories: acm
tags: [acm,hdu,舞蹈链]
---
舞蹈链重复覆盖问题

<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=2295>

# 题意
&emsp;&emsp;给出n个城市，m个雷达站，以及它们的坐标，每个雷达站有一个自身为中心的圆形覆盖范围，每个雷达站的覆盖范围半径R相等。现在要使得每个城市都能被雷达站覆盖，且最多只能启用k个雷达站，求满足条件的R的最小值。

# 题目解析
&emsp;&emsp;二分搜索R的范围，对于每个范围的中值，先假设R等于这个中值，然后构建一个m×n的矩阵，矩阵的第i行第j列表示第i个雷达是否能覆盖第j个城市，如果能为1，否则为0。然后用舞蹈链的重复覆盖算法来，判断覆盖所有城市最少需要的雷达站个数p。最后根据p是否大于k来更新R的范围，直到小于精度值。
&emsp;&emsp;这里精度值最好设小一点，设成1e-6就WA了。

# 代码
```cpp
/* http://acm.hdu.edu.cn/showproblem.php?pid=2295 */
#include <stdio.h>
#include <string.h>
#include <math.h>

const int MAX_N = 50 + 5;
const double EXP = 1e-8;

typedef struct point
{
	double x, y;
	double distance(point b)
	{
		return sqrt((x - b.x) * (x - b.x) + (y - b.y) * (y - b.y));
	}
} point;

typedef struct dance_link
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
		}
		nd[0].l = cols;
		nd[cols].r = 0;
		memset(col_nds, 0, sizeof(col_nds));
		node_size = cols + 1;

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
		col_nds[col]++;
		node_size++;
	}

	void remove(int col)
	{
		int i;
		for(i = nd[col].d; i != col; i = nd[i].d)
		{
			nd[nd[i].l].r = nd[i].r;
			nd[nd[i].r].l = nd[i].l;
		}
	}

	void resume(int col)
	{
		int i;
		for(i = nd[col].d; i != col; i = nd[i].d)
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
		if(limit != -1 && len + get_min_rows() > limit)
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
	int solve(bool is_min_ans = true, int select_rows[] = NULL, int limit = -1)
	{
		this->is_min_ans = is_min_ans;
		this->select_rows = select_rows;
		this->limit = limit;
		ans = -1;
		ans = dfs(0);
		return ans;
	}

} dance_link;

dance_link dl;

int main()
{
	int t, n, m, k;
	int i, j;
	double left, right, mid;
	point city[MAX_N], radar[MAX_N];

	double dist;
	int len;

	scanf("%d", &t);
	while(t--)
	{
		scanf("%d %d %d", &n, &m, &k);
		for(i = 0; i < n; i++)
		{
			scanf("%lf %lf", &city[i].x, &city[i].y);
		}
		for(i = 0; i < m; i++)
		{
			scanf("%lf %lf", &radar[i].x, &radar[i].y);
		}

		left = 0.0;
		right = 1500.0;
		while(right - left >= EXP)
		{
			mid = (right + left) / 2.0;
			dl.init(m, n);
			for(i = 0; i < m; i++)
			{
				for(j = 0; j < n; j++)
				{
					dist = radar[i].distance(city[j]);
					if(radar[i].distance(city[j]) <= mid)
					{
						dl.add_node(i + 1, j + 1);
					}
				}
			}
			len = dl.solve(false, NULL, k);
			if(len != -1 && dl.solve() <= k)
			{
				right = mid;
			}
			else
			{
				left = mid;
			}
		}
		printf("%.6lf\n", right);
	}
	return 0;
}

```