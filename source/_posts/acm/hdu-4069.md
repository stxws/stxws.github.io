---
title: 'HDU-4069 Squiggly Sudoku'
date: 2020-03-31 15:26:52
categories: acm
tags: [acm,hdu,舞蹈链]
---
变形的数独问题
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=4069>

# 题意
&emsp;&emsp;普通的数独问题是要求每个3×3的子矩阵里不能有相同的数字，这题将3×3的子矩阵改成了题目给定的连通区域，每个连通区域的面积为9，其他要求不变。

# 题目解析
&emsp;&emsp;与用舞蹈链解决普通数独问题类似，求解前需要用深度优先搜索找出每个连通区域的范围，然后给每个连通区域编号，用这个编号去代替解决普通数独问题的3×3子矩阵的编号。
&emsp;&emsp;这题比较麻烦的是，需要判断是否有两个以上的解，所以在用舞蹈链搜索的时候记录解的个数，如果解的个数大于2个就停止搜索。这里需要注意的是，找到第一个解后需要用数组把搜索过程中选择的行保存下来，因为下一次搜索不一定能得到第二个正确答案，但是在求解的过程中会取得第一个答案选择的行覆盖掉，所以不能用搜索选择的行来作为正确答案选择的行。

# 代码
```cpp
/* http://acm.hdu.edu.cn/showproblem.php?pid=4069 */
/* AC 764MS 1324K */
#include <stdio.h>

const int MAX_N = 10;

typedef struct dance_link
{
	const static int MAX_ROWS = MAX_N * MAX_N * MAX_N;
	const static int MAX_COLS = 4 * MAX_N * MAX_N;

	typedef struct node
	{
		int u, d, l, r;
		int row, col;
	} node;

	int rows, cols, node_size;
	node nd[MAX_ROWS * 4 * MAX_N];
	int row_head[MAX_ROWS], col_nds[MAX_COLS];
	int path[MAX_ROWS];

	int ansl, *select_rows;
	int ans_num;

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

		/* 当前十字链表没有列 */
		if(nd[0].r == 0)
		{
			ans_num++;
			ansl = len;
			for(i = 0; i < len; i++)
			{
				select_rows[i] = path[i];
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
		remove(select_col);
		for(i = nd[select_col].d; i != select_col; i = nd[i].d)
		{
			path[len] = nd[i].row;
			for(j = nd[i].r; j != i; j = nd[j].r)
			{
				remove(nd[j].col);
			}
			res = dfs(len + 1);
			if(res >= 0)
			{
				if(ans_num > 1)
				{
					return res;
				}
			}
			for(j = nd[i].l; j != i; j = nd[j].l)
			{
				resume(nd[j].col);
			}
		}
		resume(select_col);
	}

	/*
	bool is_min_ans: 是否求答案最小值，如果不是，得到一个可行解就返回，默认求最小值。
	int select_rows[]: 用于保存选择的行，取NULL时不保存，默认取NULL。
	int limit：答案的上限，取-1时无上限，默认为-1。
	*/
	int solve(int select_rows[] = 0)
	{
		ans_num = 0;
		this->select_rows = select_rows;
		dfs(0);
		return ans_num;
	}

} dance_link;

dance_link dl;

typedef struct node
{
	int num;
	int grp;
	int dir[4];
} node;

node mp[MAX_N][MAX_N];
int dirs[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

void dfs(int x, int y, int grp)
{
	int i;

	if(x < 0 || x >= 9 || y < 0 || y >= 9 || mp[x][y].grp != 0)
	{
		return;
	}
	mp[x][y].grp = grp;
	for(i = 0; i < 4; i++)
	{
		if(mp[x][y].dir[i] == 0)
		{
			dfs(x + dirs[i][0], y + dirs[i][1], grp);
		}
	}
}

int main()
{
	int t, cas, i, j, k, in, row, ans_num;
	int x[dl.MAX_ROWS], y[dl.MAX_ROWS], num[dl.MAX_ROWS], ans[dl.MAX_ROWS], ansl;

	scanf("%d", &t);
	for(cas = 1; cas <= t; cas++)
	{
		for(i = 0; i < 9; i++)
		{
			for(j = 0; j < 9; j++)
			{
				scanf("%d", &in);
				mp[i][j].num = in % 16;
				in = in >> 4;
				for(k = 0; k < 4; k++)
				{
					mp[i][j].dir[k] = in & 1;
					in = in >> 1;
				}
				mp[i][j].grp = 0;
			}
		}
		k = 1;
		for(i = 0; i < 9; i++)
		{
			for(j = 0; j < 9; j++)
			{
				if(mp[i][j].grp == 0)
				{
					dfs(i, j, k);
					k++;
				}
			}
		}

		dl.init(9 * 9 * 9, 4 * 9 * 9);
		row = 1;
		for(i = 0; i < 9; i++)
		{
			for(j = 0; j < 9; j++)
			{
				if(mp[i][j].num == 0)
				{
					for(k = 0; k < 9; k++)
					{
						dl.add_node(row, i * 9 + j + 1);
						dl.add_node(row, 81 + i * 9 + k + 1);
						dl.add_node(row, 162 + j * 9 + k + 1);
						dl.add_node(row, 243 + (mp[i][j].grp - 1) * 9 + k + 1);
						x[row] = i;
						y[row] = j;
						num[row] = k + 1;
						row++;
					}
				}
				else
				{
					k = mp[i][j].num - 1;
					dl.add_node(row, i * 9 + j + 1);
					dl.add_node(row, 81 + i * 9 + k + 1);
					dl.add_node(row, 162 + j * 9 + k + 1);
					dl.add_node(row, 243 + (mp[i][j].grp - 1) * 9 + k + 1);
					x[row] = i;
					y[row] = j;
					num[row] = k + 1;
					row++;
				}
			}
		}

		ans_num = dl.solve(ans);
		printf("Case %d:\n", cas);
		if(ans_num <= 0)
		{
			printf("No solution\n");
		}
		else if(ans_num == 1)
		{
			for(k = 0; k < dl.ansl; k++)
			{
				i = x[ans[k]];
				j = y[ans[k]];
				mp[i][j].num = num[ans[k]];
			}

			for(i = 0; i < 9; i++)
			{
				for(j = 0; j < 9; j++)
				{
					printf("%d", mp[i][j].num);
				}
				printf("\n");
			}
		}
		else
		{
			printf("Multiple Solutions\n");
		}
	}
	return 0;
}

/*
3
144 18 112 208 80 25 54 144 48
135 38 147 80 121 128 97 130 32
137 32 160 144 114 167 208 0 32
192 100 160 160 208 96 183 192 101
209 80 39 192 86 48 136 80 114
152 48 226 144 112 160 160 149 48
128 0 112 166 215 96 160 128 41
128 39 153 32 209 80 101 136 35
192 96 200 67 80 112 208 68 96 

144 48 144 81 81 16 53 144 48
128 96 224 144 48 128 103 128 38
163 208 80 0 37 224 209 0 32
135 48 176 192 64 112 176 192 104
192 101 128 89 80 82 32 150 48
149 48 224 208 16 48 224 192 33
128 0 114 176 135 0 80 112 169
137 32 148 32 192 96 176 144 32
192 96 193 64 80 80 96 192 96

144 88 48 217 16 16 80 112 176
224 176 129 48 128 40 208 16 37
145 32 128 96 196 96 176 136 32
192 32 227 176 144 80 96 192 32
176 192 80 98 160 145 80 48 224
128 48 144 80 96 224 183 128 48
128 36 224 144 51 144 32 128 105
131 64 112 136 32 192 36 224 176
224 208 80 64 64 116 192 83 96


Case 1:
521439678
763895124
984527361
346182795
157964832
812743956
235678419
479216583
698351247
Case 2:
No solution
Case 3:
Multiple Solutions

*/

```