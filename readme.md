# py4ss.net

## Ubuntu Server 安装微软雅黑

1. 安装微软字体
```bash
sudo apt update
sudo apt install ttf-mscorefonts-installer
```

2. 拷贝微软雅黑到字体目录
```bash
sudo cp msyh.ttf /usr/share/fonts/truetype/msttcorefonts/
```

检查安装

```bash
fc-list | grep "Microsoft YaHei"
```

3. 删除缓存
```bash
rm -rf ~/.cache/matplotlib
```

4. 如果还不行，编辑`matplotlibrc`

路径
```bash
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"
```

文件最后添加

```
font.family         : Microsoft YaHei
```



