---
title: 'shell脚本基础知识'
date: 2020-05-10 22:30:26
categories: 学习笔记
tags: [linux,shell]
---

# 简介
## shell
&emsp;&emsp;shell是操作系统内核之外的指令解析器，是一个程序，同时是一种命令语言和程序设计语言。是处于操作人员和操作系统接口之间的一层封装，用于方便操作人员使用计算机。
用途：
1. 用于计算机的启动、常用程序的运行等脚本。
2. 作为配置文件。
3. 处理文本文件。

&emsp;&emsp;常用的shell：sh、bash。

## shell脚本
&emsp;&emsp;将多行命令封装进一个文本文件里，执行一个shell脚本即可执行多个shell命令。
&emsp;&emsp;shell的第一行用于指定脚本解释器的路径，方法是`#!解释器的路径`，比如指定为/bin/sh的代码如下：
```shell
#!/bin/sh
```

# 执行方式
&emsp;&emsp;shell有两种执行方式，第一种是`脚本解释器 shell文件`，第二种是`./shell文件`。使用第二种方式时，要确保shell文件有可执行权限。
```shell
bash ./test.sh  # 第一种方式
./test.sh  # 第二种方式
```

# 注释
## 单行注释
&emsp;&emsp;shell脚本里用#来表示单行注释，如果使用第一种方式执行shell，第一行的`#!`也是注释；如果用第二种方式执行shell，第一行的`#!`则不是注释。
```shell
#!/bin/sh

# 这是一个注释
ls -l # 这也是一个注释
```
## 多行注释
1. 方法一

```shell
: '
echo "这是一个注释"
echo "这也是注释"
echo "这还是注释"
'
```
**注意**：注释的开头的`:`和`'`之间有一个空格，不然会报错。

2. 方法二

```shell
:<< 字符
echo "这是一个注释"
echo "这也是注释"
echo "这还是注释"
字符
```
&emsp;&emsp;这里的字符上下两个要相同，否则注释无法结束。


# 别名
&emsp;&emsp;给命令取其他名字，用来简化带参数的命令，比如使用`alias ll='ls -l'`命令来给`ls -l`取一个`ll`的别名，以后就可以用`ll`来代替`ls -l`了。
&emsp;&emsp;如果是在终端输入`alias`命令后取的别名，在终端退出后别名就会失效，下次开启终端后，需要再执行一次`alias`命令才能使用别名。如果想要在每次开启终端后都能使用别名，需要把`alias`命令写入~/.bashrc文件里。

# 输入输出
## 输出
&emsp;&emsp;echo命令用于将字符输出到标准输出，语法：`echo [可选项] 要输出的字符串...`，可选项有两个：
* -n ：输出后不换行，默认会换一行。
* -e ：输出前解析转义字符（类似`\n`之类的），默认不解析。

```shell
$ echo 'abc!'   # 输出后会换一行
abc!
$ echo -n 'abc!'   # 输出后不换行
abc!$ 

$ echo 'abc\nabc'  # 不解析转义字符，将\n当做普通字符串输出
abc\nabc
$ echo -e 'abc\nabc'  # 解析转义字符，将\n当做换行符输出
abc
abc
$ 
```

&emsp;&emsp;cat命令用于将文件的内容输出到标准输出，语法：`cat 要输出的文件`。

## 输入
&emsp;&emsp;read命令会从标准输入中读取字符串，保存到变量中，语法：`read 保存输入的变量`。
```shell
$ read VAR
abc   # 输入的字符串
$ echo ${VAR}
abc
$ 
```
&emsp;&emsp;也可以用read命令将读取的字符串保存到多个变量中，语法：`read 变量1 变量2 ...`。read命令读取到空格就换一个变量来保存字符串，读取到回车停止读取。
```shell
$ read VAR1 VAR2
abc 123  # 输入的字符串
$ echo ${VAR1}
abc
$ echo ${VAR2}
123
$ 
```
&emsp;&emsp;用read将输入保存到变量时，如果想将空格当做普通字符保存到变量中，可以在空格前加一个反斜杠来转义。
```shell
$ read VAR1 VAR2
abc\ 123 xyz       
$ echo ${VAR1}
abc 123
$ echo ${VAR2}
xyz
$ 
```
&emsp;&emsp;当用来保存输入的变量是最后一个变量的时候，即使不加反斜杠来转义，也会把空格当做普通字符来处理。
```shell
$ read VAR1 VAR2
abc 123 xyz
$ echo ${VAR1}
abc
$ echo ${VAR2}
123 xyz  # 变量VAR2是最后一个保存输入的变量
$   # 所以“123”和“xyz”之间的空格，即使不加反斜杠，也当做普通字符处理
```
&emsp;&emsp;如果后面的变量还没有用到，read就读取到了换行，那么，没用到的变量会赋值为空字符串。
```shell
$ VAR1=xyz
$ VAR2=123
$ read VAR1 VAR2
abc
$ echo ${VAR1}
abc
$ echo ${VAR2} # 变量VAR2原来是123，现在是空字符串。

$ 
```


## 文件重定向
&emsp;&emsp;一个进程启动时，默认会打开3个文件描述符。
* 0 标准输入　STDIN_FILENO
* 1 标准输出　STDOUT_FILENO
* 2 标准错误　STDERR_FILENO

&emsp;&emsp;一般在终端运行的命令会将当前终端作为标准输入、标准输出和标准错误，如果想用一个文件去替换终端，作为该命令的标准输入、标准输出或者标准错误，则需要用到输入输出重定向。输入输出重定向的语法如下：
* `commad 0<file` ：将file文件作为commad命令的标准输入，0可以省略。
* `commad 1>file` ：将commad命令的标准输出重定向到file文件，会覆盖file文件原来的内容，用`>>`替换`>`就不会覆盖，会将标准输出追加到file文件里。1也可以省略，效果是一样的。
* `commad 2>file` ：将commad命令的标准错误重定向到file文件，覆盖写入，用`>>`表示追加，这里2不可以省略。
* `commad 1>file 2>&1` ：将commad命令的标准输出和标准错误都重定向到file文件，会覆盖file文件原来的内容，用`>>`表示追加，前面的1可以省略。

```shell
./a.out <in.txt    # 将in.txt文件作为./a.out的输入
./a.out >out.txt   # 将./a.out的标准输出重定向到out.txt文件中，覆盖写入
./a.out >>out.txt   # 将./a.out的标准输出重定向到out.txt文件中，追加写入
./a.out 2>out.txt   # 将./a.out的标准错误重定向到out.txt文件中，覆盖写入
```

# 管道
&emsp;&emsp;用`|`表示，即将前一条命令的执行结果，利用管道传给下一条命令，作为下一条命令的输入，比如查看test.cpp文件里所有包含`printf`的行可以使用以下命令：
```sh
cat test.cpp | grep 'printf'
```

# 变量
&emsp;&emsp;变量是一段内存名字。shell里只有字符串和整数两种类型的变量。shell变量常用大写英文字符表示。
## 声明
&emsp;&emsp;shell变量可以用`declare`来声明。设定属性的选项：
* -a&emsp;声明下标数组 (如果支持)
* -A&emsp;声明关联数组 (如果支持)
* -i&emsp;声明整型变量
* -r&emsp;声明只读变量
* -n&emsp;声明指向一个以其值为名称的变量的引用
* -x&emsp;声明一个变量，并将变量导出，有关导出的内容会在下文的[环境变量](#环境变量)里解释。
* -t&emsp;声明带有`trace'(追踪)属性的变量
* -l&emsp;将变量在赋值时转为小写
* -u&emsp;将变量在赋值时转为大写

&emsp;&emsp;如果在声明变量时，不指定任何属性，则默认为声明一个字符串类型的变量。
```shell
#声明一个下标数组
declare -a MY_ARRAY

#声明一个整型变量
declare -i MY_INT

#声明一个只读变量，并将其初始化为'123'
declare -r MY_READ_ONLY='123'

#声明一个变量，并将变量导出
declare -x MY_EXPORT

#声明一个字符串变量
declare MY_STRING
```
&emsp;&emsp;其实，字符串类型的变量不用`declare`声明也可以赋值或者使用，相当于一个空字符串。
```shell
$ echo "MY_VAR=${MY_VAR};" #在没有用`declare`声明时，使用'MY_VAR'变量
MY_VAR=;
$ MY_VAR=123 #在没有用`declare`声明时，给'MY_VAR'变量赋值
$ echo "MY_VAR=${MY_VAR};"
MY_VAR=123;
```

## 使用
语法：`$变量名`或`${变量名}`
```shell
echo $VAR
echo ${VAR}
```
&emsp;&emsp;推荐使用加大括号的方式，可以增强代码的可读性。

## 赋值
语法：`变量名=给变量赋的值`
&emsp;&emsp;赋值和初始化时等号两边不要加空格。
&emsp;&emsp;只读变量初始化后不能再赋值了。

## 释放
语法：`unset 变量名`
```shell
$ VAR=123
$ echo "VAR=${VAR};"
VAR=123;
$ unset VAR
$ echo "VAR=${VAR};"
VAR=;
```
&emsp;&emsp;变量VAR在释放之前的值是123，在释放之后是一个空字符串。

## 局部变量
&emsp;&emsp;局部变量(local variable)是用户自定义的变量，`declace`不加`-x`声明的变量都是局部变量。局部变量只在当前shell进程中有效，其父shell进程和其创建的子shell进程都无法使用。

## 环境变量
&emsp;&emsp;环境变量(global variable)也叫全局变量。与局部变量不同，当前shell进程在创建子shell进程时，会将环境变量复制给子shell进程，使其成为子进程的环境变量，而当前shell进程的局部变量不会复制。
&emsp;&emsp;可以用`export`将局部变量导出为环境变量，语法：`export 要导出的局部变量名`。
&emsp;&emsp;下面，用两个例子来说明环境变量和局部变量的区别。假设当前目录下有一个test.sh脚本，里面只有一条`echo`命令，如下：
```shell
echo "VAR=${VAR};"
```
**第一个例子**
&emsp;&emsp;首先在终端中声明一个名称为VAR的局部变量，然后用bash执行test.sh脚本，结果如下：
```shell
$ declare VAR='123'
$ bash ./test.sh
VAR=;
```
&emsp;&emsp;在这个例子中，当前终端可以当做一个shell进程，执行`bash ./test.sh`命令会创建一个子shell进程，然后用创建的子shell进程去解析test.sh里的命令。因为VAR是一个局部变量，所以在创建子shell进程时，不会将VAR变量复制给子shell进程，所以子shell进程执行test.sh后输出的VAR是一个空字符串。

**第二个例子**
&emsp;&emsp;首先在终端中声明一个名称为VAR的局部变量，先将VAR用`export`导出为环境变量，然后再用bash执行test.sh脚本，结果如下：
```shell
$ declare VAR='123'
$ export VAR
$ bash ./test.sh 
VAR=123;
```
&emsp;&emsp;与第一个例子不同的地方是VAR被导出成了环境变量，当前终端在创建子shell进程的时候会将VAR复制，成为子shell进程的环境变量，所以输出的VAR是字符串'123'。

***
&emsp;&emsp;可以用`env`、`export`、`set`命令来查看当前shell进程的环境变量。
&emsp;&emsp;常用的环境变量：
* **HOME**：home目录路径
* **PWD**：当前目录路径
* **LOGNAME**：当前用户用户名
* **PATH**：shell命令的存放路径，每个路径用引号分隔，用于shell寻找命令。

## 特殊变量
* **$0**：用于保存的是当前运行的可执行文件的名字。
* **$1~9**：用于保存给shell脚本或者shell脚本里的函数传的参数，一共有9个。
* **$#**：用于保存传的参数个数，\$0不在计数范围内。
* **$\***：以单个字符串的形式保存传的参数，即\$1~9，不包括\$0。
* **$@**：以字符串数组的形式保存传的参数，不包括\$0。
* **$?**：用于保存上一条命令或者函数的返回值，值为0表示正常退出。
* **$$**：当前shell进程的PID。
* **$!**：用于保存上一个放到后台运行的进程的PID，注意，不是前台进程。
* **$-**：显示shell使用的当前选项，与set命令功能相同。(这个没弄懂)

# 后台切换
&emsp;&emsp;在命令后面加一个`&`可以将该命令切换到后台工作，这样不用等待该命令结束就可以执行下一条命令了。
```
./a.out &
ls -l
```
&emsp;&emsp;上面这个例子，假设`./a.out`需要执行10秒，如果不加`&`，则`ls -l`需要等10秒后，也就是`./a.out`执行结束后才能运行，加了`&`就不需要等待`./a.out`结束就能运行`ls -l`了。
&emsp;&emsp;使用这种切换到后台的进程，在终端退出后就会结束，如果想在退出终端后，后台进程任然继续运行，需要用到`nohup`命令。
```
nohup ./a.out &
```
&emsp;&emsp;使用`nohup`命令会将切换到后台的进程的输出写入到当前目录的nohup.out文件里。

# 特殊字符
## 双引号
&emsp;&emsp;双引号用来使shell将空格、制表符和其他大多数特殊字符当做普通字符来处理。举个栗子：
```shell
touch aaa bbb
touch "aaa bbb"
```
&emsp;&emsp;没加双引号时，`aaa`和`bbb`之间的空格表示命令参数分隔符，`touch`命令会创建两个文件“aaa”和“bbb”。
&emsp;&emsp;加了双引号时，`aaa`和`bbb`之间的空格表示普通字符，与a和b的意义相同，`touch`命令只会创建一个文件“aaa bbb”。

## 单引号
&emsp;&emsp;作用与双引号类似，区别是双引号只能将空格、制表符等部分特殊符号当普通字符来处理，而单引号可以作用于所有字符。比如`$`符号(用于引用变量)加了双引号还是特殊字符，加单引号则表示普通字符。
```shell
echo ${PATH}
echo "${PATH}"
echo '${PATH}'
```
&emsp;&emsp;上面的三行命令，第一行和第二行的作用相同，都是输出PATH变量，第三行命令只会输出字符串“$PATH”。

## 反引号
&emsp;&emsp;反引号用于使shell将字符串当做命令来处理。举个例子：
```shell
echo ls -l
echo `ls -l`
```
&emsp;&emsp;第一行命令会将字符串“ls -l”输出，第二行命令则会先执行`ls -l`命令，然后用`echo`命令将`ls -l`的执行结果输出。
&emsp;&emsp;反引号也可以用`$()`来代替，比如`` `ls -l` ``和`$(ls -l)`是等效的。

## 反斜杠
&emsp;&emsp;转义字符，将反斜杠后面的字符当做普通字符来处理。
```shell
touch aaa\ bbb
```
&emsp;&emsp;上面命令里的空格被转义为普通字符，执行命令后会创建一个“aaa bbb”文件。

## 分号
&emsp;&emsp;可以在一行执行多条命令，分号表示一条命令的结束。
```shell
echo "hello world"; ls -la;
```

## 空格、制表符、换行符
&emsp;&emsp;当做空白。

## 其他符号
1. **\*\?\!^**：用于shell的[模式](#模式)匹配。
2. **<>**：用于输入输出重定向，见[文件重定向](#文件重定向)。
3. **|**：用于使用管道，见[管道](#管道)。
4. **$**：用于引用变量，见[变量](#变量)。
5. **&**：将命令放到后台运行，见[后台切换](#后台切换)。
6. **#**：在shell脚本里表示单行注释，见[单行注释](#单行注释)。
7. **()**：`$()`用来表示括号里的是命令，和[反引号](#反引号)作用相同。`$(())`用来表示[表达式运算](#表达式运算)。
8. **\[\]**：用于shell的[模式](#模式)匹配，或者用来表示[表达式运算](#表达式运算)，也可以用来表示[条件判断](#条件判断)。
9. **{}**：用于shell的[模式](#模式)匹配，或者用来引用[变量](#变量)，也可以用来生成序列，用法见[for语句](#for语句)。

# 模式和正则表达式
&emsp;&emsp;shell里的模式一般用来匹配文件路径，正则表达式则是用来匹配字符串的。
## 模式
&emsp;&emsp;shell的模式包括普通字符和通配符，这里列出常用的一些通配符：

| 通配符 | 含义 | 实例 |
| :---: | :----: | :--- |
| `*` | 匹配0个或多个字符 | `a*b`，a与b之间可以有任意长度的任意字符, 也可以一个也没有，比如：aabcb, axyzb, a012b, ab。|
| `?` | 匹配任意一个字符 | `a?b`，a与b之间必须也只能有一个字符, 可以是任意字符，比如：aab, abb, acb, a0b。|
| `[list]` | 匹配list中的任意单一字符 | `a[xyz]b`，a与b之间必须也只能有一个字符, 但只能是x或y或z, 比如：axb, ayb, azb。|
| `[c1-c2]` | 匹配c1到c2之间的任意一个字符 | `a[0-9]b`，a与b之间必须也只能有一个0到9之间的字符，比如：a0b, a1b... a9b。|
| `[!list]`或`[^list]` | 匹配除list中的任意单一字符 | `a[!xyz]b`，a与b之间必须也只能有一个字符, 但不能是x、y、z, 比如：a0b, apb, a-b。
| `[!c1-c2]`或`[^c1-c2]` | 匹配不在c1-c2的任意字符 | `a[!0-9]b`，比如：acb adb。 |
| `{string1,string2,...}` | 匹配sring1或string2(或更多)其一字符串 | `a{abc,xyz,123}b`，a与b之间必须是abc或xyz或123，比如：aabcb,axyzb,a123b |

&emsp;&emsp;shell里的模式一般用来匹配多个文件或文件夹的路径，使用模式的常用命令有：ls、find、cp、mv、chmod...。
```shell
$ ls -1 test_[0-9].sh
test_0.sh
test_1.sh
test_2.sh
```

## 正则表达式
&emsp;&emsp;正则表达式是用来匹配字符串的。linux里的grep是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹配的行打印出来，这里用grep来演示正则表达式。
&emsp;&emsp;正则表达式常用元字符集：

| 字符 | 含义 |
| :---: | :--- |
| `\` | 转义字符 |
| `^` | 匹配字符串的开始位置 |
| `$` | 匹配字符串的结束位置 |
| `.` | 匹配任意一个字符 |
| `[list]` | 匹配list里的任意一个字符。例如，`[abc]`可以匹配 "plain" 中的 'a'。 |
| `[^list]` | 匹配除了list里的其他任意一个字符。例如，`[^abc]`可以匹配"plain"中的'p'、'l'、'i'、'n'。 |
| `[c1-c2]` | 匹配c1到c2之间的任意字符。例如，`[a-z]`可以匹配'a'到'z'范围内的任意小写字母字符。|
| `[^c1-c2]` | 匹配不在c1到c2之间的任意字符。例如，`[^a-z]`可以匹配任何不在'a' 到'z'范围内的任意字符。|
| `x\|y` | 匹配x或y。例如，`z\|food`能匹配"z"或"food"，`(z\|f)ood`则匹配"zood"或"food"。 |
| `()` | 标记一个子表达式的开始和结束位置。 |
| `*` | 匹配前面的子表达式零次或多次。例如，`zo*`能匹配"z"以及"zoo"。`*`等价于`{0,}`。 |
| `+` | 匹配前面的子表达式一次或多次。例如，`zo+`能匹配"zo"以及"zoo"，但不能匹配 "z"。`+`等价于`{1,}`。 |
| `?` | 匹配前面的子表达式零次或一次。例如，`do(es)?`可以匹配"do"或"does"。`?`等价于`{0,1}`。 |
| `{n}` | 匹配前面的子表达式确定的n次。例如，`o{2}`不能匹配"Bob"中的'o'，但是能匹配"food"中的两个'o'。 |
| `{n,}` | 至少匹配前面的子表达式n次。例如，`o{2,}`不能匹配 "Bob" 中的 'o'，但能匹配"foooood"中的所有'o'。 |
| `{n,m}` | 最少匹配前面的子表达式n次且最多匹配m次。例如，`o{1,3}`将匹配"fooooood"中的前三个'o'。注意，在逗号和两个数之间不能有空格。
| `\b` | 匹配一个单词边界，也就是指单词和空格(shell里的grep并不限于空格，单词和'.'、'_'之间也能匹配)间的位置。例如，`er\b`可以匹配"never" 中的"er"，但不能匹配 "verb" 中的"er"。 |
| `\B` | 匹配非单词边界。`er\B`能匹配"verb"中的"er"，但不能匹配"never"中的"er"。 |
| `\d` | 匹配一个数字字符。等价于`[0-9]`。 |
| `\D` | 匹配一个非数字字符。等价于 [^0-9]。 |
| `\w` | 匹配字母、数字、下划线。等价于`[A-Za-z0-9_]`。 |
| `\W` | 匹配非字母、数字、下划线。等价于`[^A-Za-z0-9_]`。 |
| `\xn` | 匹配n，其中n为十六进制转义值。十六进制转义值必须为确定的两个数字长。例如，`\x41`匹配"A"。`\x041`则等价于'\x04'&"1"。正则表达式中可以使用ASCII编码。
| `\s` | 匹配任何空白字符，包括空格、制表符、换页符等等。等价于`[\f\n\r\t\v]`。
| `\S` | 匹配任何非空白字符。等价于`[^\f\n\r\t\v]`。 |

&emsp;&emsp;**注意**：shell里用grep时，`|`、`()`、`{}`、`+`、`?`需要转义。比如：
```shell
$ ls -1 | grep 'test_1\{2\}'
test_11.sh
```
&emsp;&emsp;上面的`{`和`}`前面要加`\`转义。

# 表达式运算
## 运算符
&emsp;&emsp;shell里的运算符基本跟c语言的一样
* 基本运算符：+、-、*、/(加减乘除)、%(取模)
* 逻辑运算符：&&、||、!(与或非)
* 位运算符：&(与)、|(或)、^(异或)、~(取反)、<<(位左移)、>>(位右移)
* 赋值运算符：=、+=、*=、/=、%=、&=、|=、^|、<<=、.....

## 格式
&emsp;&emsp;shell里用`$[表达式]`表示中括号里的是表达式，也可以用`$((表达式))`来表示，推荐使用中括号的形式。
&emsp;&emsp;**注意**：shell里只能对整形变量进行表达式运算，不能对字符串类型的变量进行表达式运算
```shell
$ declare -i VAR1=123
$ declare -i VAR2=111
$ echo $[VAR1 + VAR2]
234
```

## expr命令
&emsp;&emsp;也可以用expr命令来进行表达式运算，expr命令支持的运算符有：|、&、<、<=、=、!=、>=、+、-、*、/、%。语法：`expr 表达式`，举个栗子：
```shell
$ expr 123 + 111  # 加法运算
234
$ VAR1=333
$ VAR2=234
$ expr ${VAR1} - ${VAR2}  # 变量１减变量２
99
$ expr ${VAR1} \* ${VAR2}  # 变量１乘变量２
77922
$ expr ${VAR1} / ${VAR2}  # 变量１除变量２
1
```
&emsp;&emsp;**注意**：运算符两边都有一个空格。部分运算符前面要加个`\`来转义，比如*、&、(、>。
&emsp;&emsp;还可以用小括号来组成更复杂的表达式。
```shell
$ expr 12 \* \( 34 - 26 \)  # 乘号和小括号前都要加\
96
$ declare -i VAR1=413
$ declare -i VAR2=34
$ expr ${VAR1} % \( ${VAR2} - 21 \) 
10
```
&emsp;&emsp;expr还可以进行简单的字符串运算，支持的有：
* **字符串 : 正则表达式**： 在字符串中由给定正则表达式决定的锚定模式匹配。
* **match 字符串 正则表达式**：与“字符串 : 正则表达式”相同。
* **substr 字符串 位置 长度**：从某个位置开始，截取指定长度的子串，位置由 1 开始计数。
* **index 字符串 字符**：字符串中第一次出现指定字符的位置，如果不存在该字符，则输出0。
* **length 字符串**：字符串的长度。

```shell
$ expr substr 'this is a test' 2 8
his is a
$ expr length 'this is a test'
14
$ expr index 'this is a test' s
4
```
&emsp;&emsp;expr命令会将计算结果输出到标准输出，如果想将结果保存到变量里，可以用反引号来实现。
```shell
$ VAR=`expr 23 \* 42`
$ echo ${VAR}
966
```

# 条件判断
&emsp;&emsp;shell里可以用test命令进行条件判断。语法：`test 表达式`或者`[ 表达式 ]`(注意这里中括号和表达式之间的空格不能省)。
&emsp;&emsp;可以通过查看变量\$?的值，来判断表达式是否成立，如果成立，test命令返回值为0，变量\$?的值也是0，如果不成立，则值为非0。test命令可以进行的条件判断包括以下几种。

## 字符串判断
* **-z 字符串**：字符串的长度为 0
* **-n 字符串**：字符串长度非零
* **字符串**：等价于`-n 字符串`
* **字符串1 = 字符串2**：字符串相等
* **字符串1 != 字符串2**：字符串不相等

```shell
$ VAR=''
$ [ -z ${VAR} ] # 判断字符串${VAR}长度是否为0
$ echo $?  # 查看test命令的返回值
0
$ VAR='abc'
$ [ -z ${VAR} ]
$ echo $?
1
$ [ ${VAR} = 'abc' ] # 判断字符串${VAR}是否等于'abc'
$ echo $?
0
$ [ ${VAR} = '123' ]
$ echo $?
1
```

## 整数判断
* **整数1 -eq 整数2**：整数1与整数2相等
* **整数1 -ge 整数2**：整数1大于或等于整数2
* **整数1 -gt 整数2**：整数1大于整数2
* **整数1 -le 整数2**：整数1小于或等于整数2
* **整数1 -lt 整数2**：整数1小于整数2
* **整数1 -ne 整数2**：整数1和整数2不相等

## 文件判断
* **-e 文件**：文件存在
* **-d 文件**：文件存在且为目录
* **-f 文件**：文件存在且为普通文件
* **-r 文件**：文件存在且有可读权限
* **-w 文件**：文件存在且有可写权限
* **-x 文件**：文件存在且有可执行（或搜索）权限
* **-b 文件**：文件存在且为块特殊文件
* **-c 文件**：文件存在且为字符特殊文件
* **-g 文件**：文件存在且被设置了 set-group-ID 位
* **-g 文件**：文件存在且为有效组ID 所有
* **-h 文件**：文件存在且为一个符号链接（与 -L 相同）
* **-L 文件**：文件存在且为一个符号链接（与 -h 相同）
* **-k 文件**：文件存在且被设置粘着位
* **-O 文件**：文件存在且为有效用户ID 所有
* **-p 文件**：文件存在且为命名管道
* **-s 文件**：文件存在且其大小大于零
* **-S 文件**：文件存在且为套接字
* **-u 文件**：文件存在且被设置了 set-user-ID 位
* **-t FD**：文件描述符 FD 在某个终端打开
* **文件1 -ef 文件2**：文件1 和文件2 拥有相同的设备编号与 inode 编号
* **文件1 -nt 文件2**：文件1 在修改时间上新于文件2
* **文件1 -ot 文件2**：文件1 比文件2 更旧

## 逻辑判断
* **! 表达式**：表达式为假
* **表达式1 -a 表达式2**：表达式1 与表达式2 皆为真
* **表达式1 -o 表达式2**：表达式1 或表达式2 为真

# 分支结构
## if语句
&emsp;&emsp;直接上语法：
```shell
if 条件1
then
	条件1成立时执行的命令
elif 条件2
then
	条件1不成立，且条件2成立时执行的命令
else
	条件1和条件2都不成立时执行的命令
fi # 结束if语句
```
&emsp;&emsp;这里的条件一般是一条shell命令，比如`test`、`gcc`等。如果命令的返回值为0，则条件成立。
&emsp;&emsp;小实验：
```shell
$ cat shell.sh 
#!/bin/sh

if [ ${1} -gt ${2} ]  # 判断${1}是否大于${2}
then
	echo 'num_1 > num_2'
elif [ ${1} -eq ${2} ]  # 判断${1}是否等于${2}
then
	echo 'num_1 = num_2'
else
	echo 'num_1 < num_2'
fi

$ ./shell.sh 12 12
num_1 = num_2
$ ./shell.sh 12 11
num_1 > num_2
$ ./shell.sh 12 13
num_1 < num_2
```

## case语句
&emsp;&emsp;语法：
```shell
case 字符串 in
模式1)
	# 模式1能匹配字符串时执行的命令
	;; # 表示结束
模式2)
	# 模式2能匹配字符串时执行的命令
	;; # 结束
*)
	# 以上模式都不匹配时执行的命令
	;; # 结束
esac # 结束case语句
```
&emsp;&emsp;case语句只能对字符串进行判断，这里的模式是指正则表达式。

# 循环结构
## for语句
&emsp;&emsp;语法：
```shell
for VAR in item1 item2 .... itemN
do
	# 循环内的命令
done
```
&emsp;&emsp;举个栗子：
```shell
$ cat shell.sh 

for VAR in aaa bbb ccc
do
	echo ${VAR}
done

$ bash shell.sh 
aaa
bbb
ccc
```
&emsp;&emsp;然后再介绍几种shell里与for语句搭配使用的形式。
1. `{s..e}`：用来生成从s到e的序列，s和e可以是整数，也可以是大小写字母。
```shell
$ echo {-3..12}
-3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12
$ echo {a..z}
a b c d e f g h i j k l m n o p q r s t u v w x y z
```
&emsp;&emsp;这里要注意的是，s和e中间有**两个**点，多一个或少一个都不行。
&emsp;&emsp;如果s和e是整数的话，可以在s和e前面加0，达到自动用0补全的效果，比如：
```shell
$ echo {001..012}
001 002 003 004 005 006 007 008 009 010 011 012
```
&emsp;&emsp;这个和for循环搭配使用，就可以从s循环到e了，举个栗子：
```shell
$ cat shell.sh 

for i in {01..04}
do
	echo "str_${i}"
done

$ bash shell.sh 
str_01
str_02
str_03
str_04
```

2. `` `命令` ``或者`$(命令)`：用for语句来循环shell命令的输出，下面的例子用for语句输出当前目录的所有文件：
```shell
for FILE_NAME in `ls`
do
	echo ${FILE_NAME}
done
```
&emsp;&emsp;这里再重点介绍一下seq命令，seq命令也是用来生成序列的，与`{s..e}`不同的是，seq可以生成浮点数序列，但是不能生成大小写字母序列，用法有三种，如下：
- seq [选项]... 尾数
- seq [选项]... 首数 尾数
- seq [选项]... 首数 增量 尾数

&emsp;&emsp;首数默认是1，增量默认也是1，可用的选项有三个：

| 选项 | 描述 |
| --- | --- |
| -f | 指定生成的序列中每个数字的格式，指定方式和c语言的printf函数方式相同，<br>比如`%2.1f`，要注意的是只能用`%f`，`%d`和`%lf`都不行。 |
| -s | 指定分隔数字的字符串，默认是换行`\n`。 |
| -w | 通过填充前导零来均衡宽度，这个不能和`-f`同时使用。 |

&emsp;&emsp;一些例子：
```shell
$ seq 3 # 只有一个数字的，生成从1到该数字的序列，默认增量是1
1
2
3
$ seq -s ' ' 12  # 用空格来分隔数字
1 2 3 4 5 6 7 8 9 10 11 12
$ 
$ seq -s ' ' -3 12  # 有两个数字的，生成两个数字之间增量为1的序列
-3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12
$ 
$ seq -s ' ' -3 0.8 12 # 三个数字的
-3.0 -2.2 -1.4 -0.6 0.2 1.0 1.8 2.6 3.4 4.2 5.0 5.8 6.6 7.4 8.2 9.0 9.8 10.6 11.4
$ 
$ seq -s '__' -3 12  # 用'__'来分隔数字
-3__-2__-1__0__1__2__3__4__5__6__7__8__9__10__11__12
$ 
$ seq -s ' ' -w -3 12  # 通过填充前导零来均衡宽度
-3 -2 -1 00 01 02 03 04 05 06 07 08 09 10 11 12
$ 
$ seq -s ' ' -f %05.2f 12  # 指定数字的格式
01.00 02.00 03.00 04.00 05.00 06.00 07.00 08.00 09.00 10.00 11.00 12.00
```
&emsp;&emsp;seq与for语句搭配使用：
```shell
$ cat shell.sh 

for i in `seq -3 12`
do
	echo -n "${i} "
done
echo

$ bash shell.sh 
-3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 
```

3. 最后一种是for语句和路径通配符，举个栗子：
```shell
$ cat shell.sh 
# 用for语句输出当前目录下的所有文件
for FILE_NAME in ./*
do
	echo -n "${FILE_NAME} "
done
echo

$ bash shell.sh 
./a.out ./in.txt ./out.txt ./shell.sh ./test.cpp 
```

## while语句
&emsp;&emsp;语法：
```shell
while 条件测试
do
	# 循环内的命令
done
```
&emsp;&emsp;while语句首先进行条件测试，如果条件为真，则进入循环，直到条件为假时退出循环，跟C语言的一样。while语句的一个经典的用法是搭配输入重定向，读取文件的内容，下面是一个例子：
```shell
while read VAR # 读取标准输入的一行
do
	echo ${VAR}
done < in.txt # 将in.txt文件重定向到标准输入
```

## until语句
&emsp;&emsp;语法：
```shell
until 条件测试
do
	# 循环内的命令
done
```
&emsp;&emsp;until语句在条件为假时进入循环，条件为真时退出循环，其他和while语句相同。

# 其他命令

## find
&emsp;&emsp;find命令用于查找文件，这里简单的列出一些常用的用法，更详细的用法可以查manpages。

### 根据文件名查找
&emsp;&emsp;语法`find 查找的路径 -name pattern`，查找文件名与[模式](#模式)pattern相匹配的文件。比如查找当前目录下所有以'.sh'结尾的文件。
```shell
find ./ -name "*.sh"
```

### 根据正则表达式查找
&emsp;&emsp;语法`find 查找的路径 -regex pattern`，查找文件名与[正则表达式](#正则表达式)pattern相匹配的文件。比如查找当前目录下所有以'test'开头的文件。
```shell
find ./ -regex '^\./test.*'
```

### 根据路径查找
&emsp;&emsp;语法`find 查找的路径 -path pattern`，查找文件的完整路径与[模式](#模式)pattern相匹配的文件。与`-name`的区别是`-name`不匹配文件所在的目录，举个栗子：
```shell
$ find ./shell -name "*sh*"
./shell
./shell/test_1.sh
$ find ./shell -path "*sh*"
./shell
./shell/stxws.txt
./shell/test_1.sh
```

&emsp;&emsp;使用`-name`匹配文件'./shell/stxws.txt'时，只匹配文件名'stxws.txt'，因为'stxws.txt'和模式"\*sh\*"不匹配，所以不输出。使用`-path`匹配文件'./shell/stxws.txt'时，会匹配文件的完整路径'./shell/stxws.txt'，而'./shell/stxws.txt'和模式"\*sh\*"匹配成功。

### 根据文件类型查找
&emsp;&emsp;语法`find 查找的路径 -type c`，查找文件文件类型是c的文件，类型包括：
- b ：特殊块文件(缓冲的)
- c ：特殊字符文件(不缓冲)
- d ：目录
- p ：命名管道(FIFO)
- f ：普通文件
- l ：符号链接
- s ：套接字

&emsp;&emsp;查找当前目录下的普通文件：
```shell
find ./ -type f
```

### 根据文件大小查找
&emsp;&emsp;语法`find 查找的路径 -size n[单位]`，查找文件大小是n的文件，默认的单位是512字节的块，也可以使用其他单位，支持的单位有：
- b ：块(512字节)
- c ：字节
- w ：字(2字节)
- k ：千字节
- M ：兆字节
- G ：千兆字节

&emsp;&emsp;还可以在n前面加个加号和减号，加个加号表示查找文件大小大于n的文件，减号表示小于，如果不加的话则查找文件大小刚好等于n的文件。举个栗子：
```shell
# 查找当前目录下文件大小等于8个块的文件
find ./ -size 8b

# 查找当前目录下文件大小大于100千字节的文件（不包括等于100千字节的文件）
find ./ -size +100k

# 查找当前目录下文件大小小于10兆的文件（不包括等于10M的文件）
find ./ -size -10M
```
&emsp;&emsp;这里还有一个要注意的细节是，n必须是整数，所以低阶单位换算成高阶单位要向上取整，比如某个大小为70字节的文件，换算成块是70÷512=0.13671875块，但是用块来查找的时候，find命令将这个文件大小当做等于1个块来处理。

### 根据时间查找
&emsp;&emsp;语法：`find 查找的路径 -[时间类型][时间单位] n`，参数的关键字由时间类型和时间单位组成，时间类型包括三种：
- 访问时间 ：对文件的最后一次的访问时间，用a表示。
- 修改时间 ：文件数据最后一次的修改时间，用m表示。
- 变化时间 ：文件状态(例如权限、所有者等)最后一次修改时间，用c表示。

时间单位支持两种：
- min ：分钟
- time ：24个小时

将三种时间类型和两种时间单位组合，可以产生6种参数：
- -amin n ：对文件的最后一次的访问时间是在n分钟之前。
- -atime n ：对文件的最后一次的访问时间是在n×24小时之前。
- -mmin n ：文件数据最后一次的修改时间是在n分钟之前。
- -mtime n ：文件数据最后一次的修改时间是在n×24小时之前。
- -cmin n ：文件状态最后一次修改时间是在n分钟之前。
- -ctime n ：文件状态最后一次修改时间是在n×24小时之前。

&emsp;&emsp;举个栗子：
```shell
# 查找当前目录下，最后一次的访问是在5分钟之前的文件。
find ./ -amin 5

# 查找当前目录下，文件数据最后一次的修改时间是在2×24小时之前的文件。
find ./ -mtime 2
```

&emsp;&emsp;如果n前面加个负号，则查找的是对应时间离现在不超过n的文件，举个栗子：
```shell
# 查找当前目录下，最后一次的访问时间离现在不超过5分钟的文件。
find ./ -amin -5
```

&emsp;&emsp;还可以以某个文件的最后一次修改时间作为参照，来查找文件。
- -anewer file ：对文件的最后一次访问时间在file的最后一次修改时间之后。
- -newer file ：文件数据最后一次的修改时间在file的最后一次修改时间之后。(注意这里前面不要加m)
- -cnewer file ：文件状态最后一次修改时间在file的最后一次修改时间之后。

```shell
# 查找当前目录下，最后一次的访问时间在./test.sh文件的最后一次修改时间之后的文件。
find ./ -anewer ./test.sh
```

### 根据文件所有者查找
参数：
- -user uname ：文件的所有者是uname(也可以使用数字形式的用户ID)。
- -group gname ：文件属于gname(也允许使用数字形式的组ID)群组。

```shell
# 查找当前目录下，文件所有者是root的文件。
find ./ -user root

# 查找当前目录下，文件所在群组为root的文件。
find ./ -group root
```

### 根据权限查找
- -perm mode ：文件的权限位恰好是mode(八进制或符号)。
- -perm -mode ：mode中的所有的权限位都被设置了的文件。
- -perm +mode ：mode中的任意一个的权限位被设置了的文件。

```shell
# 查找当前目录下，权限是0777的文件。
find ./ -perm 0777

# 查找当前目录下，文件所有者既有可写，又有可执行权限的文件。
find ./ -perm -0300

# 查找当前目录下，文件所有者有可写，或者有可执行权限的文件。
find ./ -perm +0300 # 这条命令会报错“find: 非法权限 ‘+0300’”，不知道为什么
```

### 多条件查找
&emsp;&emsp;可以用与或非逻辑，查找满足多种条件的命令。
- !或-not ：查找不满足条件的文件。
- -a或-and ：查找两个条件都满足的文件。(默认的条件连接逻辑)
- -o或-or ：查找满足任意一个条件的文件。

&emsp;&emsp;举个栗子：
```shell
# 查找当前目录下，除文件目录外的所有文件
find ./ ! -type d

# 查找当前目录下，文件大小在2M到100M之间的文件
find ./ -size +2M -and -size -100M

# 查找当前目录下，以.png或.jpg结尾的文件
find ./ -name "*.png" -or -name "*.jpg"
```
&emsp;&emsp;逻辑运算的优先级是“! > -not > 缺省与 > -a > -and > -o > -or”。如果要提高运算的优先级，可以用小括号括起来。举个栗子：
```shell
# 查找当前目录下，以.png或.jpg结尾，且大小大于1M的文件
find ./ \( -name "*.png" -or -name "*.jpg" \) -and -size +1M
```
&emsp;&emsp;上面的命令中，如果不加扩号，会先进行与运算，再进行或运算。加了括号以后，则优先进行括号里的或运算，再进行与运算。
&emsp;&emsp;要注意的是两个括号前面要加`\`转义，而且前后都要用空格和其他参数分开。

### 找到文件后执行命令
&emsp;&emsp;find命令可以用`-exec`和`-ok`参数，在找到的文件后执行特定的命令。举个栗子：
```shell
# 查找当前目录下以.sh结尾的文件，并将找到的文件移动到./shell/目录下
find ./ -name "*.sh" -exec mv {} ./shell/ \;
```
&emsp;&emsp;上述命令中，`{}`表示找到的文件，`\;`表示命令的结束。
&emsp;&emsp;find命令中，`-exec`和`-ok`的区别是，使用`-ok`在每次执行命令前会进行确认是否执行，`-exec`则直接执行，不确认。
&emsp;&emsp;如果在对找到的文件要执行多条命令，可以使用多次`-exec`或`-ok`，举个栗子：
```shell
# 将当前目录下的文件输出两遍
find ./ -exec echo {} \; -exec echo {} \;
```

## sed

还没学会

## awk

&emsp;&emsp;awk是一个文本分析工具，用于分割处理文本内容。其主要工作流程是：将输入内容以记录为单位，逐个记录读入，用域分割字符串将每个记录分割成多个子字符串，分割后的这些子字符串叫作域，然后用处理指令对分割后的域进行处理。

&emsp;&emsp;awk有三种方式调用方式：

1. 命令行方式。语法：`awk [-F 域分割字符串] 处理指令 输入文件`。
2. shell脚本方式。将所有的处理指令插入一个文件，并使awk程序可执行，然后awk命令解释器作为脚本的首行，通过键入脚本名称来调用。相当于把shell脚本首行的：`#!/bin/sh`，换成：`#!/bin/awk`。
3. 将所有的awk命令插入一个单独文件，然后调用：`awk -f awk-script-file 输入文件`，其中，-f选项加载awk-script-file中的awk脚本。

&emsp;&emsp;实际上awk算是一种编程语言，深入研究的话，涉及的内容比较多，这里只简单介绍一下常用的用法，想深入研究的小伙伴可以去看[GNU的官方文档](https://www.gnu.org/software/gawk/manual/gawk.html)。

### 记录

&emsp;&emsp;在awk里，记录的分割用RS变量指定的字符分隔开来，RS默认是换行符，所以一般情况下，一条记录就是一行。可以通过在BEGIN里修改RS的值，来修改记录分隔字符，关于BEGIN，后面再说。

### 域

&emsp;&emsp;awk对记录进行处理时，会将其分割成多个域，将分割后的域按顺序存到$1、$2、..$n变量里，$0存的是整条记录。

&emsp;&emsp;域分割字符串用`-F`加一个[正则表达式](#正则表达式)来指定，不指定时，默认用空格、制表符等空白字符组成的字符串（相当于`-F "[\f\n\r\t\v ]*"`）作为域分割字符串。下面是一个awk中分割域的例子：

``` shell
$ cat ./awk_input.txt 
12 | 24 | 48
4  | 8  | 6
5  | 11 | 17
10 | 20 | 30

# 使用正则表达式"[ |]*"作为域分割字符串
$ awk -F "[ |]*" '{ printf("%2s %2s %2s\n", $1, $2, $3); }' ./awk_input.txt 
12 24 48
 4  8  6
 5 11 17
10 20 30

# 使用默认的空白字符作为域分割字符串
$ awk '{ printf("%2s %2s %2s\n", $1, $2, $3); }' ./awk_input.txt 
12  | 24
 4  |  8
 5  | 11
10  | 20
```

&emsp;&emsp;上面的例子中，printf是awk的一种输出语句，用法和C语言几乎一样。`printf("%2s %2s %2s\n", $1, $2, $3);`语句用于输出当前记录的第1、2、3个域。

&emsp;&emsp;第一条awk命令使用正则表达式"[ |]*"匹配每条记录，每条记录共匹配到了两个域分割字符串，所以被分割成了3个域。第二条awk命令使用默认的域分割字符串（空格、制表符等空白字符组成），共匹配到了4个域分割字符串，所以每条记录被分割成了5个域（3个整数、两个"|"）。

### 变量

&emsp;&emsp;包括内置变量和自定义的变量。

常用的内置变量：

|          |         |
| :---     | :---    |
| $n       | 第n个域 |
| $0       | 所有域  |
| ARGC     | 命令行参数个数 |
| ARGV     | 命令行参数排列 |
| ENVIRON  | 支持队列中系统环境变量的使用 |
| FILENAME | awk浏览的文件名 |
| FNR      | 浏览文件的记录数 |
| FS       | 设置输入域分隔符，等价于命令行-F选项 |
| NF       | 当前记录的域的个数 |
| NR       | 已读的记录数 |
| OFS      | 输出域分隔符 |
| ORS      | 输出记录分隔符 |
| RS       | 控制记录分隔符 |

&emsp;&emsp;自定义的变量和[shell的变量](#变量)很相似。举个简单的例子，将每个记录第2个域的值+1，存到变量`num`中，然后输出`num`的值：

``` shell
$ cat ./awk_input.txt 
12  24  48
4   8   6
5   11  17
10  20  30
$ awk '{ num = $2 + 1; printf("第%d行第2个域+1后的值：%d\n", NR, num); }' ./awk_input.txt 
第1行第2个域+1后的值：25
第2行第2个域+1后的值：9
第3行第2个域+1后的值：12
第4行第2个域+1后的值：21
```

### 数组

&emsp;&emsp;awk可以使用关联数组这种数据结构，索引可以是数字或字符串。awk关联数组不需要提前声明其大小，因为它在运行时可以自动的增大或减小。用起来和C++的map很像。

数组使用的语法格式：
```
array_name[index] = value
```

#### 创建数组

&emsp;&emsp;直接对数组赋值就可以创建数组了，举个栗子：

``` shell
$ pwd | awk '{ arr[2] = "111"; arr["aaa"] = "222"; printf("%s %s\n", arr[2], arr["aaa"]); }'
111 222
```

&emsp;&emsp;上面的例子中，数组arr分别用了数字2和字符串"aaa"作为索引，数组里存的数据都是字符串。

#### 删除数组元素

&emsp;&emsp;可以使用`delete`语句来删除数组元素，语法格式如下：
```
delete array_name[index]
```

删除数组元素例子：
``` shell
$ pwd | awk '{ arr[2] = "111"; printf("%s\n", arr[2]); delete arr[2]; printf("%s\n", arr[2]); }'
111

```

&emsp;&emsp;上面的例子中，删除arr\[2\]后，数组对应的值变成了空。

### 模式

&emsp;&emsp;awk的每条处理指令包括两部分，模式和动作，模式是用来控制动作的执行的。如果没有模式的话，默认对每一条记录都执行动作，比如前面举的awk的例子，都没有指定模式
这里简单介绍一下三种类型的模式：1、条件模式，2、正则表达式，3、BEGIN和END。

1. 条件模式：顾名思义，就是对符合条件的记录才进行处理，举个例子：
``` shell
$ cat ./awk_input.txt 
12 | 24 | 48
4  | 8  | 6
5  | 11 | 17
10 | 20 | 30

# 这条awk指令的条件模式是"$2 > 15"，作用是只对第2个域大于15的记录执行后面的动作
# 第2行和第3行的第2个域都小于15，不符合条件，所以没有执行动作里的printf语句
$ awk -F "[ |]*" '$2 > 15 { printf("第%d行第2个域大于15\n", NR); }' ./awk_input.txt 
第1行第2个域大于15
第4行第2个域大于15
```

2. 正则表达式：只对能用正则表达式匹配上的行进行处理，使用正则表达式作为模式的话，正则表达式要放在两个`/`中间，举个例子：
``` shell
$ cat ./awk_input.txt 
12 | 24 | 48
4  | 8  | 6
5  | 11 | 17
10 | 20 | 30

# 这条awk指令使用正则表达式".*2.*"，意思是只对包含2的记录执行后面的动作
$ awk '/.*2.*/ { printf("第%d行包含2\n", NR); }' ./awk_input.txt 
第1行包含2
第4行包含2
```

3. BEGIN和END是两个特殊的模式，BEGIN的作用是使后面的动作在处理所有记录前执行一次，END则是在处理完所有记录后执行一次，举个例子：
``` shell
$ cat ./awk_input.txt 
12 | 24 | 48
4  | 8  | 6
5  | 11 | 17
10 | 20 | 30

$ awk 'BEGIN { printf("这是BEGIN打印的\n"); } { printf("这是第%d行\n", NR); } END { printf("这是END打印的\n"); }' ./awk_input.txt 
这是BEGIN打印的
这是第1行
这是第2行
这是第3行
这是第4行
这是END打印的
```

### 动作

&emsp;&emsp;动作是由一些处理的指令，每个动作需要用大括号{}括起来，动作里也有选择和循环控制流，支持的控制流语句包括：
```
if (condition) statement [ else statement ]

while (condition) statement
do statement while (condition)

for (expr1; expr2; expr3) statement
for (var in array) statement

break
continue

delete array[index]
delete array

exit [ expression ]

{ statements }

switch (expression) {
	case value|regex : statement
	...
	[ default: statement ]
}
```

&emsp;&emsp;语法和C语言很相似，这里只介绍一下`if、else`和`for`语句，其他语句类比C语言，照着用就好了。

#### if语句

`if、else`语句语法：

```awk
if(条件)
{
	动作
}
else
{
	动作
}
```

`if、else`语句例子：

``` shell
$ cat ./awk_input.txt 
12  24  48
4   8   6
5   11  17
10  20  30

$ awk '{ if($2 > 15) { printf("第%d行第2个域大于15\n", NR); } else { printf("第%d行第2个域小于等于15\n", NR); } }' ./awk_input.txt
第1行第2个域大于15
第2行第2个域小于等于15
第3行第2个域小于等于15
第4行第2个域大于15
```

#### for语句

&emsp;&emsp;`for`语句有两种用法，一种用法和C语言相似，一种和shell里的for很相似。

`for`语句语法：

```
for(表达式1; 条件; 表达式2)
{
	动作
}

for(索引 in 数组)
{
	动作
}
```

`for`语句例子：
``` shell
$ cat ./awk_input.txt 
12  24  48
4   8   6
5   11  17
10  20  30

# 第一种for语句
$ awk '{ arr[NR] = $2; } END{ for(i = 1; i <= NR; i++) { printf("%s ", arr[i]); } }' ./awk_input.txt
24 8 11 20 

# 第二种for语句
$ awk '{ arr[NR] = $2; } END{ for(i in arr) { printf("%s ", arr[i]); } }' ./awk_input.txt
24 8 11 20 
```

&emsp;&emsp;上面的两个例子都是利用`for`语句打印所有记录第2个域的内容，需要注意的是，第二种`for`语句循环的是数组的索引，而不是值。

### 输出

&emsp;&emsp;awk可以用`printf`和`print`来输出，`printf`用法和C语言很像，`print`的用法和python2的很像。

``` shell
$ pwd | awk '{ printf("printf: %s\n", NR); print "print:", NR; }'
printf: 1  # printf的输出
print: 1   # print的输出
```