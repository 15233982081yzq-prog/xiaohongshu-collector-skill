# 小红书笔记收集器 Skill

一个智能的小红书笔记收集工具，支持关键词搜索、内容筛选、定时收集和多种输出格式。

## ✨ 功能特性

- 🔍 **智能搜索**：根据关键词搜索小红书笔记
- 🎯 **内容筛选**：基于关键词过滤高质量内容
- ⏰ **定时收集**：支持cron表达式定时执行
- 📁 **多种格式**：支持JSON、Word文档输出
- ⚙️ **配置驱动**：所有参数通过配置文件管理
- 🚀 **一键运行**：简单的命令行接口

## 📦 安装依赖

```bash
# 安装Python依赖
pip install pyyaml python-docx

# 确保已安装小红书技能
# 小红书技能目录应位于: ~/.openclaw/workspace/skills/xiaohongshu-skills
```

## 🚀 快速开始

### 1. 创建配置文件

```bash
# 创建配置模板
python cli.py init

# 编辑配置文件
nano config.yaml
```

### 2. 运行一次测试

```bash
# 显示当前配置
python cli.py config

# 运行一次收集
python cli.py run --once
```

### 3. 设置定时任务

```bash
# 设置定时任务（根据config.yaml中的配置）
python cli.py schedule
```

## ⚙️ 配置文件说明

配置文件 `config.yaml` 包含以下主要部分：

### 基本配置 (`basic`)
```yaml
basic:
  search_keyword: "后端面试"      # 搜索关键词
  collect_count: 3               # 收集数量 (1-10)
  output_dir: "~/Desktop/面经收集" # 输出目录
  sort_by: "最新"                # 排序方式
  note_type: "不限"              # 笔记类型
  publish_time: "不限"           # 发布时间
```

### 筛选配置 (`filter`)
```yaml
filter:
  include_keywords:              # 必须包含的关键词
    - "面试"
    - "面经"
    - "后端"
  exclude_keywords:              # 排除的关键词
    - "招聘"
    - "广告"
    - "推广"
  min_content_length: 100        # 最小内容长度
  quality_threshold: 10          # 质量阈值
```

### 定时任务配置 (`schedule`)
```yaml
schedule:
  enabled: true                  # 是否启用定时任务
  cron_expression: "0 23 * * *"  # 每天23:00执行
  timezone: "Asia/Shanghai"      # 时区
```

### 高级配置 (`advanced`)
```yaml
advanced:
  request_delay: 2               # 请求延迟（秒）
  timeout: 30                    # 超时时间（秒）
  save_raw_json: true            # 保存原始JSON数据
  generate_word_doc: true        # 生成Word文档
```

## 📋 命令行使用

### 显示帮助
```bash
python cli.py -h
```

### 运行收集
```bash
# 运行一次收集（不设置定时任务）
python cli.py run --once

# 运行并设置定时任务
python cli.py run
```

### 管理配置
```bash
# 显示当前配置
python cli.py config

# 创建配置模板
python cli.py init

# 测试配置
python cli.py test
```

### 定时任务管理
```bash
# 设置定时任务
python cli.py schedule
```

## 🎯 使用示例

### 示例1：收集Java面试笔记
```yaml
# config.yaml
basic:
  search_keyword: "Java面试"
  collect_count: 5
  output_dir: "~/面试资料/Java"

filter:
  include_keywords:
    - "Java"
    - "面试"
    - "Spring"
    - "数据库"
  exclude_keywords:
    - "招聘"
    - "广告"
```

运行：
```bash
python cli.py run --once
```

### 示例2：每天自动收集
```yaml
# config.yaml
basic:
  search_keyword: "Python面试"
  collect_count: 3

schedule:
  enabled: true
  cron_expression: "0 9,18 * * *"  # 每天9:00和18:00执行
```

运行：
```bash
python cli.py schedule
```

### 示例3：自定义输出
```yaml
# config.yaml
basic:
  search_keyword: "算法面试"
  output_filename: "算法笔记_{date}.docx"

advanced:
  generate_word_doc: true
  generate_markdown: true
```

## 📁 输出文件

收集完成后，会在指定的输出目录生成以下文件：

```
输出目录/
├── 小红书笔记_后端面试_20240326.json      # 原始JSON数据
├── 小红书笔记_后端面试_20240326.docx      # Word文档
└── xiaohongshu_collector.log           # 日志文件
```

### Word文档内容
- 笔记标题
- 作者信息
- 发布时间
- 完整内容
- 点赞/收藏/评论数

## 🔧 故障排除

### 常见问题

1. **找不到小红书技能目录**
   ```
   错误：未找到小红书技能目录
   解决：确保 ~/.openclaw/workspace/skills/xiaohongshu-skills 目录存在
   ```

2. **配置文件不存在**
   ```
   错误：配置文件不存在
   解决：运行 python cli.py init 创建配置文件
   ```

3. **权限问题**
   ```
   错误：无法写入文件
   解决：检查输出目录的写入权限
   ```

4. **网络问题**
   ```
   错误：搜索失败
   解决：检查网络连接，确保可以访问小红书
   ```

### 查看日志
```bash
# 查看日志文件
tail -f ~/xiaohongshu_collector.log
```

## 📝 开发说明

### 项目结构
```
xiaohongshu-collector-skill/
├── __init__.py          # 主模块
├── cli.py              # 命令行接口
├── config.py           # 配置管理
├── collector.py        # 收集器核心逻辑
├── config.yaml         # 配置文件
├── config_template.yaml # 配置模板
└── README.md           # 说明文档
```

### 扩展功能
如需扩展功能，可以修改以下文件：
- `collector.py`：修改收集逻辑
- `config.py`：添加新的配置项
- `cli.py`：添加新的命令行参数

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请：
1. 查看日志文件：`~/xiaohongshu_collector.log`
2. 检查配置文件：`config.yaml`
3. 提交Issue