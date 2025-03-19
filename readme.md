```
E:\AIGC_design\word-passgame\
│   ├── main.py                 # 主程序入口，负责启动 Flask 应用和路由注册
│   ├── config.py               # 配置文件，定义路径和常量
│   ├── routes\                 # 路由模块目录，存放所有 API 和页面路由
│   │   ├── __init__.py         # 空文件，标记 routes 为包
│   │   ├── home.py             # 主页路由，返回 index.html
│   │   ├── words.py            # 单词管理路由（上传、获取单词）
│   │   ├── game.py             # 游戏逻辑路由（生成关卡、检查匹配）
│   │   └── scores.py           # 分数管理路由（保存、获取分数）
│   ├── utils\                  # 工具模块目录，存放辅助函数
│   │   ├── __init__.py         # 空文件，标记 utils 为包
│   │   ├── words_util.py       # 单词加载工具，处理 CSV 文件读取
│   │   └── game_util.py        # 游戏生成工具，生成卡片逻辑
│   ├── data\                   # 数据目录，存放单词库和分数记录
│   │   ├── default_words.csv   # 默认单词库文件
│   │   ├── game_words.csv      # 中转缓存文件，游戏使用的单词
│   │   ├── words1.csv          # 用户上传的单词库（示例，可有多个）
│   │   └── scores.json         # 分数记录文件
│   ├── static\                 # 静态文件目录，存放前端资源
│   │   ├── index.html          # 主页面，只包含基本结构和引入外部文件
│   │   ├── css\                # CSS 文件目录
│   │   │   └── styles.css      # 样式文件，定义页面布局和效果
│   │   ├── js\                 # JavaScript 文件目录
│   │   │   ├── main.js         # 主逻辑，初始化和页面切换
│   │   │   ├── game.js         # 游戏逻辑，处理关卡和交互
│   │   │   ├── scores.js       # 分数管理，处理排行榜
│   │   │   └── upload.js       # 上传逻辑，处理单词库上传
│   ├── .venv\                  # 虚拟环境目录
│   ├── .gitignore              # Git 忽略文件
│   ├── Dockerfile              # Docker 配置文件
│   ├── readme.md               # 项目说明文件
│   └── requirements.txt        # 依赖清单
```
# 单词消消乐游戏

一个通过消消乐游戏辅助记忆英语单词的项目，支持上传自定义单词表，未来计划集成 OCR 拍照识别。

## 功能
- **游戏模式**：65秒、125秒、180秒、无尽模式。
- **单词管理**：上传 CSV 或文本格式单词表。
- **分数记录**：保存最近 5 次游戏分数。
- **错词反馈**：游戏结束后显示错选单词。

## 安装

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd word-game


创建虚拟环境
bash

python -m venv .venv
.venv\Scripts\activate  # Windows

安装依赖
bash

pip install -r requirements.txt

运行
bash

python main.py

访问 http://127.0.0.1:5000。

项目结构
main.py：程序入口。

routes/：路由模块。

utils/：工具函数。

static/：前端文件。

data/：单词库和分数数据。

未来计划
添加 OCR 拍照识别单词。

优化 UI 和音效。

支持多语言。

贡献
欢迎提交 Issue 或 PR！

- **保存路径**：`E:\AIGC_design\word-game\readme.md`
- **说明**：
  - 用 Markdown 格式，便于 GitHub 或其他平台展示。
  - 根据你的需求（OCR 等）添加了未来计划。

---

### 5. `requirements.txt`（依赖清单）
- **作用**：列出项目所需 Python 包，方便安装。
- **内容**：

Flask==2.3.2
pandas==1.5.3

- **保存路径**：`E:\AIGC_design\word-passgame\requirements.txt`
- **说明**：
  - `Flask`：Web 框架。
  - `pandas`：处理 CSV 文件。
- **安装**：
  ```bash
  E:/AIGC_design/word-passgame/.venv/Scripts/pip install -r requirements.txt




目录树详细注释
根目录
E:\AIGC_design\word-game\
项目根目录，所有代码和数据文件存放于此。

main.py
作用：程序入口，初始化 Flask 应用，注册所有路由。

职责：保持简洁，仅负责启动和模块集成。

config.py
作用：集中管理配置，如路径、常量。

职责：定义全局变量（如 DATA_DIR），方便修改和复用。

路由模块目录
routes\
作用：存放所有路由逻辑，按功能拆分。

__init__.py
空文件，标记为 Python 包。

home.py
作用：处理主页路由，返回 index.html。

职责：静态文件服务。

words.py
作用：管理单词相关路由（如上传、获取）。

职责：处理 /upload_words 和 /words 接口。

game.py
作用：游戏核心路由。

职责：处理 /game/<level>、/next_group/<level>、/check。

scores.py
作用：分数管理路由。

职责：处理 /save_score 和 /get_scores。

工具模块目录
utils\
作用：存放通用工具函数。

__init__.py
空文件，标记为 Python 包。

words_util.py
作用：处理单词文件的加载和保存。

职责：从 CSV 读取单词，更新 game_words.csv。

game_util.py
作用：游戏卡片生成逻辑。

职责：封装 generate_game() 函数，供 game.py 调用。

数据目录
data\
作用：存放所有数据文件，无需改动。

default_words.csv
默认单词库，程序启动时若无用户词库则使用。

game_words.csv
游戏实际使用的单词中转文件。

words1.csv
用户上传的单词库，文件名递增。

scores.json
分数记录文件。

静态文件目录
static\
作用：存放前端文件，无需改动。

index.html
前端界面，包含游戏逻辑。

