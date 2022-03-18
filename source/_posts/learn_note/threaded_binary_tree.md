---
title: '线索二叉树'
date: 2021-12-29
categories: 学习笔记
tags: [二叉树，数据结构，算法]
mathjax: true
---

# 先说两句

&emsp;&emsp;前几天考研题里，考到了线索二叉树和哈夫曼树，之前打acm的时侯没遇到过关于这两个的题目，所以就一直懒得学，考研要考，只好花点时间学一下了。本文大部分内容参考自大佬的这篇[博客](https://www.jianshu.com/p/3965a6e424f5)，好吧，几乎就是照抄。

# 线索二叉树产生背景

&emsp;&emsp;现有一棵结点数目为n的二叉树，采用二叉链表的形式存储。对于每个结点均有指向左右孩子的两个指针域，而结点为n的二叉树一共有n-1条有效分支路径。那么，则二叉链表中存在2n-(n-1)=n+1个空指针域。那么，这些空指针造成了空间浪费。

&emsp;&emsp;例如：图1所示一棵二叉树一共有10个结点，空指针^有11个。

![图1](/images/learn_note/threaded_binary_tree/fig_1.png)

&emsp;&emsp;此外，当对二叉树进行中序遍历时可以得到二叉树的中序序列。例如：图1所示二叉树的中序遍历结果为HDIBJEAFCG，可以得知A的前驱结点为E，后继结点为F。但是，这种关系的获得是建立在完成遍历后得到的，那么可不可以在建立二叉树时就记录下前驱后继的关系呢，那么在后续寻找前驱结点和后继结点时将大大提升效率。

# 线索化

&emsp;&emsp;现将某结点的空指针域指向该结点的前驱后继，定义规则如下：

>若结点的左子树为空，则该结点的左孩子指针指向其前驱结点。
>若结点的右子树为空，则该结点的右孩子指针指向其后继结点。

&emsp;&emsp;这种指向前驱和后继的指针称为线索。将一棵普通二叉树以某种次序遍历，并添加线索的过程称为线索化。
&emsp;&emsp;按照规则将图1所示二叉树线索化后如图2所示：

![图2](/images/learn_note/threaded_binary_tree/fig_2.png)

&emsp;&emsp;图中黑色点画线为指向后继的线索，紫色虚线为指向前驱的线索。
&emsp;&emsp;可以看出通过线索化，既解决了空间浪费问题，又解决了前驱后继的记录问题。

# 线索化带来新问题

&emsp;&emsp;经过第3节的讲解后，可以将一棵二叉树线索化为一棵线索二叉树，那么新的问题产生了。我们如何区分一个结点的lchild指针是指向左孩子还是前驱结点呢？例如：对于图2所示的结点E，如何区分其lchild的指向的结点J是其左孩子还是前驱结点呢？
&emsp;&emsp;为了解决这一问题，现需要添加标志位ltag，rtag。并定义规则如下：

>ltag为0时，指向左孩子，为1时指向前驱
>rtag为0时，指向右孩子，为1时指向后继

&emsp;&emsp;添加ltag和rtag属性后的结点结构如下：

![图3](/images/learn_note/threaded_binary_tree/fig_3.png)

图2所示线索二叉树转变为下图4所示的二叉树:

![图4](/images/learn_note/threaded_binary_tree/fig_4.png)

# 线索二叉树结点数据结构

```cpp
typedef enum pointer_flag
{
	POINTER_NODE,
	POINTER_THREAD
} pointer_flag;

typedef struct tree_node
{
	char data;
	struct tree_node *left_child;
	struct tree_node *right_child;
	pointer_flag left_flag, right_flag;
} tree_node;
```

# 中序线索二叉树

## 建立

&emsp;&emsp;二叉树中序遍历的方法可以参考大佬的这篇[博客](https://www.jianshu.com/p/bf73c8d50dc2)，实现线索化的过程就是在中序遍历同时修改结点空指针的指向。

## 加上头结点

&emsp;&emsp;加上线索的二叉树结构是一个双向链表结构，为了便于遍历线索二叉树，我们为其添加一个头结点，头结点左孩子指向原二叉树的根结点，右孩子指针指向中序遍历的最后一个结点。同时，将第一个结点左孩子指针指向头结点，最后一个结点的右孩子指针指向头结点。

&emsp;&emsp;图4所示线索二叉树添加头结点后如图5所示：

![图5](/images/learn_note/threaded_binary_tree/fig_5.png)

## 代码实现

&emsp;&emsp;采用中序遍历的访问顺序实现一棵二叉树的线索化过程代码如下：

```cpp
void mid_order_traverse_build_tree(tree_node *root, tree_node **pre_node)
{
	if(root != NULL)
	{
		mid_order_traverse_build_tree(root->left_child, pre_node);
		if(root->left_child == NULL)
		{
			root->left_child = *pre_node;
			root->left_flag = POINTER_THREAD;
		}
		else
		{
			root->left_flag = POINTER_NODE;
		}

		if((*pre_node)->right_child == NULL)
		{
			(*pre_node)->right_child = root;
			(*pre_node)->right_flag = POINTER_THREAD;
		}
		else
		{
			(*pre_node)->right_flag = POINTER_NODE;
		}
		*pre_node = root;
		mid_order_traverse_build_tree(root->right_child, pre_node);
	}
}

tree_node* build_thread_binary_tree(tree_node *root)
{
	tree_node *head_node = (tree_node *)malloc(sizeof(tree_node));
	tree_node *pre_node;

	if(root != NULL)
	{
		head_node->left_child = root;
		pre_node = head_node;
		mid_order_traverse_build_tree(head_node->left_child, &pre_node);
		head_node->right_child = pre_node;
		head_node->right_flag = POINTER_THREAD;
		pre_node->right_child = head_node;
		pre_node->right_flag = POINTER_THREAD;
	}
	else
	{
		head_node->left_child = head_node;
		head_node->right_child = head_node;
	}
	return head_node;
}
```

## 遍历

&emsp;&emsp;带有头结点的中序线索二叉树遍历代码如下：

```cpp
void traverse_thread_binary_tree(tree_node *head_node)
{
	tree_node *p = head_node->left_child;

	while(p != head_node)
	{
		while(p->left_flag == POINTER_NODE)
		{
			p = p->left_child;
		}
		printf("%c ", p->data);
		while(p->right_flag == POINTER_THREAD && p->right_child != head_node)
		{
			p = p->right_child;
			printf("%c ", p->data);
		}
		p = p->right_child;
	}
	printf("\n");
}
```

# 先序线索二叉树

&emsp;&emsp;先序线索二叉树在建立时，除了建立的顺序不一样，其他和中序的一样，这里，我就偷个懒，只贴个代码参考。

先序线索二叉树的建立：
```cpp
void pre_order_traverse_build_tree(tree_node *root, tree_node **pre_node)
{
	if(root != NULL)
	{
		if(root->left_child == NULL)
		{
			root->left_child = *pre_node;
			root->left_flag = POINTER_THREAD;
		}
		else
		{
			root->left_flag = POINTER_NODE;
		}

		if((*pre_node)->right_child == NULL)
		{
			(*pre_node)->right_child = root;
			(*pre_node)->right_flag = POINTER_THREAD;
		}
		else
		{
			(*pre_node)->right_flag = POINTER_NODE;
		}
		*pre_node = root;

		if(root->left_flag == POINTER_NODE)
		{
			pre_order_traverse_build_tree(root->left_child, pre_node);
		}
		pre_order_traverse_build_tree(root->right_child, pre_node);
	}
}

tree_node* build_thread_binary_tree(tree_node *root)
{
	tree_node *head_node = (tree_node *)malloc(sizeof(tree_node));
	tree_node *pre_node;

	if(root != NULL)
	{
		head_node->left_child = root;
		pre_node = head_node;
		pre_order_traverse_build_tree(head_node->left_child, &pre_node);
		head_node->right_child = pre_node;
		head_node->right_flag = POINTER_THREAD;
		pre_node->right_child = head_node;
		pre_node->right_flag = POINTER_THREAD;
	}
	else
	{
		head_node->left_child = head_node;
		head_node->right_child = head_node;
	}
	return head_node;
}
```

先序线索二叉树的遍历：

```cpp
void traverse_thread_binary_tree(tree_node *head_node)
{
	tree_node *p = head_node->left_child;

	while(p != head_node)
	{
		while(p->left_flag == POINTER_NODE)
		{
			printf("%c ", p->data);
			p = p->left_child;
		}
		printf("%c ", p->data);
		p = p->right_child;
	}
	printf("\n");
}
```

# 后序线索二叉树

&emsp;&emsp;后序线索二叉树是不完善的，要对它进行遍历，还需要使用栈来辅助，这里就不讲了。

# 结语
&emsp;&emsp;线索二叉树充分利用了指针空间，同时又便于寻找结点的前驱结点和后继结点。线索二叉树适用于经常需要遍历寻找结点前驱或者后继结点的二叉树。
