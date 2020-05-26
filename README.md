# AirConditioningManagementSystem(分布式温控系统)

## 前言

某快捷廉价酒店响应节能绿色环保理念，推行自助计费式中央温控系统，使得入住的客户可以根据要求设定温度和风速的调节，同时可以显示所需支付的金额。客户退房时酒店须出具空调使用的账单及详单。空调运行期间，空调管理员能够监控各房间空调的使用状态，需要的情况下可以生成格式统计报表。



---

## start

`git clone git@github.com:SimonGH0oSTRiley/AirConditioningManagementSystem.git`

---

### 关于如何使用`plantuml-markdown`插件

由于这个插件是基于`python`的，那么你需要安装`python`，这个步骤请自行解决，记得配置环境路径哦喵~。

其次，当你安装好`python`后，可以在shell里使用如下命令安装

```bash
pip install plantuml-markdown
```

或者对于软饭来说，可以利用`Chocolatey`依赖管理工具安装，那么首先需要安装它。请在拥有管理员权限的PowerShell中用如下命令安装`Chocolatey`

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

如果你不知道如何开启管理员权限的Power Shell或者你想康康你是不是有权限，请在PowerShell中运行 `Get-ExecutionPolicy` 。如果返回的是 `Restricted`，那么就运行`Set-ExecutionPolicy AllSigned` 或者 `Set-ExecutionPolicy Bypass -Scope Process`看你心情就好了。如果不是 `Restricted`，那么恭喜你NM$L。

还有很多其他步骤，请参考相关页面哦

[planetuml-markdown on Github](https://github.com/mikitex70/plantuml-markdown)

[planetuml-markdown on pypi](https://pypi.org/project/plantuml-markdown/)

[How to install Chocolatey on chocolatey.org](https://chocolatey.org/install)

