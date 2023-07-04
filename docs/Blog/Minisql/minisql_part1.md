---
commnets: true
---

# Minisql\#1 Disk and BufferPoolManager 

!!! abstract
    这一部分主要负责与内存磁盘空间申请释放等打交道，在项目中的地位大概相当于`new` `delete`，所以这一部分在后续会被频繁调用，也是直接与磁盘IO打交道的，实现既要求正确又要求效率

### 动机

假设我们手头上现在有65536（4096*16）页（一页为4096Bytes）的数据需要存在磁盘上，最自然的想法就是数组，实际上是变长数组，因为我们可以在文件尾继续写入新的页。

但是，数据库会对数据进行删除。假设我们分配出去第0-9页用于记录某个表，然后删除了其中第2，4，6页的数据，那么下次再请求页面来存储信息的时候，就可以用这空闲的三页来存储。不这样做，那么面对申请100页，删100页，申请100页，删100页这样的操作，本来只要100页的空间就可以实现，实际上却会花的多得多。

这就引出了BitMap，我们只要拿出一页来，把这一页4096个Byte，即32768个bit，每个bit的0指示该页未被使用，1指示已经被使用，这样这一页就可以管理其后的32768页了，我们每次都现在其中找0，没有0了，才去新开一页。

当然实际上这一页的4096B我们不会都拿去用来记录使用情况，还有一些元数据比如记录目前以占用的有10页等等。

但注意第一段假设我们有65536页要存，一页BitMap不够，那就多来几个。我们把1页BitMap和后面的（大概）32767页称为一段(extent)，我们需要两段来存储65536页，在最前面来个Disk Meta Page来管理所有页。