---
title: 'HDU-1166 敌兵布阵'
date: 2020-04-13 12:02:13
categories: acm
tags: [acm,hdu,线段树]
---
线段树模板题，求区间和
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=1166>

# 题意
&emsp;&emsp;又是一道可以偷懒的中文题，开心！

# 题目解析
&emsp;&emsp;这是一道线段树的模板题，而且不加延迟标记也能AC。这题也可以用树状数组来做。

# 代码
```cpp
/* http://acm.hdu.edu.cn/showproblem.php?pid=1166 */
/* AC 249MS 1928K */
#include <stdio.h>

const int MAX_N = 50000 + 10;

int num[MAX_N];
int seg_tree[4 * MAX_N];

int build(int root, int left, int right)
{
	int a, b, mid;

	if(left == right - 1)
	{
		seg_tree[root] = num[left];
	}
	else
	{
		mid = (left + right) / 2;
		a = build(root * 2, left, mid);
		b = build(root * 2 + 1, mid, right);
		seg_tree[root] = a + b;
	}
	return seg_tree[root];
}

int update(int root, int left, int right, int index, int add)
{
	int mid;
	
	if(left == right - 1)
	{
		seg_tree[root] += add;
	}
	else
	{
		mid = (left + right) / 2;
		if(index < mid)
		{
			seg_tree[root * 2] = update(root * 2, left, mid, index, add);
		}
		else
		{
			seg_tree[root * 2 + 1] = update(root * 2 + 1, mid, right, index, add);
		}
		seg_tree[root] = seg_tree[root * 2] + seg_tree[root * 2 + 1];
	}
	return seg_tree[root];
}

int query(int root, int left, int right, int ql, int qr)
{
	int a, b, mid;

	if(qr <= left || right <= ql)
	{
		return 0;
	}
	else if(ql <= left && right <= qr)
	{
		return seg_tree[root];
	}
	else
	{
		mid = (left + right) / 2;
		a = query(root * 2, left, mid, ql, qr);
		b = query(root * 2 + 1, mid, right, ql, qr);
		return a + b;
	}
}

int main()
{
	int cas, t, n, x, y;
	int i, ans;
	char req[20];

	scanf("%d", &t);
	for(cas = 1; cas <= t; cas++)
	{
		scanf("%d", &n);
		for(i = 0; i < n; i++)
		{
			scanf("%d", &num[i]);
		}
		build(1, 0, n);

		printf("Case %d:\n", cas);
		while(getchar(), scanf("%s", req) != EOF)
		{
			if(req[0] == 'E')
			{
				break;
			}
			scanf("%d %d", &x, &y);
			x -= 1;
			if(req[0] == 'Q')
			{
				ans = query(1, 0, n, x, y);
				printf("%d\n", ans);
			}
			else if(req[0] == 'A')
			{
				update(1, 0, n, x, y);
			}
			else if(req[0] == 'S')
			{
				update(1, 0, n, x, -y);
			}
		}
	}
	return 0;
}

```