#!/usr/bin/python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 幂率变换
def exponential_transform():
	my_font = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

	x = range(0, 256, 1)

	c = 255.0 / (255.0 ** 0.04)
	y = [ c * (i ** 0.04) for i in x ]
	plt.plot(x, y, label="$\gamma = 0.04$")

	c = 255.0 / (255.0 ** 0.1)
	y = [ c * (i ** 0.1) for i in x ]
	plt.plot(x, y, label="$\gamma = 0.1$")

	c = 255.0 / (255.0 ** 0.2)
	y = [ c * (i ** 0.2) for i in x ]
	plt.plot(x, y, label="$\gamma = 0.2$")

	c = 255.0 / (255.0 ** 0.4)
	y = [ c * (i ** 0.4) for i in x ]
	plt.plot(x, y, label="$\gamma = 0.4$")

	c = 255.0 / (255.0 ** 0.67)
	y = [ c * (i ** 0.67) for i in x ]
	plt.plot(x, y, label="$\gamma = 0.67$")

	c = 255.0 / (255.0 ** 1)
	y = [ c * (i ** 1) for i in x ]
	plt.plot(x, y, label="$\gamma = 1$")

	c = 255.0 / (255.0 ** 1.5)
	y = [ c * (i ** 1.5) for i in x ]
	plt.plot(x, y, label="$\gamma = 1.5$")

	c = 255.0 / (255.0 ** 2.5)
	y = [ c * (i ** 2.5) for i in x ]
	plt.plot(x, y, label="$\gamma = 2.5$")

	c = 255.0 / (255.0 ** 5.0)
	y = [ c * (i ** 5.0) for i in x ]
	plt.plot(x, y, label="$\gamma = 5.0$")

	c = 255.0 / (255.0 ** 10.0)
	y = [ c * (i ** 10.0) for i in x ]
	plt.plot(x, y, label="$\gamma = 10.0$")

	c = 255.0 / (255.0 ** 25.0)
	y = [ c * (i ** 25.0) for i in x ]
	plt.plot(x, y, label="$\gamma = 25.0$")

	plt.xlabel("输入灰度级$r$", fontproperties=my_font)
	plt.ylabel("输出灰度级$s$", fontproperties=my_font)
	plt.xlim(0, 255)
	plt.ylim(0, 255)
	plt.legend()
	plt.show()

# 对比度拉伸
def contrast_stretch():
	my_font = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

	x = [0, 80, 255 - 80, 255]
	y = [0, 20, 255 - 20, 255]
	plt.plot(x, y)

	x_p = [80, 255 - 80]
	y_p = [20, 255 - 20]
	plt.plot(x_p, y_p, 'om')

	plt.annotate('$(r_1, s_1)$', xy=(80, 20), xytext=(80 + 5, 20 - 2))
	plt.annotate('$(r_2, s_2)$', xy=(255 - 80, 255 - 20), xytext=(255 - 80 + 5, 255 -20 - 10))

	plt.xlabel("输入灰度级$r$", fontproperties=my_font)
	plt.ylabel("输出灰度级$s$", fontproperties=my_font)
	plt.xlim(0, 255)
	plt.ylim(0, 255)
	plt.legend()
	plt.show()

# 灰度级分层
def grayscale_stratification():
	my_font = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

	x_1 = [0, 80, 80, 150, 150, 255]
	y_1 = [20, 20, 150, 150, 20, 20]
	plt.subplot(1, 2, 1)
	plt.plot(x_1, y_1)
	plt.xlabel("输入灰度级$r$", fontproperties=my_font)
	plt.ylabel("输出灰度级$s$", fontproperties=my_font)
	plt.xlim(0, 255)
	plt.ylim(0, 255)

	x_2 = [0, 80, 80, 150, 150, 255]
	y_2 = [0, 80, 200, 200, 150, 255]
	plt.subplot(1, 2, 2)
	plt.plot(x_2, y_2)
	plt.xlabel("输入灰度级$r$", fontproperties=my_font)
	plt.ylabel("输出灰度级$s$", fontproperties=my_font)
	plt.xlim(0, 255)
	plt.ylim(0, 255)

	plt.legend()
	plt.show()

if __name__ == "__main__":
	exponential_transform()
	# contrast_stretch()
	# grayscale_stratification()
