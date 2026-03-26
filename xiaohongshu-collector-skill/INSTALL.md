# 小红书笔记收集器 - 安装指南

## 🚀 快速开始

### 前提条件
1. **Python 3.8+** 已安装
2. **Git** 已安装（用于克隆仓库）
3. **网络连接** 正常

### 安装步骤

#### 方法1：一键安装（推荐）
```bash
# 克隆仓库
git clone https://github.com/你的用户名/xiaohongshu-collector-skill.git
cd xiaohongshu-collector-skill

# 运行安装脚本
python install.py
```

#### 方法2：手动安装
```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/xiaohongshu-collector-skill.git
cd xiaohongshu-collector-skill

# 2. 安装Python依赖
pip install pyyaml python-docx

# 3. 安装小红书技能
python setup_dependencies.py

# 4. 初始化配置
python cli.py init

# 5. 测试运行
python cli.py run --once
```

## 📋 详细安装说明

### 1. 获取代码
```bash
# 从GitHub克隆
git clone https://github.com/你的用户名/xiaohongshu-collector-skill.git
cd xiaohongshu-collector-skill
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 安装小红书技能
本工具依赖小红书技能 (`xiaohongshu-skills`)。安装脚本会自动处理：
- 检查是否已安装
- 如果未安装，自动克隆并安装
- 配置环境变量

### 4. 配置工具
```bash
# 创建配置文件
python cli.py init

# 编辑配置文件（可选）
# 编辑 config.yaml 文件调整参数
```

### 5. 测试运行
```bash
# 显示当前配置
python cli.py config

# 运行一次测试
python cli.py run --once

# 设置定时任务
python cli.py schedule
```

## 🔧 依赖管理

### 必需依赖
- **pyyaml**: 配置文件解析
- **python-docx**: Word文档生成
- **xiaohongshu-skills**: 小红书数据采集

### 自动安装
安装脚本会自动：
1. 检查Python版本
2. 安装Python包依赖
3. 安装小红书技能
4. 创建必要的目录结构
5. 初始化配置文件

## 🐛 故障排除

### 常见问题

#### 1. Python版本问题
```
错误：Python版本过低
解决：请安装Python 3.8或更高版本
```

#### 2. 依赖安装失败
```
错误：pip install失败
解决：尝试使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. 小红书技能安装失败
```
错误：无法安装小红书技能
解决：手动安装
git clone https://github.com/openclaw/xiaohongshu-skills.git ~/.openclaw/workspace/skills/xiaohongshu-skills
```

#### 4. 配置文件问题
```
错误：配置文件不存在
解决：运行 python cli.py init 创建配置文件
```

#### 5. 权限问题
```
错误：无法写入文件
解决：检查输出目录权限，或使用管理员权限运行
```

### 获取帮助
```bash
# 查看帮助
python cli.py -h

# 查看配置
python cli.py config

# 测试环境
python verify.py
```

## 📁 项目结构
```
xiaohongshu-collector-skill/
├── cli.py              # 命令行接口
├── collector.py        # 核心收集逻辑
├── config.py           # 配置管理
├── __init__.py         # 主模块
├── config.yaml         # 配置文件
├── config_template.yaml # 配置模板
├── requirements.txt    # Python依赖
├── install.py          # 安装脚本
├── setup_dependencies.py # 依赖安装
├── verify.py           # 环境验证
├── README.md           # 使用说明
├── INSTALL.md          # 安装指南（本文件）
└── SKILL.md            # Skill规范
```

## 🔄 更新
```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖（如果需要）
python install.py --update
```

## 📞 支持
如有问题，请：
1. 查看日志文件：`~/xiaohongshu_collector.log`
2. 检查配置文件：`config.yaml`
3. 提交GitHub Issue
4. 查看详细文档：`README.md`

---

**注意**：使用本工具请遵守小红书的使用条款，仅用于个人学习和研究目的。