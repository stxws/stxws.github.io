---
title: '做了一个点阵屏'
date: 2021-07-16
categories: 其他
tags: [嵌入式, 单片机, MAX7219]
mathjax: true
---

# 先说两句

&emsp;&emsp;~~最近上班摸鱼太无聊了，~~因为和某人约定好了要送一个礼物，又因为最近做嵌入式的原因，有点手痒，想自己做个东西玩玩，所以打算开始做个点阵屏。然后前阵子学了一下kicad，打算拿这个练手，算是我第一次画电路板。感觉和大佬比起来，我这就像过家家一样🙃。

# MAX7219芯片

&emsp;&emsp;因为没学过硬件，画电路板没一点头绪，所以就花了5块钱从淘宝上买了一个8×8的点阵屏，打算~~抄~~参考一下，买来以后是这样的：

![](/images/other/lattice_screen/max7219_module.jpeg)

&emsp;&emsp;感觉比我想像的要简单一点，就一个芯片、一个点阵屏、一个电容和一个电阻。去找商家要了一下资料（[下载链接](/documnets/other/lattice_screen/MAX7219点阵模块资料.rar)），后来才知道这个芯片叫MAX7219。扫了一眼MAX7219的芯片手册，没怎么看懂🙃，结合资料里的样例代码才勉强看懂了一点点。

## 硬件方面

&emsp;&emsp;MAX7219一共有24个引脚，各个引脚的功能如下表：

| 管脚 | 名称 | 功能描述 |
| :--- | :--- | :---|
| 1 | DIN | 串行数据输入端口。在时钟上升沿时数据被载入内部的16位寄存器。 |
| 2,3,5-8,10,11 | DIG0–DIG7 | 八个数据驱动线路置显示器共阴极为低电平。关闭时此管脚输出高电平。 |
| 4,9 | GND | 地线(4 脚和 9 脚必须同时接地) |
| 12 | LOAD | 载入数据。连续数据的后16位在LOAD端的上升沿时被锁定。 |
| 13 | CLK | 时钟序列输入端。最大速率为10MHz.在时钟的上升沿,数据移入内部移位寄存器。下降沿时,数据从DOUT端输出。 |
| 14-17,20-23 | SEGA-SEGG,DP | 7段和小数点驱动,为显示器提供电流。当一个段驱动关闭时,此端呈低电平 |
| 18 | SET | 通过一个电阻连接到 $V_{DD}$ 来提高段电流。 |
| 19 | $V_{+}$ | 正极电压输入，+5V（好像3.3V）也可以 |
| 24 | DOUT | 串行数据输出端口,从DIN输入的数据在16.5个时钟周期后在此端有效。当使用多个MAX7219时用此端方便扩展。 |

&emsp;&emsp;然后8×8的点阵屏模块MAX7219部分的原理图是这样的：

![](/images/other/lattice_screen/max7219_design.png)

&emsp;&emsp;按照原理图，MAX7219的DIG0–DIG7接点阵屏的共阴极，SEGA-SEGG和DP接点阵屏的共阳极，DIN、CLK、LOAD接到MCU的IO口上，用来与MCU通信，DOUT接到下一个MAX7219的DIN上，用来实现多个级联。
然后其他引脚按照电路图接对应的元件和电源就好了。

## 软件方面

&emsp;&emsp;控制MAX7219的方式是写寄存器，MAX7219一共有14个8位的可寻址的数据寄存器和控制寄存器，MCU通过给这些寄存器写数据来控制MAX7219的工作。

### 写移位寄存器

&emsp;&emsp;刚刚说到，MAX7219有3个引脚（DIN、CLK、LOAD）是接到MCU的IO口上的，写寄存器就是通过这3个引脚来完成的。在MAX7219里有一个16位的移位寄存器，当CLK引脚出现一个上升沿的电压信号后，MAX7219就会将DIN端的信号移入移位寄存器里，作为移位寄存器的最后一位。
&emsp;&emsp;举个栗子，下图中在CLK的第1个上升沿，MCU给了DIN一个高电平，所以MAX7219的移位寄存器移入了一个1，然后在CLK的第2个上升沿，MCU给了DIN一个低电平，所以MAX7219的移位寄存器移入了一个0。最终的效果就是移位寄存器里原来的数据向前移动了两位，后两位数据变成了移入的1和0。

![](/images/other/lattice_screen/max7219_write_regitist.png)

&emsp;&emsp;按照上面说的方法，连续写16位数据，就可以把移位寄存器写成我们想要的数据了。

### 写内部寄存器

&emsp;&emsp;数据写入移位寄存器之后，就可以利用移位寄存器的数据来更改MAX7219的14个数据寄存器和控制寄存器（以下简称为内部寄存器）了。
&emsp;&emsp;移位寄存器的数据可以分成两个部分，一部分是用来表示内部寄存器的地址，占4位，位于第8到第11位，一部分是用来表示寄存器的数据，位于第0到第7位，如下图所示：

![](/images/other/lattice_screen/max7219_regitist_struct.png)

&emsp;&emsp;当MCU给LOAD引脚一个上升沿信号时，MAX7219就根据移位寄存器中的4个地址位，选择对应的内部寄存器，然后把移位寄存器里的8个数据位写入该寄存器中。
&emsp;&emsp;结合之前的写移位寄存器的方法，就可以实现将数据据写入对应的内部寄存器中了。这里给出一个用来写内部寄存器的参考代码：

```cpp
/**
 * @brief : 向MAX7219的移位寄存器写入一个字节的数据
 * @param data : [in]需要写入的数据
 */
void write_max7219_byte(unsigned char data)
{
	int i;

	for (i = 0; i < 8; i++)
	{
		write_max7219_pin(CLK_PIN, 0);
		if(data & 0x80)
		{
			write_max7219_pin(DIN_PIN, 1);
		}
		else
		{
			write_max7219_pin(DIN_PIN, 0);
		}
		write_max7219_pin(CLK_PIN, 1);
		data = data << 1;
	}
}

/**
 * @brief : 向MAX7219的内部寄存器写入数据
 * @param load_pin : [in]对应MAX7219的LOAD引脚
 * @param address : [in]内部寄存器地址
 * @param data : [in]需要写入内部寄存器的数据
 */
void write_max7219_register(max7219_pin_def load_pin, unsigned char address, unsigned char data)
{
	write_max7219_pin(load_pin, 0);
	write_max7219_byte(address);
	write_max7219_byte(data);
	write_max7219_pin(load_pin, 1);
}
```

### 内部寄存器

&emsp;&emsp;刚刚已经介绍了如何写内部寄存器，接下来就是如何用这14个内部寄存器控制MAX7219工作。这些寄存器分两类，一类是控制寄存器，共5个，分别用来设置编码模式、显示亮度、扫描限制、掉电模式以及显示检测，另一类是数据寄存器，用来设置显示的数据。

| 地址 | 寄存器 |
| :---: | :---: |
| 0x00 | 不工作寄存器 |
| 0x01-0x08 | 8个数据寄存器 |
| 0x09 | 译码模式寄存器 |
| 0x0A | 亮度控制寄存器 |
| 0x0B | 扫描控制寄存器 |
| 0x0C | 掉电模式寄存器 |
| 0x0F | 显示检测寄存器 |

&emsp;&emsp;数据寄存器很好理解，共8个，对应8个段选，每个8位，每一位对应SEGA～SEGG和SEGDP八个引脚的输出电平。MAX7219工作时，DIG0～7八个引脚会按顺序输出低电平，同时根据数据寄存器中的值，给SEG八个引脚输出对应的电平。比如，当前DIG引脚输出低电平时，其他DIG引脚都输出高电平，MAX7219就按照第2个数据寄存器（地址是0x03）中的值，给SEG引脚输出对应的电平，下一次就轮到给DIG3引脚输出低电平，按照第3个数据寄存器中的值，给SEG引脚输出对应的电平，如此循环八个引脚。
&emsp;&emsp;控制寄存器我没怎么细看，打算直接按照参考的驱动代码设置，如下：

```cpp
/**
 * @brief : 初始化MAX7219
 * @param load_pin : [in]对应MAX7219的LOAD引脚
 */
void init_max7219(max7219_pin_def load_pin)
{
	write_max7219_register(load_pin, 0x09, 0x00); /* 译码方式 */
	write_max7219_register(load_pin, 0x0a, 0x03); /* 亮度 */
	write_max7219_register(load_pin, 0x0b, 0x07); /* 扫描界限；8个数码管显示 */
	write_max7219_register(load_pin, 0x0c, 0x01); /* 掉电模式：0，普通模式：1 */
	write_max7219_register(load_pin, 0x0f, 0x00); /* 显示测试：1；测试结束，正常显示：0 */
}
```

&emsp;&emsp;按照上面的代码初始化好后，将要显示的内容写入数据寄存器就好了。比如要显示一个字母'A'的代码如下：

```cpp
/**
 * @brief : 让点阵屏显示一个A
 */
void show_a()
{
	int i;
	/* 字母A的点阵数据，1的位置是点阵屏上要亮的位置 */
	unsigned char data[8] = {0x08, 0x14, 0x22, 0x3E, 0x22, 0x22, 0x22, 0x22};
	/*	16进制         二进制
		 0x08 ---> 0 0 0 0 1 0 0 0
		 0x14 ---> 0 0 0 1 0 1 0 0
		 0x22 ---> 0 0 1 0 0 0 1 0
		 0x3E ---> 0 0 1 1 1 1 1 0
		 0x22 ---> 0 0 1 0 0 0 1 0
		 0x22 ---> 0 0 1 0 0 0 1 0
		 0x22 ---> 0 0 1 0 0 0 1 0
		 0x22 ---> 0 0 1 0 0 0 1 0
	*/

	init_max7219(CS1_PIN);
	for(i = 1; i <= 8; i++)
	{
		write_max7219_register(CS1_PIN, (unsigned char)i, data[i - 1]);
	}
}
```

# 点阵屏

&emsp;&emsp;点阵屏比较容易理解，就是一些led灯组成的点阵。分为共阴极和共阳极两种，共阴极点阵屏的同一行led阴极是连在一起的，同一列的阳极连在一起，而共阳极点阵屏同一行led的阳极是连在一起的，同一列的阴极连在一起。原理图如下（左边是共阳，右边是共阴）：

![](/images/other/lattice_screen/screen.png)

&emsp;&emsp;从点阵屏的正面看，四个边中有个一个边有突起，将那个边向下，这时点阵的行和列就和上图对应了。上图中圆圈里的编号是引脚编号，点阵屏一共有16个引脚，分成两行，按刚刚的方法放好，上面一排的引脚编号从左往右是16、15、...、9，下面一排的引脚编号从左往右是1、2、...、8。


# 硬件设计

## 原理图设计

&emsp;&emsp;看懂了MAX7219和点阵屏的工作原理后，就可以用kicad开始设计电路了。kicad是一个开源的PCB设计软件，用起来感觉不错，而且有中文文档教程，还跨平台，对于我这个新手来说相当友好，想了解的小伙伴可以去[kicad的官网](https://www.kicad.org)看看。

&emsp;&emsp;kicad的元件库里有MAX7219，可以直接拿来用，但是没有点阵屏，所以要自己加一个点阵屏元件，下图是我自己加的1088AS元件和封装：

![](/images/other/lattice_screen/1088AS.png)

&emsp;&emsp;接下来就是设计原理图了，MAX7219部分可以参考资料里的原理图来设计，要做成16×16的点阵的话，需要4个8×8点阵拼接起来，原理图就是下面这样的。

![](/images/other/lattice_screen/schematic_diagram_1.png)

&emsp;&emsp;MCU本来打算用STM32F103C8T6的，在淘宝上看了一下，发现最近因为芯片缺货的问题，C8T6涨到了30块钱一片😓....，不过C6T6价格还可以接受，6块一片，而且C6T6的引脚和C8T6的完全一样，用来替代C8T6刚刚好。去网上找了一个STM32F103C8T6最小系统板的资料，参考原理图改了一下，如下：

![](/images/other/lattice_screen/schematic_diagram_2.png)

&emsp;&emsp;完整的pdf原理图可以在[这里](/documnets/other/lattice_screen/schematic_diagram.pdf)查看。

## 电路设计

&emsp;&emsp;设计好原理图后开始设计电路。
&emsp;&emsp;首先选择封装，所有的电阻和电容都选择0603贴片，两个LED灯用了0805，USB插座想用type-c的，本来想用6PIN的，在kicad里没找到6PIN的封装，干脆就用16PIN的了，都差不多。其他的按照元件的尺寸随便选了一些。
&emsp;&emsp;接下来就是让人头大的布线了，唔....，第一次布线，感觉比想像中要难一些，改了很久才搞定，特别是MCU附近的线比较难走线。布好线后是这样的：

![](/images/other/lattice_screen/circuit_design.png)

&emsp;&emsp;kicad里有个3D查看器，可以模拟成品的样子，大概是这个样子的：

![](/images/other/lattice_screen/3d_view.png)

&emsp;&emsp;左边是正面，右边是背面，因为点阵屏的封装里没有3D模型，所以这个渲染出来就没有点阵屏。

## 制作

&emsp;&emsp;布好线后，在淘宝上找了个PCB打样的，发现22块钱能打10块板子，感觉还算比较便宜。打样好是这个样子的：

![](/images/other/lattice_screen/empty_baord.jpeg)

&emsp;&emsp;然后把需要的元件都买到后，开始焊板子，感觉比想像中要难焊一点，特别是焊MCU的时候，锡容易把两个引脚粘在一起，用了助焊剂后好了很多。焊好后是这样的：

![](/images/other/lattice_screen/baord_ok.jpeg)

&emsp;&emsp;焊的有点丑，有些电容和电阻歪了。接下来把点阵屏插上去应该就能用了。

# 写代码

## 环境搭建

&emsp;&emsp;用STM32CubeMX生成了一个工程（不清楚的小伙伴可以参考这篇[博客](/learn_note/linux_arm_config/)），按照电路的连接，配置对应引脚为GPIO上拉输出模式。

![](/images/other/lattice_screen/MCU_config.png)

&emsp;&emsp;接下来生成工程代码，make以后尝试烧录，烧录失败了....。openocd报了下面这个错：

```
> program build/lattice_screen.hex                                                
target halted due to debug-request, current mode: Thread 
xPSR: 0x01000000 pc: 0x08001038 msp: 0x20002800
** Programming Started **
device id = 0x10006412
SWD DPIDR 0x1ba01477
Failed to read memory at 0x1ffff7e2
STM32 flash size failed, probe inaccurate - assuming 32k flash
flash size = 32kbytes
stm32x device protected
failed erasing sectors 0 to 4
embedded:startup.tcl:530: Error: ** Programming Failed **
in procedure 'program' 
in procedure 'program_error' called at file "embedded:startup.tcl", line 595
at file "embedded:startup.tcl", line 530
```

&emsp;&emsp;一开始还以为是芯片某个引脚没焊好，然后检查一下电路，发现没问题。百度了一下，网上说是因为芯片flash上了锁，要解锁才能烧录，参考了一下大佬的这篇[博客](https://www.brobwind.com/archives/1139)，用openocd执行下面的解锁命令后，就可以烧录了。

```
> reset halt
target halted due to debug-request, current mode: Thread 
xPSR: 0x01000000 pc: 0x08001038 msp: 0x20002800
> stm32f1x unlock 0
stm32x unlocked.
INFO: a reset or power cycle is required for the new settings to take effect.

> reset halt
target halted due to debug-request, current mode: Thread 
xPSR: 0x01000000 pc: 0xfffffffe msp: 0xfffffffc
```

## 汉字编码生成

&emsp;&emsp;要显示一个汉字，需要有对应的汉字编码，自己设计比较麻烦，在网上找了一个大佬写的生成16×16汉字点阵的[代码](https://blog.twofei.com/embedded/hzk.html)。大致的原理是用汉字的GB2312编码，在HZK16字库中，索引到对应的编码，然后打印出来。

## 显示逻辑

&emsp;&emsp;前面说了8×8点阵屏的显示逻辑，现在是16×16的，也就是4个8×8拼在一起，所以只要让每个8×8显示对应的内容就好了，显示一个汉字的代码如下：

```cpp
/**
 * @brief : 让16*16点阵屏显示一个字
 */
void show_word(unsigned char *word_code)
{
	int i;
	for(i = 0; i < 16; i++)
	{
		if(i % 2 == 0)
		{
			write_max7219_register(CS4_PIN, (unsigned char)(i / 2 + 1), word_code[i]);
		}
		else
		{
			write_max7219_register(CS2_PIN, (unsigned char)(i / 2 + 1), word_code[i]);
		}
	}
	for(i = 16; i < 32; i++)
	{
		if(i % 2 == 0)
		{
			write_max7219_register(CS3_PIN, (unsigned char)(i / 2 - 8 + 1), word_code[i]);
		}
		else
		{
			write_max7219_register(CS1_PIN, (unsigned char)(i / 2 - 8 + 1), word_code[i]);
		}
	}
}
```

&emsp;&emsp;接下来实现一个字符串的循环移动显示，其实也很简单，只要在一定的延时后，把汉字编码按照一定的逻辑，循环移动一位，然后再把开头显示出来就好了。循环移位的代码如下：

```cpp
/**
 * @brief : 将字的编码循环移动一位
 * @param word_code : [in/out]字的编码
 * @param word_count : [in]字的个数
 */
void cyclic_shift_word(unsigned char *word_code, int word_count)
{
	int i, len;
	unsigned short front;
	unsigned char *p = word_code;

	front = 0x0000;
	for(i = 0; i < 16; i++)
	{
		if((p[2 * i] & 0x80) != 0)
		{
			front += (0x0001 << i);
		}
	}
	len = word_count * 32;
	for(i = 0; i < len - 32; i++)
	{
		if(i % 2 == 0)
		{
			p[i] = (p[i] << 1) + (p[i + 1] >> 7);
		}
		else
		{
			p[i] = (p[i] << 1) + (p[i + 31] >> 7);
		}
	}
	for(i = len - 32; i < len; i++)
	{
		if(i % 2 == 0)
		{
			p[i] = (p[i] << 1) + (p[i + 1] >> 7);
		}
		else
		{
			p[i] = (p[i] << 1) + ((front >> ((i + 31 - len) / 2)) & 0x0001);
		}
	}
}
```

&emsp;&emsp;主函数代码：

```cpp
HAL_Delay(2); // 防止MAX7219未正常启动
init_screen();
while (1)
{
	show_word(word_code);
	cyclic_shift_word(word_code, WORD_COUNT);
	HAL_Delay(180);
}
```

# 成果演示

<center><video src="/images/other/lattice_screen/run_show.mp4" controls="controls" autoplay="autoplay" loop="loop"></video></center>

&emsp;&emsp;虽然点阵屏算是比较简单的一个东西，但是因为是第一次自己画板子，设计电路，感觉还是挺好玩的。
&emsp;&emsp;这个点阵屏的硬件设计和代码都已经放到github上了，<https://github.com/stxws/lattice_screen>。

<style>
	.post-block img{
		max-width: 400px;
		max-height: 400px;
	}
</style>