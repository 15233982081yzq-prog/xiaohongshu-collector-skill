"""
小红书笔记收集器 - 主模块
提供简单的API接口
"""

import os
import sys
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

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

class XiaohongshuCollectorSkill:
    """小红书笔记收集器Skill主类"""
    
    def __init__(self, config_path: str = None):
        """
        初始化收集器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config_manager = ConfigManager(config_path)
        self.collector = XiaohongshuCollector(self.config_manager)
        logger.info("小红书笔记收集器初始化完成")
    
    def run(self, once: bool = False) -> Dict[str, Any]:
        """
        运行收集器
        
        Args:
            once: 是否只运行一次（不设置定时任务）
            
        Returns:
            收集结果
        """
        try:
            logger.info("开始收集小红书笔记...")
            
            # 运行收集
            result = self.collector.collect()
            
            if result["success"]:
                logger.info(f"收集完成！共收集 {result['collected_count']} 篇笔记")
                return result
            else:
                logger.error(f"收集失败: {result.get('error', '未知错误')}")
                return result
                
        except Exception as e:
            error_msg = f"运行收集器时发生错误: {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config_manager.get_config()
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """更新配置"""
        return self.config_manager.update_config(new_config)
    
    def test_connection(self) -> bool:
        """测试连接"""
        return self.collector.test_connection()

# 导出主要功能
__all__ = [
    'XiaohongshuCollectorSkill',
    'ConfigManager',
    'XiaohongshuCollector'
]

# 如果直接运行此文件，显示使用说明
if __name__ == '__main__':
    print("="*60)
    print("小红书笔记收集器")
    print("="*60)
    print("\n使用方式:")
    print("\n1. 命令行方式:")
    print("   python cli.py run          # 运行一次收集")
    print("   python cli.py schedule     # 设置定时任务")
    print("   python cli.py config       # 显示配置信息")
    print("   python cli.py init         # 创建配置模板")
    print("   python cli.py test         # 测试配置")
    
    print("\n2. 作为模块导入:")
    print("   from xiaohongshu_collector import XiaohongshuCollectorSkill")
    print("   skill = XiaohongshuCollectorSkill()")
    print("   result = skill.run()")
    
    print("\n3. 配置文件:")
    print("   编辑 config.yaml 文件修改参数")
    print("   参考 config_template.yaml 了解所有可用参数")
    
    print("\n4. 定时任务:")
    print("   在 config.yaml 中设置 schedule.enabled: true")
    print("   设置 cron_expression 指定执行时间")
    
    print("\n" + "="*60)