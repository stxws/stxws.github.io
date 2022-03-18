---
title: '图像的几何空间变换'
date: 2020-07-03 09:54:55
categories: 图像处理
tags: [图像处理, opencv]
mathjax: true
---

# 介绍
&emsp;&emsp;图像的几何空间变换可以改进图像中像素间的空间关系，主要由两个基本操作组成：
* 坐标空间的变换。
* 图像内插，对空间变换后的像素赋值。

## 空间坐标变换
&emsp;&emsp;可由下式表示：
$$(x, y) = T\{(v, w)\}$$

&emsp;&emsp;上式中$(v, w)$是原图中像素的坐标，$(x, y)$是变换后图像的坐标，$T$是变换函数，也就是原图中某个位置的像素通过变换函数，映射到目标图像中。比如：$(x, y) = T{(v, w)} = (v/2, w/2)$表示在两个方向上将原图缩小一半。

## 图像内插
&emsp;&emsp;请参考我的另一篇博文[图像内插](/image_processing/interpolation/)。

# 仿射变换
&emsp;&emsp;仿射变换是最常用的空间坐标变换之一，其一般形式如下：
$$
\left[\begin{matrix} x & y & 1 \end{matrix}\right] = 
\left[\begin{matrix} v & w & 1 \end{matrix}\right]T = 
\left[\begin{matrix} v & w & 1 \end{matrix}\right]
\left[\begin{matrix}
t_{11} & t_{12} & 0 \\\\
t_{21} & t_{22} & 0 \\\\
t_{31} & t_{32} & 1
\end{matrix}\right]
$$

&emsp;&emsp;上式中，$T$表示变换矩阵，可根据$T$中元素所选择的值，对一组坐标点做尺度、旋转、平移或偏移。

|变换名称|变换矩阵$T$|坐标公式|例子|
|:---:|:---:|:---:|:---:|
| 恒等变换 | $\left[\begin{matrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1\end{matrix}\right]$ | $x = v \\\\ y = w$ | ![](/images/image_processing/space_transformation/affine_t_1.png) |
| 尺度变换 | $\left[\begin{matrix} c_x & 0 & 0 \\\\ 0 & c_y & 0 \\\\ 0 & 0 & 1\end{matrix}\right]$ | $x = c_x v \\\\ y = c_y w$ | ![](/images/image_processing/space_transformation/affine_t_2.png) |
| 平移变换 | $\left[\begin{matrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ t_x & t_y & 1\end{matrix}\right]$ | $x = v + t_x \\\\ y = w + t_y$ | ![](/images/image_processing/space_transformation/affine_t_3.png) |
| 旋转变换 | $\left[\begin{matrix} \cos\theta & \sin\theta & 0 \\\\ -\sin\theta & \cos\theta & 0 \\\\ 0 & 0 & 1\end{matrix}\right]$ | $x = v\cos\theta - w\sin\theta \\\\ y = v\sin\theta + w\cos\theta$ | ![](/images/image_processing/space_transformation/affine_t_4.png) |
| 垂直偏移变换 | $\left[\begin{matrix} 1 & s_h & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1\end{matrix}\right]$ | $x = v \\\\ y = w + s_hv$ | ![](/images/image_processing/space_transformation/affine_t_5.png) |
| 水平偏移变换 | $\left[\begin{matrix} 1 & 0 & 0 \\\\ s_v & 1 & 0 \\\\ 0 & 0 & 1\end{matrix}\right]$ | $x = v + s_vw \\\\ y = w$ | ![](/images/image_processing/space_transformation/affine_t_6.png) |

# 实现
&emsp;&emsp;实现空间变换的方法有两种：
* **前向映射**：整体思想是扫描原图像，对于原图像上的每个像素，根据它在原图中的坐标$(v, w)$，利用$(x, y) = T\{(v, w)\}$计算其在目标图像上的坐标$(x, y)$，然后将原图中坐标为$(v, w)$的像素值赋值给目标图像中坐标为$(x, y)$的像素。
* **反向映射**：整体思想是扫描目标图像的每个像素，对于坐标为$(x, y)$的像素，利用$(v, w) = T^{-1}\{(x, y)\}$计算其在原图像上的坐标$(v, w)$，然后用内插的方法计算该像素的值。
&emsp;&emsp;这里$T^{-1}$表示变换函数的反函数，对于仿射变换来说，相当于$\left[\begin{matrix} x & y & 1 \end{matrix}\right]$乘变换矩阵的逆矩阵。

&emsp;&emsp;使用前向映射可能会存在两个问题，一个是原图像中多个像素被变换到目标图像的同一个位置，产生冲突，另一个问题是计算出的目标像素坐标不存在，比如不是个整数坐标。而反向映射不存在这两个问题，因此反向映射用的多一点。
&emsp;&emsp;这里给出用反向映射实现仿射变换的C++代码，代码用的是opencv库处理图像。
```cpp
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

/* 原图路径 */
char img_path[100] = "img/affine.png";
/* 变换后图像的大小 */
Size img_out_size = {300, 300};
/* 仿射矩阵 */
double T[3][3] = 
{
	{1, 0, 0},
	{0, 1, 0},
	{0, 0, 1},
};

/* 利用双线性内插计算原图中的浮点像素值 */
double bilinear_interpolation(Mat src, double x, double y)
{
	if(x < 0 || x > src.cols || y < 0 || y > src.rows)
	{
		return 0;
	}

	/* 表示在原图中与浮点像素最近的四个整数坐标值(lx:左x、rx:右x、uy:上y、dy:下y) */
	double lx = (int)x;
	double rx = lx + 1;
	double uy = (int)y;
	double dy = uy + 1;

	/* 先计算y方向的两个像素点值f1、f2，再计算xy两个方向上的像素点值 */
	double f1 = (rx - x) * src.at<uchar>(uy, lx) + (x - lx) * src.at<uchar>(uy, rx);
	double f2 = (rx - x) * src.at<uchar>(dy, lx) + (x - lx) * src.at<uchar>(dy, rx);
	double xy = (dy - y) * f1 + (y - uy) * f2;
	return xy;
}

int main()
{
	int i, j;
	Mat src = imread(img_path, cv::IMREAD_GRAYSCALE);
	src.rows -= 2;
	Mat dst = Mat(img_out_size, src.type());

	Mat t_s = Mat(3, 3, CV_64FC1, T);
	Mat t_inv = Mat(3, 3, CV_64FC1);
	invert(t_s, t_inv); // t_inv为仿射矩阵的逆矩阵

	Mat src_vec, dst_vec;
	for(i = 0; i < dst.rows; i++)
	{
		for(j = 0; j < dst.cols; j++)
		{
			/* 目标图像的坐标向量 */
			dst_vec = (Mat_<double>(1, 3) << j, i, 1);
			/* 计算dst_vec对应于原图中的坐标向量src_vec */
			src_vec = dst_vec * t_inv;
			/* 计算目标图像的浮点像素值 */
			dst.at<uchar>(i, j) = (uchar)bilinear_interpolation(src, src_vec.at<double_t>(0, 0), src_vec.at<double_t>(0, 1));
		}
	}
	imshow("dst", dst);
	imwrite("img/t_1.png", dst);

	waitKey(0);
	return 0;
}
```