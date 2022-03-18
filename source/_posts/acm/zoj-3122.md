---
title: 'ZOJ-3122 Sudoku'
date: 2020-03-27 16:03:14
categories: acm
tags: [acm,poj,舞蹈链]
---
用舞蹈链来解决16×16数独问题
<!-- more -->

# 题目
&emsp;&emsp;<https://zoj.pintia.cn/problem-sets/91827364500/problems/91827367537>

# 题意
&emsp;&emsp;给一个16×16的矩阵，求解数独问题。

# 题目解析
&emsp;&emsp;这题跟上一题的解法类似，只是上一题是9×9，这题是16×16，具体请参考<https://nchuxw.github.io/post/poj-3074-sudoku/>，题目的测试样例的输入有问题，需要改正，还有就是输出的时候最后一个测试样例不要换行，否则会`Presentation Error`。

# 代码
```cpp
/* https://zoj.pintia.cn/problem-sets/91827364500/problems/91827367537 */
/* AC 201ms	640kb */
#include <stdio.h>

const int MAX_N = 16;

/* 舞蹈链算法，用于求不重复精确覆盖问题 */
typedef struct dance_link
{
	const static int MAX_ROWS = MAX_N * MAX_N * MAX_N + 10;
	const static int MAX_COLS = MAX_N * MAX_N * 4 + 10;

	typedef struct node
	{
		int u, d, l, r;
		int row, col;
	} node;

	int rows, cols, node_size;
	node nd[(MAX_ROWS + 1) * MAX_COLS];
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
				col_nds[nd[j].col]--;
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
				col_nds[nd[j].col]++;
			}
		}
	}

	int dfs(int len)
	{
		int i, j;
		int res, select_col;

		/* 判断是否超过了界限 */
		if(limit != -1 && len > limit)
		{
			return -1;
		}
		if(is_min_ans == true && ans != -1 && len > ans)
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
		remove(select_col);
		for(i = nd[select_col].d; i != select_col; i = nd[i].d)
		{
			if(select_rows != 0)
			{
				select_rows[len] = nd[i].row;
			}
			for(j = nd[i].r; j != i; j = nd[j].r)
			{
				remove(nd[j].col);
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
				resume(nd[j].col);
			}
		}
		resume(select_col);
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

} dance_link;

dance_link dl;

int main()
{
	int i, j, k, t, row;
	char str[MAX_N + 10][MAX_N + 10];
	int x[dl.MAX_ROWS], y[dl.MAX_ROWS], num[dl.MAX_ROWS], ans[dl.MAX_ROWS], ansl;

	for(t = 0; ; t++)
	{
		for(i = 0; i < 16; i++)
		{
			if(scanf("%s", str[i]) == EOF)
			{
				break;
			}
		}
		if(i < 16)
		{
			break;
		}
		if(t != 0)
		{
			printf("\n");
		}

		dl.init(16 * 16 * 16, 4 * 16 * 16);
		row = 1;
		for(i = 0; i < 16; i++)
		{
			for(j = 0; j < 16; j++)
			{
				if('A' <= str[i][j] && str[i][j] <= 'Z')
				{
					k = (int)(str[i][j] - 'A');
					dl.add_node(row, i * 16 + j + 1);
					dl.add_node(row, 256 + i * 16 + k + 1);
					dl.add_node(row, 512 + j * 16 + k + 1);
					dl.add_node(row, 768 + (i / 4 * 4 + j / 4) * 16 + k + 1);
					// printf("(%d,%d) ", row, i * 16 + j + 1);
					// printf("(%d,%d) ", row, 256 + i * 16 + k + 1);
					// printf("(%d,%d) ", row, 512 + j * 16 + k + 1);
					// printf("(%d,%d)\n", row, 768 + (i / 4 * 4 + j / 4) * 16 + k + 1);
					x[row] = i;
					y[row] = j;
					num[row] = k;
					row++;
				}
				else if(str[i][j] == '-')
				{
					for(k = 0; k < 16; k++)
					{
						dl.add_node(row, i * 16 + j + 1);
						dl.add_node(row, 256 + i * 16 + k + 1);
						dl.add_node(row, 512 + j * 16 + k + 1);
						dl.add_node(row, 768 + (i / 4 * 4 + j / 4) * 16 + k + 1);
						// printf("(%d,%d) ", row, i * 16 + j + 1);
						// printf("(%d,%d) ", row, 256 + i * 16 + k + 1);
						// printf("(%d,%d) ", row, 512 + j * 16 + k + 1);
						// printf("(%d,%d)\n", row, 768 + (i / 4 * 4 + j / 4) * 16 + k + 1);
						x[row] = i;
						y[row] = j;
						num[row] = k;
						row++;
					}
				}
			}
		}
		ansl = dl.solve(false, ans);
		for(i = 0; i < ansl; i++)
		{
			str[x[ans[i]]][y[ans[i]]] = (char)('A' + num[ans[i]]);
		}
		for(i = 0; i < 16; i++)
		{
			str[i][16] = '\0';
			printf("%s\n", str[i]);
		}
	}

	return 0;
}

/*

--A----C-----O-I
-J--A-B-P-CGF-H-
--D--F-I-E----P-
-G-EL-H----M-J--
----E----C--G---
-I--K-GA-B---E-J
D-GP--J-F----A--
-E---C-B--DP--O-
E--F-M--D--L-K-A
-C--------O-I-L-
H-P-C--F-A--B---
---G-OD---J----H
K---J----H-A-P-L
--B--P--E--K--A-
-H--B--K--FI-C--
--F---C--D--H-N-

FPAHMJECNLBDKOGI
OJMIANBDPKCGFLHE
LNDKGFOIJEAHMBPC
BGCELKHPOFIMAJDN
MFHBELPOACKJGNID
CILNKDGAHBMOPEFJ
DOGPIHJMFNLECAKB
JEKAFCNBGIDPLHOM
EBOFPMIJDGHLNKCA
NCJDHBAEKMOFIGLP
HMPLCGKFIAENBDJO
AKIGNODLBPJCEFMH
KDEMJIFNCHGAOPBL
GLBCDPMHEONKJIAF
PHNOBALKMJFIDCEG
IAFJOECGLDPBHMNK

*/

```