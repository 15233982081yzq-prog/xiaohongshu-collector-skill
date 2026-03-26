#!/usr/bin/env python3
"""
小红书笔记收集器 - 最终验证脚本
验证核心功能是否可用
"""

import os
import sys
from pathlib import Path

print("="*60)
print("小红书笔记收集器 - 功能验证")
print("="*60)

# 1. 检查文件结构
print("\n1. 检查文件结构...")
required_files = [
    "__init__.py",
    "cli.py", 
    "config.py",
    "collector.py",
    "config.yaml",
    "config_template.yaml",
    "README.md",
    "SKILL.md"
]

all_files_exist = True
for file in required_files:
    file_path = Path(__file__).parent / file
    if file_path.exists():
        print(f"   [OK] {file}")
    else:
        print(f"   [MISSING] {file}")
        all_files_exist = False

if not all_files_exist:
    print("\n[ERROR] 缺少必要文件，请检查项目结构")
    sys.exit(1)

print("\n[OK] 所有必要文件都存在")

# 2. 检查Python依赖
print("\n2. 检查Python依赖...")
try:
    import yaml
    print("   [OK] pyyaml")
except ImportError:
    print("   [MISSING] pyyaml - 请运行: pip install pyyaml")
    sys.exit(1)

try:
    import docx
    print("   [OK] python-docx")
except ImportError:
    print("   [MISSING] python-docx - 请运行: pip install python-docx")
    sys.exit(1)

print("\n[OK] 所有Python依赖已安装")

# 3. 检查小红书技能
print("\n3. 检查小红书技能...")
possible_paths = [
    Path(__file__).parent.parent / "xiaohongshu-skills",
    Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-skills",
]

skills_dir = None
for path in possible_paths:
    if path.exists() and (path / "scripts" / "cli.py").exists():
        skills_dir = path
        break

if skills_dir:
    print(f"   [OK] 找到小红书技能目录: {skills_dir}")
else:
    print("   [ERROR] 未找到小红书技能目录")
    print("   请确保已安装小红书技能")
    print("   预期位置:")
    for path in possible_paths:
        print(f"     - {path}")
    sys.exit(1)

# 4. 检查配置文件
print("\n4. 检查配置文件...")
config_path = Path(__file__).parent / "config.yaml"
if config_path.exists():
    print(f"   [OK] 配置文件存在: {config_path}")
    
    # 尝试读取配置文件
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 检查必要配置项
        required_keys = ["basic", "filter", "schedule"]
        for key in required_keys:
            if key in config:
                print(f"   [OK] 配置项: {key}")
            else:
                print(f"   [WARNING] 缺少配置项: {key}")
                
    except Exception as e:
        print(f"   [ERROR] 读取配置文件失败: {e}")
else:
    print("   [WARNING] 配置文件不存在，将使用默认配置")

# 5. 检查输出目录
print("\n5. 检查输出目录...")
output_dir = Path.home() / "Desktop" / "面经收集"
try:
    output_dir.mkdir(parents=True, exist_ok=True)
    test_file = output_dir / "test_write.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("测试写入权限\n")
    
    if test_file.exists():
        test_file.unlink()
        print(f"   [OK] 输出目录可写: {output_dir}")
    else:
        print(f"   [ERROR] 输出目录不可写: {output_dir}")
        
except Exception as e:
    print(f"   [ERROR] 输出目录检查失败: {e}")

# 6. 显示使用说明
print("\n" + "="*60)
print("验证完成！")
print("="*60)

print("\n[NEXT] 下一步操作:")
print("\n1. 初始化配置（可选）:")
print("   python cli.py init")

print("\n2. 查看当前配置:")
print("   python cli.py config")

print("\n3. 运行一次测试收集:")
print("   python cli.py run --once")

print("\n4. 设置定时任务:")
print("   python cli.py schedule")

print("\n5. 查看帮助:")
print("   python cli.py -h")

print("\n[CONFIG] 配置文件位置:")
print(f"   {config_path}")
print("   编辑此文件可以修改所有参数")

print("\n[OUTPUT] 输出目录:")
print(f"   {output_dir}")

print("\n[EDIT] 如果需要修改配置:")
print("   1. 编辑 config.yaml 文件")
print("   2. 或运行 python cli.py init 创建新配置")
print("   3. 参考 config_template.yaml 了解所有可用参数")

print("\n" + "="*60)
print("小红书笔记收集器已准备就绪！")
print("="*60)