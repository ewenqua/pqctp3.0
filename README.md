# pqctp3.0
=====
python quant of CTP

QQ交流群：273182530

用法
=====
环境：Windows 10 64位，或Linux 64位，python 3.7-3.8.5
依赖的库文件需要单独下载编译，见参考来源。

运行：pqctp目录下，cmd
执行 python SyncDayBar.py  #下载补全日K线
完成后，
执行 python main.py

新功能：
2.0适配穿透式API, 兼容郑商所合约, 解决RtnOrder bug。
3.0采用日线新接口。简化ctpwrapper的使用。

Windows环境变量
PYTHONPATH D:\Python-3.8.5\Lib

db3修改查看
1, Win 10建议使用SQLite Expert Personal
2, Ubuntu建议SQLite Browser
安装：sudo apt-get install sqlitebrowser

参考来源
=====
https://github.com/nooperpudd/ctpwrapper
-----
pip install cython --upgrade
pip install ctpwrapper --upgrade
自动安装 cython ctpwrapper 到Lib\site-packages目录。
ctpwrapper会自动编译生成。

注意
=====
http://www.simnow.com.cn
可以快速申请仿真帐号，跑起来。程序里自带帐号被修改过，不共享


