Git 简介
=============


版本控制
-------------

版本控制（Version Control System, VCS）记录了文件的变化，便于查阅或恢复到某个时刻的文件状态。

版本控制系统主要有三种：

* **本地版本控制（Local Version Control System）**：
  
  所有修订版本的信息都存储在本地。磁盘损坏可能损坏记录。

* **中心式版本控制（Centralized Version Control System, CVCS）**：

  所有修订版本的信息都存储在中心服务器上，协同工作的用户们通过客户端连接服务器，以此取出文件或提交更新。优点是便于管理员管理，缺点是中心服务器宕机会导致无法进行任何工作。

* **分布式版本控制（Distributed Version Control System, DVCS）**：  

  客户端取出文件时，会克隆整个仓库。任一协同服务器的故障都可以从克隆仓库中恢复。

Git 属于分布式版本控制系统。


Git 简史
-------------

2005 年，分布式版本控制系统 BitKeeper 所在公司与 Linux 内核开源社区合作结束；后者无法继续使用 BitKeeper 进行版本控制。因此 Linux 开源社区开发了自己的版本系统，称为 Git。Git 仍遵循着其设计初衷：

* 速度
* 简洁的设计
* 支持数量众多的并行开发分支
* 完全分布式
* 能够高效管理具有 Linux 或更大规模的大型项目

基本的 Git 工作特点：

* Git 记录每个版本的快照，而不是相对上个版本的变更。这使得 Git 与其他大部分版本控制系统都不相同。
* Git 使用 SHA-1 散列建立内部的索引，显示为 40 位 16 进制字符。
* Git 很少执行删除指令，因此信息误丢失的可能极小。


.. _git-status:

Git 仓库、工作目录与暂存区
-------------------------------

Git 仓库是保存对象数据库的地方。工作目录是从仓库中提取的某版本的文件内容，可能包含你的修改。暂存区保存了你下次要提交到仓库的内容。

在 Git 中托管的文件有三种状态：

* **已提交（commited）**：文件更改已记录到仓库中；如果所有文件均已被提交，那么工作目录状态从 Staged 变为 Unmodified。
* **已修改（modified）**：文件被修改了（与最后一次提交的文件不同），但修改尚未记录；如果任何文件已被修改，那么工作目录状态从 Unmodified 变为 Modified。
* **已暂存（staged）**：文件已被修改且被标记，将在下一次提交中记录到仓库；如果所有文件均已暂存，那么工作目录状态从 Untracked 与Unmodified 变为 Staged。 

.. figure:: pics/git-status-cycle.png
   :width: 80%
   :align: center
   
   Git 文件的状态变化周期（图源： `官方 Git 手册（第二版） <https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E8%AE%B0%E5%BD%95%E6%AF%8F%E6%AC%A1%E6%9B%B4%E6%96%B0%E5%88%B0%E4%BB%93%E5%BA%93>`_ 第 2.2 节）

git 中的 HEAD 指针总是指向当前位置（最后一次提交），除非人为地移动它。
