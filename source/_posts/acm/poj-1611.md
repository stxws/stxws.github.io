---
title: 'POJ-1611 The Suspects'
date: 2020-04-07 18:06:14
categories: acm
tags: [acm,poj,并查集]
---
简单的并查集
<!-- more -->

# 题目
&emsp;&emsp;<http://poj.org/problem?id=1611>

# 题意
&emsp;&emsp;有n个学生和m个团队，学生编号为0～n，一个学生可以属于多个团体。团体内如果有一个学生被怀疑感染了病毒，那么团体内所有学生都会被怀疑感染了病毒，初始时假设只有0号学生被怀疑感染了病毒，问一共有多少人会被怀疑感染了病毒。

# 题目解析
&emsp;&emsp;可以用并查集来解决，首先0号学生属于0号集合，对于每个团体，找到所有成员所在的集合编号，如果有一个成员属于0号集合，则把所有成员都合并到0号集合，如果没有成员属于0号集合，则将所有成员所属的集合合并成一个集合，集合编号任意。

# 代码
```cpp
/* http://poj.org/problem?id=1611 */
/* AC 16MS 464K */
#include <stdio.h>

const int MAX_N = 30000 + 10;
const int MAX_M = 500 + 10;

int find_root(int set[], int i)
{
	if(set[i] != i)
	{
		set[i] = find_root(set, set[i]);
	}
	return set[i];
}

int main()
{
	int n, m;
	int i, j, k, num, ar, br, ans;
	int set[MAX_N];

	while(scanf("%d %d", &n, &m) != EOF && (n != 0 || m != 0))
	{
		for(i = 0; i < n; i++)
		{
			set[i] = i;
		}
		for(i = 0; i < m; i++)
		{
			scanf("%d", &k);
			if(k != 0)
			{
				scanf("%d", &num);
				ar = find_root(set, num);
			}
			for(j = 1; j < k; j++)
			{
				scanf("%d", &num);
				br = find_root(set, num);
				if(br == 0)
				{
					set[ar] = br;
					ar = 0;
				}
				else
				{
					set[br] = ar;
				}
			}
		}
		ans = 0;
		for(i = 0; i < n; i++)
		{
			ar = find_root(set, i);
			if(ar == 0)
			{
				ans++;
			}
		}
		printf("%d\n", ans);
	}
	return 0;
}

```