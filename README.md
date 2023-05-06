PyAxeTool
=========

An utility tool collection for make life easily.

Examples
--------
```
# 显示单个文件的MD5
python3 -m PyAxeTool.MD5 file test.txt

# 显示所有满足通配符文件的MD5
python3 -m PyAxeTool.MD5 file "*.txt"

# 显示目录内所有文件汇总的单个MD5
python3 -m PyAxeTool.MD5 dir testdir

# 显示字符串的MD5
python3 -m PyAxeTool.MD5 str abc
```