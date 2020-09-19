从零开始 WSL
================

.. important::
   
   本章基于 WSL 2，不过在 WSL 1 中的表现应当相近。

在阅读本章节前，请浏览下列 bash 指令检测您是否了解它们的基础用法：

* `cd`: 切换目录。特别地，用 `..` 表示上级目录。
* `grep`: 文本搜索，支持通配符模式。
* `ls`: 列出目录下的所有文件夹。常用参数 `-h` 与 `-l`。
  
  * `ll` 是 `ls -l --color=auto` 的别名

熟悉初始环境
---------------

认识主目录
^^^^^^^^^^^^^^

安装完 WSL 后，进入了用户主目录 `~` 。我的用户名是 `wklchris` ，因此主目录实质上是 `/home/wklchris` ：

.. code-block:: sh
   
   wklchris@PC:~$ cd ..
   wklchris@PC:/home$ ls
   wklchris

可以看到，目录非常干净。现在我们切换回用户主目录吧：

.. code-block:: sh
   
   wklchris@PC:/home$ cd ~
   wklchris@MSI-W:~$


更新系统
^^^^^^^^^^^^^^^

使用 `apt-get` 来检查更新：

.. code-block:: sh
   
   $ sudo apt-get update
   $ sudo apt-get upgrade


创建软链接
^^^^^^^^^^^^^^^

Ubuntu 会随系统安装 Python；如果你满意该 Python 的版本，那么可以直接在其下安装 pip 工具：

.. code-block:: sh
   
   $ sudo apt-get install python3-pip

但随即，你会发现命令行中只有 `python3` 命令，没有 `python` 命令；只有 `pip3` 命令，没有 `pip` 命令。

如果你不准备安装其他版本的 Python 与 pip，那么你可以到 `/usr/bin` 目录中创建符号链接来“添加”这些命令。先查询一下已存在的与 `python` 相关的命令：
   
.. code-block:: sh
   
   $ cd /usr/bin
   $ ls | grep python
   python3
   python3-config
   python3.8
   python3.8-config
   x86_64-linux-gnu-python3-config
   x86_64-linux-gnu-python3.8-config

可以看到，只有 `python3` 与 `python3.8` 命令，并没有 `python` 。如果添加 `-l` 参数，可以发现 `python3` 实质是一个指向 `python3.8` 的软连接：

.. code-block:: sh
   
   $ ls -l | grep python   # 或者 ll | grep python
   
现在我们来创建一个新的符号链接吧，让 `python` 指向 `python3` 或者 `python3.8` ：

.. code-block:: sh
   
   $ sudo ln -s python3 python
   $ ll | grep python
   ...
   lrwxrwxrwx  1 root   root           7 Sep  1 03:39 python -> python3*
   ...
   
看到类似的一行就表示创建成功了。我们可以用 `which python` 来查询现在的 `python` 调用的是哪个：

.. code-block:: sh
   
   $ which python
   /usr/bin/python

同理，我们也可以将 `pip` 作为软链接添加：

.. code-block:: sh
   
   # cd /usr/bin
   $ sudo ln -s pip3 pip
   

配置图形界面
-----------------

许多用户不习惯只用命令行来操作 Ubuntu，我们也可以让它输出图形界面 [#bib-gui]_ 。

1. 在主机（Windows 10）上安装 X-server 服务器（比如 `VcXsrv <https://sourceforge.net/projects/vcxsrv/>`_）
2. 在 WSL 中安装 X 桌面，比如 Xfce：

   .. code-block:: sh

      $ sudo apt-get install xfce4 xfce4-terminal
   
   安装包的体积不小，请做好准备。在安装中会让你选择一个显示管理软件（display manager），用键盘选择一个即可，例如 `dgm3` 。
3. 将显示的地址配置好，具体是将以下两行写入到 `~/.bashrc` 文件中，该文件中的行在每次启动 WSL 的终端时都会被执行：
   
   .. code-block:: sh

      $ nano ~/.bashrc
      ...
      # 进入编辑器
      export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
      export LIBGL_ALWAYS_INDIRECT=1
      # 按 Ctrl S 保存，再按 Ctrl X 以退出
      ...
      # 重新加载 bashrc 文件
      $ source ~/.bashrc

4. 回到 Windows 主机，打开 VcXsrv 中的 Xlaunch 软件。
   
   1. 在 Select display settings 中，选择 One Window without titlebar，在 Display number 填 0，点击下一步；
   2. 在 Select how to start clients 中，选择 Start no client，点击下一步；
   3. 在 Extra settings 中，补充勾选 Disable access control，点击下一步。

5. 这时 Xlaunch 会打开一个窗口，由于没有图像输入，窗口内容是全黑。这时候我们返回 WSL，启动 Xfce 即可：
   
   .. code-block:: sh
   
      $ startxfce4

6. 要退出图形界面，关闭 Xlaunch，然后在 WSL 中按 `Ctrl + C` 打断命令即可。


.. rubric:: 注释

.. [#bib-gui] 本节关于 Xfce-VcXSrv 的用法参考了： `How to set up working X11 forwarding on WSL2 <https://stackoverflow.com/a/61110604/6663890>`_ 这篇回答。