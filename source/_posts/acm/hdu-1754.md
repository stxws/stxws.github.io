---
title: 'HDU-1754 I Hate It'
date: 2020-04-13 15:56:34
categories: acm
tags: [acm,hdu,线段树]
---
线段树模板题，求区间最大值
<!-- more -->

# 题目
&emsp;&emsp;<http://acm.hdu.edu.cn/showproblem.php?pid=1754>

# 题意
&emsp;&emsp;中文题，不解释

# 题目解析
&emsp;&emsp;跟上一题一样，还是线段树的模板题，只不过把求区间和改成了求区间最大值。

# 代码
```cpp
/* http://acm.hdu.edu.cn/showproblem.php?pid=1754 */
/* AC 702MS 4060K */
#include <stdio.h>

const int MAX_N = 200000 + 10;

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
		seg_tree[root] = (a > b) ? a : b;
	}
	return seg_tree[root];
}

int update(int root, int left, int right, int index, int val)
{
	int a, b, mid;
	
	if(left == right - 1)
	{
		seg_tree[root] = val;
	}
	else
	{
		mid = (left + right) / 2;
		if(index < mid)
		{
			seg_tree[root * 2] = update(root * 2, left, mid, index, val);
		}
		else
		{
			seg_tree[root * 2 + 1] = update(root * 2 + 1, mid, right, index, val);
		}
		a = seg_tree[root * 2];
		b = seg_tree[root * 2 + 1];
		seg_tree[root] = (a > b) ? a : b;
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
		return (a > b) ? a : b;
	}
}

int main()
{
	int n, m, x, y;
	int i, ans;
	char req;

	while(scanf("%d %d", &n, &m) != EOF)
	{
		for(i = 0; i < n; i++)
		{
			scanf("%d", &num[i]);
		}
		build(1, 0, n);

		for(i = 0; i < m; i++)
		{
			getchar();
			req = getchar();
			scanf("%d %d", &x, &y);
			x -= 1;
			if(req == 'Q')
			{
				ans = query(1, 0, n, x, y);
				printf("%d\n", ans);
			}
			else if(req == 'U')
			{
				update(1, 0, n, x, y);
			}
		}
	}
	return 0;
}

```