#!/usr/bin/env python3
"""
小红书笔记收集器 - 命令行接口
支持配置文件管理、手动运行、定时任务等功能
"""

import os
import sys
import json
import yaml
import argparse
import logging
import datetime
from pathlib import Path
from typing import Dict, Any

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import ConfigManager
from collector import NoteCollector as XiaohongshuCollector

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_skills_dir():
    """查找技能目录"""
    paths = [
        Path(__file__).parent.parent / "xiaohongshu-skills",
        Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-skills",
    ]
    for path in paths:
        if path.exists() and (path / "scripts" / "cli.py").exists():
            return path
    return None

def load_config(config_path: str = None) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path is None:
        # 查找配置文件
        possible_paths = [
            Path("config.yaml"),
            Path("~/.xiaohongshu_collector/config.yaml").expanduser(),
            Path(__file__).parent / "config.yaml"
        ]
        
        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break
        
        if config_path is None:
            logger.error("未找到配置文件，请创建 config.yaml 或使用 --config 参数指定")
            sys.exit(1)
    
    config_path = Path(config_path).expanduser()
    if not config_path.exists():
        logger.error(f"配置文件不存在: {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        
        logger.info(f"加载配置文件: {config_path}")
        return config
        
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        sys.exit(1)

def run_collector(config: Dict[str, Any], once: bool = False) -> bool:
    """运行收集器"""
    try:
        # 查找小红书技能目录
        skills_dir = find_skills_dir()
        if not skills_dir:
            logger.error("未找到小红书技能目录")
            return False
        
        # 初始化收集器
        collector = XiaohongshuCollector(config, skills_dir)
        
        # 运行收集
        logger.info("开始收集小红书笔记...")
        success = collector.collect_and_save()
        
        if success:
            # 获取输出目录
            output_dir = Path(config.get("basic", {}).get("output_dir", "~/Desktop/面经收集")).expanduser()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            keyword = config.get("basic", {}).get("search_keyword", "笔记")
            
            # 构建结果
            result = {
                "success": True,
                "collected_count": config.get("basic", {}).get("collect_count", 0),
                "output_dir": str(output_dir),
                "files": [
                    str(output_dir / f"小红书笔记_{keyword}_{timestamp}.docx"),
                    str(output_dir / f"小红书笔记_{keyword}_{timestamp}.json")
                ]
            }
        else:
            result = {"success": False, "error": "收集失败"}
        
        if result["success"]:
            logger.info(f"收集完成！共收集 {result['collected_count']} 篇笔记")
            logger.info(f"输出目录: {result['output_dir']}")
            
            if result.get("files"):
                for file in result["files"]:
                    logger.info(f"生成文件: {file}")
            
            return True
        else:
            logger.error(f"收集失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        logger.error(f"运行收集器时发生错误: {e}")
        return False

def setup_cron_job(config: Dict[str, Any]) -> bool:
    """设置定时任务"""
    try:
        from cron import add_cron_job
        
        if not config.get("schedule", {}).get("enabled", False):
            logger.info("定时任务未启用")
            return True
        
        cron_expr = config["schedule"]["cron_expression"]
        timezone = config.get("schedule", {}).get("timezone", "Asia/Shanghai")
        
        # 创建定时任务
        job_id = add_cron_job(
            name="小红书笔记收集",
            schedule=cron_expr,
            timezone=timezone,
            config=config
        )
        
        if job_id:
            logger.info(f"定时任务设置成功！任务ID: {job_id}")
            logger.info(f"执行时间: {cron_expr} ({timezone})")
            return True
        else:
            logger.error("设置定时任务失败")
            return False
            
    except ImportError:
        logger.error("cron模块不可用，无法设置定时任务")
        return False
    except Exception as e:
        logger.error(f"设置定时任务时发生错误: {e}")
        return False

def show_config(config: Dict[str, Any]) -> None:
    """显示配置信息"""
    print("\n" + "="*60)
    print("小红书笔记收集器 - 当前配置")
    print("="*60)
    
    # 基本配置
    print("\n[基本配置]:")
    basic = config.get("basic", {})
    print(f"  搜索关键词: {basic.get('search_keyword', '未设置')}")
    print(f"  收集数量: {basic.get('collect_count', '未设置')}")
    print(f"  输出目录: {basic.get('output_dir', '未设置')}")
    print(f"  排序方式: {basic.get('sort_by', '未设置')}")
    
    # 筛选配置
    print("\n[筛选配置]:")
    filter_cfg = config.get("filter", {})
    include = filter_cfg.get("include_keywords", [])
    exclude = filter_cfg.get("exclude_keywords", [])
    print(f"  包含关键词: {', '.join(include[:5])}{'...' if len(include) > 5 else ''}")
    print(f"  排除关键词: {', '.join(exclude[:5])}{'...' if len(exclude) > 5 else ''}")
    
    # 定时任务
    print("\n[定时任务]:")
    schedule = config.get("schedule", {})
    if schedule.get("enabled", False):
        print(f"  状态: 已启用")
        print(f"  执行时间: {schedule.get('cron_expression', '未设置')}")
        print(f"  时区: {schedule.get('timezone', 'Asia/Shanghai')}")
    else:
        print(f"  状态: 未启用")
    
    print("="*60 + "\n")

def create_template_config() -> None:
    """创建配置模板"""
    template_path = Path(__file__).parent / "config_template.yaml"
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        user_config_path = Path("config.yaml")
        if user_config_path.exists():
            print("配置文件已存在，是否覆盖？ (y/N): ", end='')
            choice = input().strip().lower()
            if choice != 'y':
                print("已取消")
                return
        
        with open(user_config_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"配置模板已创建: {user_config_path}")
        print("请编辑此文件并运行: python cli.py run")
    else:
        print("配置模板文件不存在")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小红书笔记收集器 - 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 显示帮助
  python cli.py -h
  
  # 运行一次收集
  python cli.py run
  
  # 运行一次收集（指定配置文件）
  python cli.py run --config my_config.yaml
  
  # 设置定时任务
  python cli.py schedule
  
  # 显示当前配置
  python cli.py config
  
  # 创建配置模板
  python cli.py init
  
  # 测试配置
  python cli.py test
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # run 命令
    run_parser = subparsers.add_parser('run', help='运行一次收集')
    run_parser.add_argument('--config', help='配置文件路径')
    run_parser.add_argument('--once', action='store_true', help='仅运行一次（不设置定时任务）')
    
    # schedule 命令
    schedule_parser = subparsers.add_parser('schedule', help='设置定时任务')
    schedule_parser.add_argument('--config', help='配置文件路径')
    
    # config 命令
    config_parser = subparsers.add_parser('config', help='显示配置信息')
    config_parser.add_argument('--config', help='配置文件路径')
    
    # init 命令
    subparsers.add_parser('init', help='创建配置模板')
    
    # test 命令
    test_parser = subparsers.add_parser('test', help='测试配置')
    test_parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'init':
            create_template_config()
            
        elif args.command == 'config':
            config = load_config(args.config)
            show_config(config)
            
        elif args.command == 'run':
            config = load_config(args.config)
            show_config(config)
            
            print("\n开始收集...")
            success = run_collector(config, args.once)
            
            if success and not args.once:
                print("\n设置定时任务...")
                setup_cron_job(config)
                
        elif args.command == 'schedule':
            config = load_config(args.config)
            show_config(config)
            setup_cron_job(config)
            
        elif args.command == 'test':
            config = load_config(args.config)
            print("配置测试通过！")
            show_config(config)
            
    except KeyboardInterrupt:
        print("\n用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"执行失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()