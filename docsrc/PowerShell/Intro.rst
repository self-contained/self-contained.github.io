Powershell 简介
===================

Powershell（脚本 `.ps1` ）在 Windows 10 时代已经基本取代了原来 CMD 命令行（脚本 `.cmd/.bat` ），成为了 Windows 系统新的默认命令行。

.. warning:: 检查 Powershell 版本

   Win 10 自带的 Powershell 可能低于本文档使用的版本（7.0)，请使用以下命令检查当前的版本（如下例中，版本是7.1.2）：

   .. code-block:: powershell
      
      $PSVersionTable.PSVersion
   
   .. code-block::

      Major  Minor  Patch  PreReleaseLabel BuildLabel
      -----  -----  -----  --------------- ----------
      7      1      2  
   
   * 如果版本低于 7.0，可以参考 `在 Windows 上安装 PowerShell <https://docs.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-core-on-windows>`_ 安装（但并不替代旧的）新的 Powershell 版本。

一些 Powershell 的语法特性：

* 不区分大小写，比如 `Get-Help` 与 `get-help` 。
* 用美元符设置变量或引用变量，比如 `$foobar`。


执行策略：ExecutionPolicy
-----------------------------

Powershell 默认的执行策略是受限（Restricted），即限制所有的 `.ps1` 脚本运行。所有可配置的执行策略包括：

.. table:: Powershell 执行策略
    :align: center
    
    =========       ================
    策略名           解释     
    ---------       ----------------
    AllSigned       全签名，只运行签名脚本
    Bypass          免验证，且无提示
    Restricted      受限制，阻止所有脚本
    RemoteSigned    远程脚本必须签名
    Unrestricted    所有脚本不受限
    Undefined       不配置
    =========       ================

关于什么是脚本签名，可以参考 `关于签名 <https://docs.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_signing>`_ 。


策略作用域包括：

.. table:: Powershell 执行策略
    :align: center
    
    ===============    ================
    策略作用域           解释     
    ---------------    ----------------
    MachinePolicy      计算机上所有用户组
    UserPolicy         当前用户所在用户组
    Process            当前Powershell会话
    CurrentUser        当前用户
    LocalMachine       计算机上任意用户
    ===============    ================   

一般地，我推荐将本机（LocalMachine）或当前用户（CurrentUser）的执行策略设置为 `RemoteSigned` ：

.. code-block:: powershell

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

可以通过 `Get-ExecutionPolicy` 命令（以及 `-List` 参数），查看执行策略：

.. code-block:: powershell
   
   Get-ExecutionPolicy -List


帮助命令：help
-----------------

使用 `Get-Help` 命令查询帮助，例如查询 `Get-ExecutionPolicy` 的用法：

.. code-block:: powershell
   
   Get-Help Get-ExecutionPolicy

它也支持通配符：

.. code-block:: powershell
   
   Get-Help *ExecutionPolicy


管道语法
-------------

管道语法使用 `|` 管道符，允许将管道左侧的输出作为输入，传递给管道右侧的命令。

