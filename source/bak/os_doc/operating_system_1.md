---
title: '操作系统考研笔记(1)——计算机系统概述'
date: 2021-07-22
categories: 考研
tags: [操作系统, 考研, 计算机]
mathjax: true
---

# 操作系统的基本概念

## 操作系统的概念

&emsp;&emsp;**操作系统**：是一些程序集合，这些程序需要：
1. 控制和管理整个计算机系统的硬件与软件资源。
2. 合理地组织、调度计算机的工作与资源分配。
3. 为用户和其他软件提供方便接口与环境。


## 操作系统的特征

&emsp;&emsp;操作系统的4个基本特征：并发、共享、虚拟、异步。

### 并发

&emsp;&emsp;**并发**是指两个或多个事件在同一时间间隔内发生。
&emsp;&emsp;操作系统的并发性是指计算机系统中同时存在多个运行的程序，引入进程的目的是使程序能并发执行。

&emsp;&emsp;**并行**性是指系统具有同时进行运算或操作的特性，能在同一时刻完成两种或两种以上的工作。
&emsp;&emsp;并行性需要有相关硬件的支持，如多流水线或多处理机环境。

&emsp;&emsp;注意同一**时间间隔**（并发）和同一**时刻**（并行）的区别。
&emsp;&emsp;在多道程序环境下，一段时间内，宏观上有多道程序同时执行，而在每个时刻，单处理机环境下实际仅能有一道程序执行，因此微观上这些程序是分时交替执行的。操作系统的并发性是通过分时得以实现的。


### 共享

&emsp;&emsp;共享指的是系统中的资源可供内存中多个并发执行的进程共同使用。
&emsp;&emsp;共享的两种方式：
1. **互斥共享**：一段时间内只运行`一个进程`访问资源。互斥共享要求一种资源在一段时间内只能满足一个请求，只有当前请求完成后才能处理下一个请求。
2. **同时访问**：一段时间内由`多个进程`同时访问资源。同时访问共享允许一个请求分成几个时间片段间隔地完成，在时间片段间隔之间，资源可以被其他请求访问。同时访问共享在当前请求没有完成时，也能处理其他请求，并且其效果与连续完成的效果相同。

&emsp;&emsp;**临界资源**：一段时间内只允许一个进程访问的资源。

---

&emsp;&emsp;并发和共享是操作系统的两个最基本特征，两者之间互为存在的条件：
- 资源共享是以程序的并发为条件的，若系统不允许程序并发执行，则自然不存在资源共享问题。
- 若系统不能对资源共享实施有效的管理，则必将影响到程序的并发执行，甚至根本无法并发执行。

### 虚拟

&emsp;&emsp;虚拟是指把一个物理上的实体变为若工逻辑上的对应物。
&emsp;&emsp;用于实现虚拟的技术，称为虚拟技术。
&emsp;&emsp;操作系统中利用了多种虚拟技术来实现虚拟处理器、虚拟内存和虚拟外部设备等。

&emsp;&emsp;**虚拟处理器技术**：通过多道程序设计技术，采用让多道程序并发执行的方法，来分时使用同一处理器。 **虚拟处理器**：利用多道程序设计技术，把一个物理上的CPU虚拟为多个逻辑上的CPU。
&emsp;&emsp;**虚拟存储器技术**：将一台机器的物理存储器变为虚拟存储器，以便从逻辑上扩充存储器的容量。**虚拟存储器**：逻辑上的存储器。

&emsp;&emsp;操作系统的虚拟技术可归纳为：时分复用技术，如处理器的分时共享；空分复用技术，如虚拟存储器。

### 异步

&emsp;&emsp;**进程的异步**：多道程序允许多个程序并发执行，但由于资源有限，进程的执行并不是一贯到底的，而是走走停停的，以不可预知的速度向前推进。


## 操作系统的目标和功能

### 操作系统作为计算机系统资源的管理者

&emsp;&emsp;**处理机管理**：对进程的管理。进程管理的最主要任务：进程何时创建、何时撤销、如何管理、如何避免冲突、如何共享。进程管理的主要功能：进程控制、进程同步、进程通信、死锁处理、处理机调度等。

&emsp;&emsp;**存储器管理**：主要包括内存分配与回收、地址映射、内存保护与共享和内存扩充等功能。

&emsp;&emsp;**文件管理**：操作系统中负责文件管理的部分称为文件系统。文件管理包括文件存储空间的管理、目录管理、文件读写管理和保护等。

&emsp;&emsp;**设备管理**：主要任务是完成用户的IO（输入输出）请求，方便用户使用各种设备，并提高设备的利用率。主要包括缓冲管理、设备分配、设备处理和虚拟设备等功能。

### 操作系统作为用户与计算机硬件系统之间的接口

&emsp;&emsp;操作系统提供的接口主要分为两类：命令接口、程序接口。

**命令接口**：主要方式有两种：
- **联机命令接口**：又称交互式命令接口，由一组键盘操作命令组成。用户通过终端输入操作命令，向系统提出各种服务要求。
- **脱机命令接口**：又称批处理命令接口，由一组控制命令组成。用户事先用相应的作业控制命令写成一份作业操作说明书，连同作业一起提交给系统，系统调度到改作业时，由系统中的命令解释程序逐条解释执行作业说明书上的命令。

**程序接口**：由一组系统调用（也称广义指令）组成。用户通过在程序中使用这些系统调用来请求操作系统为其提供服务。库函数是高级语言中提供的与系统调用对应的函数，但是库函数属于用户程序而非系统调用，是系统调用的上层。


### 操作系统用作扩充机器

&emsp;&emsp;**裸机**：没有任何软件支持的计算机。通常把覆盖了软件的机器称为**扩充机器**或**虚拟机**。

---

&emsp;&emsp;操作系统课程所关注的内容是操作系统如何控制和协调处理机、存储器、设备和文件，而不关注接口和扩充机器。



# 操作系统的发展和分类

## 手工操作阶段

&emsp;&emsp;此阶段无操作系统，用户在计算机上的工作都要人工干预。
&emsp;&emsp;缺点：资源利用率低，CPU等待手工操作，CPU利用不充分。

## 批处理阶段

### 单道批处理阶段

特征：

1. 单道性：内存中仅有一道程序运行。
2. 顺序性：磁带上的各道作业顺序地进入内存，先调入内存的作业先完成。
3. 自动性：磁带上的一批作业能自动地逐个运行。

缺点：每次主机内存中仅能存放一道作业，当主机在运行期间发出输入/输出请求后，高速的CPU便处于等待低速的IO完成的状态。

### 多道批处理系统

&emsp;&emsp;多道程序设计技术允许多个程序同时进入内存，并允许它们在CPU中交替地运行，这些程序共享系统中的各种硬/软件资源。特点是多道、宏观上并行、微观上串行。

1. 多道：内存中同时存放多道相互独立的程序。
2. 宏观上并行：内存中的多道程序都处于运行过程中。
3. 微观上串行：内存中的多道程序轮流占用CPU，交替执行。

需要解决的问题：

1. 如何分配处理器。
2. 多道程序的内存分配问题。
3. IO设备分配问题。
4. 如何组织和存放大量的程序和数据，以方便用户使用并保证其安全性与一致性。

&emsp;&emsp;多道批处理系统把用户提交的作业成批地送入计算机内存，然后由作业调度程序自动地选择作业运行。

&emsp;&emsp;优点：资源利用率高，系统吞吐量大。
&emsp;&emsp;缺点：用户响应时间较长，不提供人机交互能力。

## 分时操作系统

&emsp;&emsp;**分时技术**：把处理器的运行时间分成很短的时间片，按时间片轮流把处理器分配给各联机作业使用。
&emsp;&emsp;**分时操作系统**：多个用户通过终端同时共享一台主机，这些终端连接在主机上，用户可以同时与主机进行交互操作而互不干扰。

分时操作系统的特征：

1. **同时性**：也称多路性，指运行多个终端用户同时或基本同时使用同一台计算机。
2. **交互性**：用户能通过中端，采用人机对话的方式直接控制程序的运行，与程序进行交互。
3. **独立性**：系统中的多个用户可以彼此独立地进行操作，互不干扰。
4. **及时性**：用户请求能在很短时间内获得响应。

## 实时操作系统

&emsp;&emsp;**实时操作系统**：能在某个时间限制内完成某些紧急任务而不需要时间片等待。

- **硬实时操作系统**：某个动作必须绝对地在规定的时刻（或规定的时间范围）发生。
- **软实时操作系统**：能够接受偶尔违反时间规定且不会引起任何永久性的损害。

## 网络操作系统

&emsp;&emsp;把计算机网络中的各台计算机有机地结合起来，提供一种统一、经济而有效的使用各台计算机的方法，实现各台计算机之间数据的互相传送。

## 分布式计算机系统

&emsp;&emsp;分布式计算机系统是由多台计算机组成并满足下列条件的系统：

1. 系统中任意两台计算机通过通信方式交互信息；
2. 系统中的每台计算机都具有同等的地位，既没有主机也没有从机；
3. 每台计算机上的资源为所有用户共享；
4. 系统中的任意台计算机都可以构成一个子系统，并且还能重构；
5. 任何工作都可以分布在机台计算机上，由它们并行工作、协同完成。

&emsp;&emsp;用于管理分布式计算机的操作系统称为**分布式计算机系统**。该系统的主要特点是：分布性和并行性。分布式操作系统与网络操作系统的本质不同是，分布式操作系统中的若干计算机相互协同完成同一任务。

## 个人计算机操作系统

&emsp;&emsp;个人计算机系统是目前使用最广泛的操作系统，常见的有Windows、Linux和Macintosh等。

---

操作系统的发展历程：

![](/images/learn_note/operating_system_1/fig_1.png)


# 操作系统的运行环境

## 操作系统的运行机制

&emsp;&emsp;通常CPU执行两种不同性质的程序：一种是操作系统内核程序；另一种是用户自编的程序（系统外层的应用程序）。系统内核程序是应用程序的管理者，可以执行一些特权指令，比如IO指令、置中断指令、存取用于内存保护的寄存器、送程序状态字到程序状态字寄存器等，特权指令不允许用户直接使用。CPU的状态可以分为用户态（目态）和核心态（又称管态、内核态），CPU只能在核心态时运行特权指令，用户自编程序运行在用户态，操作系统内核程序运行在核心态。

&emsp;&emsp;操作系统的各项功能分别被设置在不同的层次上。一些与硬件关联较紧密的模块，如时钟管理、中断处理、设备驱动等处于最底层。其次是运行频率较高的程序，如进程管理、存储器管理和设备管理等。这两部分内容构成了操作系统的内核，工作在核心态。
&emsp;&emsp;内核是计算机上配置的底层软件，大部分操作系统内核包括4方面的内容。

### 时钟管理

&emsp;&emsp;在计算机各部件中，时钟是最关键的设备。操作系统需要通过时钟管理，向用户提供标准的系统时间，通过时钟中断的管理，可以实现进程的切换。

### 中断机制

&emsp;&emsp;中断是操作系统各项操作的基础，在中断机制中，只有一小部分功能属于内核，它们负责保护和恢复中断现场的信息，转移控制权到相关的处理程序。

### 原语

特点：

1. 处于操作系统的最底层，是最接近硬件的部分。
2. 这些程序的运行具有原子性，其操作只能一气呵成。
3. 这些程序的运行时间都较短，而且调用频繁。

&emsp;&emsp;通常把具有这些特点的程序称为**原语**。定义原语的直接方法是关闭中断，让其所有动作不可分割地完成后再打开中断。

### 系统控制的数据结构及处理

系统的一些基本操作：

1. 进程管理：进程状态管理、进程调度和分派、创建与撤销进程控制块等。
2. 存储器管理：存储器的空间分配和回收、内存信息保护程序、代码对换程序等。
3. 设备管理：缓冲区管理、设备分配和回收等。


## 中断和异常的概念

### 中断和异常的定义

&emsp;&emsp;**中断**：也称外中断，指来自CPU执行指令以外的事件的发生，如设备发出的IO结束中断，时钟中断。

&emsp;&emsp;**异常**：也称内中断、例外或陷入，指源自CPU执行指令内部的事件，如程序的非法操作码、地址越界、算术溢出等引起的事件。

### 中断处理的过程

1. **关中断**。CPU响应中断后，首先要保护程序的现场状态，在保护现场的过程中，CPU不应该响应更高级中断源的请求。否则，若现场保存不完整，在中断服务程序结束后，也就不能正确地恢复并继续执行现场程序。
2. **保存断点**。为保证中断服务程序执行完毕后能正确地返回到原来的程序，必须将原来的程序断点（即程序计数器PC指针）保存起来。
3. **引出中断服务程序**。其实质是取出中断服务程序的入口地址送入程序计数器PC中。
4. **保存现场和屏蔽字**。进入中断服务程序后，首先要保存现场，现场信息一般是指程序状态字寄存器PSWR和某些通用寄存器的内容。
5. **开中断**。允许更高级中断请求得到响应。
6. **执行中断服务程序**。字面意思，执行中断服务程序。
7. **关中断**。保证在恢复现场和屏蔽字时不被中断。
8. **开中断、中断返回**。中断服务程序的最后一条指令通常是一条中断返回指令，使其返回到原程序的断点处，以便继续执行原程序。

&emsp;&emsp;1～3步是在CPU进入中断周期后，由硬件自动（中断隐指令）完成的，4～9步由中断服务程序完成。

## 系统调用

&emsp;&emsp;系统调用是指用户在程序中调用操作系统所提供的一些子功能，系统调用可视为特殊的公共子程序。系统中的各种共享资源都由操作系统统一掌管，因此在用户程序中，凡是与资源有关的操作（如存储分配、进行IO传输及管理文件等），都必须通过系统调用方式向操作系统提出服务请求，并由操作系统代为完成。
&emsp;&emsp;系统调用的功能大致可分为如小几类：

- **设备管理**。完成设备的请求和释放，以及设备启动等功能。
- **文件管理**。完成文件的读、写、创建及删除等功能。
- **进程控制**。完成进程的创建、撤销、阻塞及唤醒等功能。
- **进程通信**。完成进程之间的消息传递或信号传递等功能。
- **内存管理**。完成内存的分配、回收以及获取作业占用内存区大小及起始地址等功能。

![系统调用执行过程](/images/learn_note/operating_system_1/fig_2.png)

&emsp;&emsp;用户程序可以执行陷入指令（又称访管指令或trap指令）来发起系统调用，请求操作系统提供服务。


# 操作系统的体系结构

## 大内核和微内核

&emsp;&emsp;**大内核**：操作系统的主要功能模块都作为一个紧密联系的整体运行在核心态，从而为应用提供高性能的系统服务。优点：性能高。缺点：大型操作系统设计比较复杂，内核代码难以维护。

&emsp;&emsp;**微内核**：将内核中最基本的功能保留在内核，将不需要在核心态执行的功能移到用户态执行，从而降低内核的设计复杂性。优点：有效地分离了内核与服务、服务与服务，使得它们之间的接口更加清晰，维护的成本大大降低。缺点：需要频繁地在核心态和用户态之间进行切换，操作系统的开销偏大。


# 疑难点

## 并性与并发的区别和联系

&emsp;&emsp;并行性，指两个或多个事件在同一时刻发生。并发性，指两个或多个事件在同一时间间隔内发生。
&emsp;&emsp;在多道程序环境下，并发性是指在一段时间内，宏观上有多个程序同时运行，但在单处理器系统中每个时刻却仅能有一道程序执行，因此微观上这些程序只能分时地交替执行。

## 特权指令和非特权指令

&emsp;&emsp;特权指令，值有特殊权限的指令。由于这类指令的权限最大，使用不当将导致整个系统崩溃，如清内存、置时钟、分配系统资源、修改虚拟内存的段表和页表、修改用户的访问权限等。为保证系统安全，这类指令只能用于操作系统或其他系统软件，不直接提供给用户使用。特权指令必须在核心态执行。
&emsp;&emsp;用户态下也能执行的指令叫非特权指令，在用户态下使用特权指令时，将产生中断以阻止用户使用特权指令。从用户态转换为核心态的唯一途径是中断或异常。

## 访管指令和访管中断

&emsp;&emsp;访管指令是一条可以在用户态下执行的指令。在用户程序中，因要求操作系统提供服务而有意识地使用访管指令，从而产生一个中断事件（自愿中断），将操作系统转换为核心态，称为访管中断。

