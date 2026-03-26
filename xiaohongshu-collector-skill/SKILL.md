# SKILL.md - 小红书笔记收集器

## 概述

一个智能的小红书笔记收集工具，支持关键词搜索、内容筛选、定时收集和多种输出格式。专为需要定期收集特定领域（如面试经验、学习资料）小红书笔记的用户设计。

## 功能特性

- 🔍 **智能搜索**：根据关键词搜索小红书笔记
- 🎯 **内容筛选**：基于关键词过滤高质量内容
- ⏰ **定时收集**：支持cron表达式定时执行
- 📁 **多种格式**：支持JSON、Word文档输出
- ⚙️ **配置驱动**：所有参数通过配置文件管理
- 🚀 **一键运行**：简单的命令行接口

## 使用场景

1. **面试准备**：定期收集后端、前端、算法等面试经验
2. **学习资料**：收集特定技术领域的学习笔记
3. **竞品分析**：收集竞品相关的用户反馈和评测
4. **内容监控**：监控特定话题的最新讨论

## 安装要求

### 前置条件
- Python 3.8+
- 已安装小红书技能 (`xiaohongshu-skills`)
- 网络连接（可访问小红书）

### Python依赖
```bash
pip install pyyaml python-docx
```

## 快速开始

### 1. 初始化配置
```bash
python cli.py init
```

### 2. 编辑配置文件
编辑生成的 `config.yaml` 文件，设置搜索关键词、筛选条件等。

### 3. 运行测试
```bash
python cli.py run --once
```

### 4. 设置定时任务
```bash
python cli.py schedule
```

## 配置文件说明

### 主要配置项

#### 基本配置
```yaml
basic:
  search_keyword: "后端面试"      # 搜索关键词
  collect_count: 3               # 收集数量
  output_dir: "~/Desktop/面经收集" # 输出目录
  sort_by: "最新"                # 排序方式
```

#### 筛选配置
```yaml
filter:
  include_keywords:              # 必须包含的关键词
    - "面试"
    - "面经"
  exclude_keywords:              # 排除的关键词
    - "招聘"
    - "广告"
  min_content_length: 100        # 最小内容长度
```

#### 定时任务
```yaml
schedule:
  enabled: true                  # 是否启用
  cron_expression: "0 23 * * *"  # 每天23:00执行
  timezone: "Asia/Shanghai"      # 时区
```

## 命令行接口

### 主要命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `run` | 运行收集 | `python cli.py run --once` |
| `schedule` | 设置定时任务 | `python cli.py schedule` |
| `config` | 显示配置 | `python cli.py config` |
| `init` | 创建配置模板 | `python cli.py init` |
| `test` | 测试配置 | `python cli.py test` |

### 常用示例

#### 收集Java面试笔记
```bash
# 编辑config.yaml
basic:
  search_keyword: "Java面试"
  collect_count: 5

# 运行
python cli.py run --once
```

#### 每天自动收集Python资料
```bash
# 编辑config.yaml
basic:
  search_keyword: "Python学习"
schedule:
  enabled: true
  cron_expression: "0 9 * * *"  # 每天9:00

# 设置定时任务
python cli.py schedule
```

## 输出文件

### 生成的文件
```
输出目录/
├── 小红书笔记_关键词_日期.json      # 原始数据
├── 小红书笔记_关键词_日期.docx      # Word文档
└── xiaohongshu_collector.log     # 日志文件
```

### Word文档内容
- 笔记标题和作者
- 发布时间和互动数据
- 完整内容
- 筛选统计信息

## 故障排除

### 常见问题

1. **找不到小红书技能**
   - 确保 `~/.openclaw/workspace/skills/xiaohongshu-skills` 目录存在
   - 确认小红书技能已正确安装

2. **配置文件错误**
   - 使用 `python cli.py test` 测试配置
   - 检查YAML格式是否正确

3. **网络问题**
   - 检查网络连接
   - 查看日志文件中的错误信息

4. **权限问题**
   - 确保有写入输出目录的权限
   - 检查日志文件路径是否可写

### 查看日志
```bash
# 查看实时日志
tail -f ~/xiaohongshu_collector.log
```

## 高级配置

### 自定义筛选逻辑
在 `collector.py` 中可以修改 `_filter_note` 方法来自定义筛选逻辑。

### 扩展输出格式
支持添加新的输出格式（如Markdown、PDF），在 `collector.py` 的 `_save_results` 方法中添加。

### 性能优化
- 调整 `request_delay` 避免请求过快
- 设置合适的 `timeout` 值
- 使用 `max_retries` 处理失败请求

## 安全注意事项

1. **配置文件安全**
   - 不要将包含敏感信息的配置文件提交到版本控制
   - 使用环境变量或密钥管理工具存储敏感信息

2. **数据使用**
   - 遵守小红书的使用条款
   - 仅用于个人学习和研究目的
   - 不要大规模爬取数据

3. **资源限制**
   - 合理设置收集频率
   - 避免对小红书服务器造成过大压力

## 更新日志

### v1.0.0 (2026-03-26)
- 初始版本发布
- 支持关键词搜索和内容筛选
- 支持定时任务和多种输出格式
- 提供完整的命令行接口

## 支持与反馈

如有问题或建议，请：
1. 查看日志文件获取详细信息
2. 检查配置文件是否正确
3. 提交Issue或联系开发者

## 许可证

MIT License - 详见 LICENSE 文件