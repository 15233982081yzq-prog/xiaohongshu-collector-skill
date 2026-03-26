"""
配置管理模块
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import datetime

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        "version": "1.0.0",
        "basic": {
            "search_keyword": "后端面试",
            "collect_count": 3,
            "output_dir": str(Path.home() / "Desktop" / "面经"),
            "output_filename": "xiaohongshu_notes_{date}.docx",
            "enable_logging": True,
            "log_level": "INFO"
        },
        "filter": {
            "include_keywords": [
                "面试", "面经", "问题", "题目", "考题", "笔试",
                "一面", "二面", "三面", "终面", "技术面", "HR面",
                "Java", "Python", "Go", "C++", "后端", "后台",
                "数据库", "MySQL", "Redis", "Spring", "微服务"
            ],
            "exclude_keywords": [
                "招聘", "招人", "内推", "直聘", "求职", "找工作",
                "广告", "推广", "营销", "带货", "商品", "产品",
                "娱乐", "搞笑", "生活", "日常", "vlog", "旅游"
            ],
            "min_content_length": 100,
            "quality_threshold": 3,
            "strict_mode": False
        },
        "schedule": {
            "enable_schedule": False,
            "cron_expression": "0 23 * * *",
            "timezone": "Asia/Shanghai"
        },
        "advanced": {
            "enable_screenshot": False,
            "request_delay_min": 3.0,
            "request_delay_max": 8.0,
            "max_retries": 3,
            "auto_login": True,
            "check_login": True
        }
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """初始化配置管理器"""
        if config_dir is None:
            config_dir = Path.home() / ".xiaohongshu_collector"
        
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = config_dir / "config.json"
        self.history_dir = config_dir / "history"
        self.history_dir.mkdir(exist_ok=True)
        
        self.config = self.load_config()
    
    def load_config(self, filepath: Optional[Path] = None) -> Dict[str, Any]:
        """加载配置"""
        if filepath is None:
            filepath = self.config_file
        
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # 合并配置
                config = self._deep_merge(self.DEFAULT_CONFIG.copy(), loaded_config)
                logger.info(f"从 {filepath} 加载配置")
                return config
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            logger.info("使用默认配置")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Optional[Dict] = None, filepath: Optional[Path] = None):
        """保存配置"""
        if config is None:
            config = self.config
        
        if filepath is None:
            filepath = self.config_file
        
        try:
            # 备份旧配置
            if filepath.exists():
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.history_dir / f"config_backup_{timestamp}.json"
                
                # 如果备份文件已存在，先删除再重命名
                if backup_file.exists():
                    backup_file.unlink()
                
                filepath.rename(backup_file)
                logger.info(f"旧配置已备份到: {backup_file}")
            
            # 保存新配置
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.config = config
            logger.info(f"配置已保存到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def update_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新配置"""
        self.config = self._deep_merge(self.config, updates)
        self.save_config()
        return self.config
    
    def reset_config(self) -> Dict[str, Any]:
        """重置为默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
        return self.config
    
    def reset_to_default(self) -> Dict[str, Any]:
        """重置为默认配置（别名方法，用于Web界面）"""
        return self.reset_config()
    
    def export_config(self, filepath: Path) -> bool:
        """导出配置到文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置已导出到: {filepath}")
            return True
        except Exception as e:
            logger.error(f"导出配置失败: {e}")
            return False
    
    def import_config(self, filepath: Path) -> bool:
        """从文件导入配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            self.config = self._deep_merge(self.DEFAULT_CONFIG.copy(), imported_config)
            self.save_config()
            logger.info(f"配置已从 {filepath} 导入")
            return True
        except Exception as e:
            logger.error(f"导入配置失败: {e}")
            return False
    
    def get_config_section(self, section: str) -> Dict[str, Any]:
        """获取配置部分"""
        return self.config.get(section, {})
    
    def set_config_value(self, section: str, key: str, value: Any):
        """设置配置值"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        self.save_config()
    
    def get_config_value(self, section: str, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(section, {}).get(key, default)
    
    def list_history(self) -> List[Dict[str, Any]]:
        """列出历史配置"""
        history_files = []
        for file in self.history_dir.glob("config_backup_*.json"):
            try:
                stat = file.stat()
                history_files.append({
                    "filename": file.name,
                    "path": str(file),
                    "size": stat.st_size,
                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime),
                    "created": datetime.datetime.fromtimestamp(stat.st_ctime)
                })
            except Exception as e:
                logger.error(f"读取历史文件失败 {file}: {e}")
        
        # 按修改时间排序
        history_files.sort(key=lambda x: x["modified"], reverse=True)
        return history_files
    
    def restore_from_history(self, filename: str) -> bool:
        """从历史恢复配置"""
        history_file = self.history_dir / filename
        if not history_file.exists():
            logger.error(f"历史文件不存在: {filename}")
            return False
        
        return self.import_config(history_file)
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """深度合并字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def validate_config(self, config: Optional[Dict] = None) -> Dict[str, Any]:
        """验证配置"""
        if config is None:
            config = self.config
        
        errors = []
        warnings = []
        
        # 验证基本配置
        basic = config.get('basic', {})
        if not basic.get('search_keyword'):
            errors.append("搜索关键词不能为空")
        
        count = basic.get('collect_count', 0)
        if count < 1 or count > 20:
            warnings.append(f"收集数量 {count} 可能不合理，建议1-20之间")
        
        # 验证筛选配置
        filter_config = config.get('filter', {})
        if not filter_config.get('include_keywords'):
            warnings.append("包含关键词列表为空，可能无法筛选内容")
        
        # 验证高级配置
        advanced = config.get('advanced', {})
        if advanced.get('request_delay_min', 0) < 1:
            warnings.append("请求延迟过小可能触发风控")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "has_warnings": len(warnings) > 0
        }
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        return {
            "basic": {
                "search_keyword": self.config['basic']['search_keyword'],
                "collect_count": self.config['basic']['collect_count'],
                "output_dir": self.config['basic']['output_dir']
            },
            "filter": {
                "include_keywords_count": len(self.config['filter']['include_keywords']),
                "exclude_keywords_count": len(self.config['filter']['exclude_keywords']),
                "strict_mode": self.config['filter']['strict_mode']
            },
            "schedule": {
                "enabled": self.config['schedule']['enable_schedule'],
                "next_run": self._calculate_next_run() if self.config['schedule']['enable_schedule'] else None
            },
            "advanced": {
                "enable_screenshot": self.config['advanced']['enable_screenshot'],
                "max_retries": self.config['advanced']['max_retries']
            }
        }
    
    def _calculate_next_run(self) -> Optional[datetime.datetime]:
        """计算下次运行时间（简化版）"""
        # 这里应该实现cron表达式的解析
        # 暂时返回None，实际使用时需要实现
        return None