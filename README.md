# 中国石油大学（华东）自动评教

本项目基于 Selenium 实现，用于自动化完成教学评价任务。通过模拟用户操作，实现从登录教务系统到完成教学评价的全流程自动化。

---

## 功能特点

- 自动登录教务系统
- 自动导航到教学评价模块
- 自动完成教学评价，包括填写评分和建议
- 支持 Chrome 和 Edge 浏览器，兼容多版本驱动

---

## 环境依赖

### 必备条件

1. **Python 版本**：`>=3.8`
2. 依赖库：
   - `selenium`
   - `webdriver-manager`

### 安装依赖

运行以下命令，通过 `requirements.txt` 文件安装所需的 Python 库：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 下载项目代码

将项目代码克隆到本地：

```bash
git clone https://github.com/restrain11/auto_teachingEvaluate.git
cd auto_teachingEvaluate
```

### 2. 配置浏览器驱动

```python
# 配置 ChromeDriver 路径并启动浏览器
options = Options()#设置浏览器启动选项。

# 手动配置chromedriver路径
# chromedriver_path = r"C:\Users\restrain\.wdm\drivers\chromedriver\win64\131.0.6778.264\chromedriver-win32\chromedriver.exe"#指定ChromeDriver路径。
# service = Service(chromedriver_path) #加载ChromeDriver服务。

#如果不知道自己电脑的chromedriver的路径在哪，也可以用下面代码自动下载。
service = Service(ChromeDriverManager().install())  # 自动下载与当前 Chrome 版本匹配的驱动

#当然如果你想用edge也可以，类比上面的代码即可。
# service = Service(EdgeChromiumDriverManager().install())  # 自动下载与 Edge 版本匹配的驱动

driver = webdriver.Chrome(service=service, options=options)# 启动浏览器。
driver.implicitly_wait(20)#隐式等待，找不到元素时会等待20秒。
```

#### 自动下载驱动

项目默认支持自动下载适配的浏览器驱动，无需手动配置：

```python
service = Service(ChromeDriverManager().install())  # 自动下载与当前 Chrome 版本匹配的驱动
```

```python
service = Service(EdgeChromiumDriverManager().install())  # 自动下载与 Edge 版本匹配的驱动
```

#### 手动指定驱动路径

如需手动指定驱动路径，请修改以下代码：

```python
chromedriver_path = r"C:\Users\restrain\.wdm\drivers\chromedriver\win64\131.0.6778.264\chromedriver-win32\chromedriver.exe" #指定ChromeDriver路径。
service = Service(chromedriver_path) #加载ChromeDriver服务。
```

### 3. 修改账号信息

在代码中修改以下部分，填写你的登录账号和密码：

```python
username_input.send_keys("你的用户名")  # 替换为你的用户名
password_input.send_keys("你的密码")  # 替换为你的密码
```

### 4. 运行代码

运行主程序：

```python
python main.py
```

程序会自动完成以下操作：

1. 登录教务系统
2. 导航到教学评价页面
3. 自动完成所有教学评价

------

## 注意事项

1. **浏览器兼容性**：

   - 支持 Chrome 和 Edge 浏览器，默认使用 Chrome 浏览器。

   - 可通过修改代码轻松切换为 Edge 浏览器：

     ```
     from webdriver_manager.microsoft import EdgeChromiumDriverManager
     service = Service(EdgeChromiumDriverManager().install())
     driver = webdriver.Edge(service=service)
     ```
