---
title: '图像内插'
date: 2020-03-23 23:05:39
categories: 图像处理
tags: [图像处理,opencv]
mathjax: true
---
关于常见的图像内插方法的介绍
<!-- more -->

&emsp;&emsp;内插是在诸如放大、收缩、旋转和几何校正等任务中广泛应用的基本工具，是一种基本的图像重取样方法，本质上，内插是用已知数据来估计未知位置的数值的处理。本文介绍的内插主要用于调整图像的大小（收缩和放大）。
# 最近邻内插
&emsp;&emsp;最近邻内插根据原图像和目标图像的尺寸，计算缩放的比例，然后根据缩放比例计算离目标像素最近的原像素，将该原像素作为目标像素。
&emsp;&emsp;假设原图像大小为$W_s \times H_s$，目标图像大小为$W_d \times H_d$，原图像在$(x0,y0)$位置处的像素表示为$f_s(x0,y0)$，则目标图像在$(x, y)$位置处的像素$f_d(x,y)$的计算公式如下：

$$f_d(x, y) = f_s(\lfloor \frac{W_s}{W_d} \times x + 0.5 \rfloor, \lfloor \frac{H_s}{H_d} \times y + 0.5 \rfloor)$$

&emsp;&emsp;上式中$\lfloor \frac{W_s}{W_d} \times x + 0.5 \rfloor$表示对$\frac{W_s}{W_d} \times x$四舍五入。
&emsp;&emsp;最近邻内插算法实现的图像缩放的原理很简单，但缺点是得到的图像效果不太好[^1]。代码可以参考下文的 nearest_interpolation() 函数。
[^1]: 有关最近邻内插的内容参考了<https://www.cnblogs.com/skyfsm/p/7578302.html>

# 双线性内插
&emsp;&emsp;双线型内插利用了源图中虚拟点四周的四个真实存在的像素，来共同决定目标图中的一个像素，使用双线性内插的缩放效果比简单的最邻近内插要好很多。
计算方法：
&emsp;&emsp;假设原图像大小为$W_s \times H_s$，目标图像大小为$W_d \times H_d$，首先根据源图像和目标图像的尺寸比例，计算目标图像像素坐标$(x_d,y_d)$在原图像中浮点坐标$(x_f,y_f)$，计算公式如下：

$$x_f = \frac{W_s}{W_d} \times x_d$$

$$y_f = \frac{H_s}{H_d} \times y_d$$

&emsp;&emsp;接下来在原图像中寻找离浮点坐标$(x_f,y_f)$最近的四个像素点，分别是坐标为$(\lfloor x_f \rfloor,\lfloor y_f \rfloor)$，$(\lfloor x_f + 1 \rfloor,\lfloor y_f \rfloor)$，$(\lfloor x_f \rfloor,\lfloor y_f + 1 \rfloor)$，$(\lfloor x_f + 1 \rfloor,\lfloor y_f + 1 \rfloor)$的四个像素。根据这四个像素计算出浮点坐标的像素值，再将浮点坐标的像素值作为目标图像对应位置的像素值。浮点坐标的像素值的计算方法如下：
&emsp;&emsp;首先，在$x$方向上进行两次线性插值计算，计算出$(x_f,\lfloor y_f \rfloor)$和$(x_f,\lfloor y_f + 1 \rfloor)$处的像素值，计算公式如下，设原图中在点$(x,y)$处的像素值为$f_s(x,y)$

$$f_s(x_f,\lfloor y_f \rfloor) = (\lfloor x_f + 1 \rfloor - x_f) \times f_s(\lfloor x_f \rfloor,\lfloor y_f \rfloor) + (x_f - \lfloor x_f \rfloor) \times f_s(\lfloor x_f + 1 \rfloor,\lfloor y_f \rfloor$$

$$f_s(x_f,\lfloor y_f + 1 \rfloor) = (\lfloor x_f + 1 \rfloor - x_f) \times f_s(\lfloor x_f \rfloor,\lfloor y_f + 1 \rfloor) + (x_f - \lfloor x_f \rfloor) \times f_s(\lfloor x_f + 1 \rfloor,\lfloor y_f + 1 \rfloor)$$

&emsp;&emsp;然后利用$f_s(x_f,\lfloor y_f \rfloor)$和$f_s(x_f,\lfloor y_f + 1 \rfloor)$在$y$方向上进行一次插值计算，得出$f_s(x_f,y_f)$，计算公式如下：

$$f_s(x_f,y_f) = (\lfloor y_f + 1\rfloor - y_f) \times f_s(x_f,\lfloor y_f \rfloor) + (y_f - \lfloor y_f \rfloor) \times f_s(x_f,\lfloor y_f + 1 \rfloor)$$

&emsp;&emsp;实际上，双线性内插是根据四个像素点与浮点坐标的距离来计算四个像素点的权重，然后将四个像素点的加权平均和作为浮点坐标的像素值。图片使用双线性内插的缩放效果要优于最邻近内插，但是计算量要比最邻近内插大一点[^2]。代码可以参考下文的 bilinear_interpolation() 函数。
[^2]: 有关双线性内插的内容参考了<https://www.cnblogs.com/yssongest/p/5303151.html>

# 双三次内插
&emsp;&emsp;双三次内插的原理于双线性内插相似，都是根据浮点坐标附近的像素来计算出浮点坐标的像素值，计算时也是根据与浮点坐标之间的距离来计算附近像素点的权重，最后根据附近像素点的权重和像素值取加权平均和。与双线性内插不同的是，双三次内插计算了浮点坐标附近的16个像素点，而双线性内插只计算了4个。
&emsp;&emsp;双三次内插的核心问题是，如何根据像素点与浮点坐标的距离计算权重，有关双三次内插的计算方法参考自<https://blog.csdn.net/qq_29058565/article/details/52769497>，我偷个懒，就不再详细解释了。
&emsp;&emsp;与前面两种内插方法相比，双三次内插在保存细节方面比双线性内插相对要好一些，但是计算量比前两种方法都要高一些，是商业图像编辑程序如Adobe Photoshap和Corel Photopaint的标准内插方法[^3]。
[^3]: 此处引用自冈萨雷斯的《数字图像处理》第三版第37页。

# 代码
&emsp;&emsp;使用opencv库实现的，只能处理灰度图。
```cpp
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

/* 最近邻内插 */
void nearest_interpolation(Mat src, Mat &dst, Size dst_size)
{
	int i, j, x, y;
	/* 计算原图像与目标图像的宽度和高度比例 */
	double wsd = (double)src.cols / dst_size.width;
	double hsd = (double)src.rows / dst_size.height;

	dst = Mat(dst_size, src.type());
	for(i = 0; i < dst.rows; i++)
	{
		y = hsd * i + 0.5;
		for(j = 0; j < dst.cols; j++)
		{
			x = wsd * j + 0.5;
			dst.at<uchar>(i, j) = src.at<uchar>(y, x);
		}
	}
}

/* 双线性内插 */
void bilinear_interpolation(Mat src, Mat &dst, Size dst_size)
{
	int i, j;
	/* 计算原图像与目标图像的宽度和高度比例 */
	double wsd = (double)src.cols / dst_size.width;
	double hsd = (double)src.rows / dst_size.height;
	/* 表示原图中的浮点像素 */
	Point2f sfp;
	/* 表示在原图中与浮点像素最近的四个整数坐标值(左x、右x、上y、下y) */
	double lx, rx, uy, dy;
	/* x方向的两个像素点值，xy两个方向上的像素点值 */
	double xf1, xf2, xyf;

	dst = Mat(dst_size, src.type());
	for(i = 0; i < dst.rows; i++)
	{
		sfp.y = hsd * i;
		for(j = 0; j < dst.cols; j++)
		{
			sfp.x = wsd * j;
			lx = (int)sfp.x;
			rx = lx + 1;
			uy = (int)sfp.y;
			dy = uy + 1;

			xf1 = (rx - sfp.x) * src.at<uchar>(uy, lx) + (sfp.x - lx) * src.at<uchar>(uy, rx);
			xf2 = (rx - sfp.x) * src.at<uchar>(dy, lx) + (sfp.x - lx) * src.at<uchar>(dy, rx);
			xyf = (dy - sfp.y) * xf1 + (sfp.y - uy) * xf2;
			dst.at<uchar>(i, j) = (uchar)xyf;
		}
	}
}

int main()
{
	Mat src, dst;
	Size dst_size = cv::Size(2000, 1000);

	src = cv::imread("img/img1.png", cv::IMREAD_COLOR);
	cvtColor(src, src, COLOR_BGR2GRAY);
	imshow("src", src);

	nearest_interpolation(src, dst, dst_size);
	imshow("nearest interpolation", dst);

	bilinear_interpolation(src, dst, dst_size);
	imshow("bilinear interpolation", dst);

	/* opencv的双线性内插接口 */
	cv::resize(src, dst, dst_size, 0, 0, INTER_LINEAR);
	imshow("opencv resize", dst);

	waitKey(0);
	return 0;
}
```