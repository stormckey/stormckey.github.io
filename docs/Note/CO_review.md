---
comments: true
---
# 计组笔记📒
!!! warning "极其简略，只有部分易忘、或不显然的知识点"

!!! danger "计租堂堂大课只有一页内容捏，猜猜是为什么😋"

!!! info "许多内容整理自[:octicons-link-16:咸鱼暄的代码空间](https://xuan-insr.github.io/computer_organization/1_prelude/)"

!!! tip "[:octicons-link-16:这里](https://bank.engzenon.com/tmp/60746e35-6aec-4163-86ed-7fdec0feb99b/626db954-7f2c-45af-9aa3-42dfc0feb99b/Computer_Organization_Manual_solution.pdf)是课本答案"

## Ch2 Instructions

- PC relative addressing: `PC + offset` 而非 `PC + 4 + offset`
- I 类型的立即数均为符号扩展，但要注意移位指令只截取低位，因为过多位数的位移无意义
- SB 和 UJ类型都不存最低位，因为他们的目的地是指令（word alignment），一般最后两位都是0（因为存在16位的指令所以只有最后一位必然是0）
- 合理利用`bgeu`来检测越界（小于零或者大于某个数）
- `lui`加载了立即数的高20位后，用`aadi`加载低12位，若因符号扩展导致进位，只要多加1000就可以抵消FFFFF000的影响
- 记清楚ld的d是doubleword，老是记成load的d

还有几张常用表：
![](images/CO_review/2023-03-31-17-29-23.png#pic)

![](images/CO_review/2023-03-31-17-29-33.png#pic)

![](images/CO_review/2023-03-31-17-29-45.png#pic)

（下图里的j imm要改成PC+imm）
![](images/CO_review/2023-03-31-17-30-14.png#pic)

![](images/CO_review/2023-03-31-18-04-03.png#pic)
## Ch3 Arithmetic

- 检测加减法溢出:最高位全加器的Cin Cout进行异或即可，这俩信号不一样，就意味着溢出了
- 最高位牵出一根线set到最低位的less，其他所有位less都置0就可以组成slt的输出信号了
- IEEE 754 注意两点 一是1+8+23 = 32 ｜1 + 11 + 52 = 64；二是下溢的非规格数的exponent跟规格数的最小exponent是一样的，这样设计就可以让 0.1111111...（下溢最大） -> 1.0000000（规格最小）...连续可以等差的往上增加
- 浮点加法：注意对齐改变的是小的指数那个
- 浮点乘法，注意减去bias

