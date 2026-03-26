// 小红书笔记收集器 - JavaScript

// 全局变量
let currentTab = 'basic';
let taskInterval = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initApp();
    loadConfig();
    checkStatus();
});

// 初始化应用
function initApp() {
    // 标签页切换
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    // 按钮事件
    document.getElementById('run-now').addEventListener('click', runCollector);
    document.getElementById('save-config').addEventListener('click', saveConfig);
    document.getElementById('load-default').addEventListener('click', loadDefaultConfig);
    document.getElementById('export-config').addEventListener('click', exportConfig);
    
    // 表单验证
    setupFormValidation();
}

// 切换标签页
function switchTab(tabName) {
    // 更新按钮状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // 更新内容区域
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    currentTab = tabName;
}

// 加载配置
function loadConfig() {
    fetch('/api/config')
        .then(response => response.json())
        .then(config => {
            if (config.success) {
                populateForm(config.data);
                updateStatus('config-status', '已加载', 'success');
            } else {
                updateStatus('config-status', '加载失败', 'error');
            }
        })
        .catch(error => {
            console.error('加载配置失败:', error);
            updateStatus('config-status', '加载失败', 'error');
        });
}

// 填充表单
function populateForm(config) {
    // 基本设置
    document.getElementById('search_keyword').value = config.basic.search_keyword || '';
    document.getElementById('collect_count').value = config.basic.collect_count || 3;
    document.getElementById('output_dir').value = config.basic.output_dir || '';
    document.getElementById('output_filename').value = config.basic.output_filename || '';
    
    // 筛选设置
    document.getElementById('include_keywords').value = config.filter.include_keywords?.join('
') || '';
    document.getElementById('exclude_keywords').value = config.filter.exclude_keywords?.join('
') || '';
    document.getElementById('min_content_length').value = config.filter.min_content_length || 100;
    document.getElementById('enable_content_filter').checked = config.filter.enable_content_filter || true;
    
    // 定时设置
    document.getElementById('enable_schedule').checked = config.schedule.enable_schedule || false;
    document.getElementById('cron_expression').value = config.schedule.cron_expression || '0 9 * * *';
    
    // 高级设置
    document.getElementById('request_delay_min').value = config.advanced.request_delay_min || 0.5;
    document.getElementById('request_delay_max').value = config.advanced.request_delay_max || 2.0;
    document.getElementById('max_search_attempts').value = config.advanced.max_search_attempts || 3;
    document.getElementById('enable_logging').checked = config.advanced.enable_logging || true;
    document.getElementById('log_level').value = config.advanced.log_level || 'INFO';
}

// 保存配置
function saveConfig() {
    const config = collectFormData();
    
    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showAlert('配置保存成功！', 'success');
        } else {
            showAlert('配置保存失败: ' + result.message, 'error');
        }
    })
    .catch(error => {
        console.error('保存配置失败:', error);
        showAlert('保存配置失败: ' + error.message, 'error');
    });
}

// 收集表单数据
function collectFormData() {
    return {
        basic: {
            search_keyword: document.getElementById('search_keyword').value,
            collect_count: parseInt(document.getElementById('collect_count').value),
            output_dir: document.getElementById('output_dir').value,
            output_filename: document.getElementById('output_filename').value
        },
        filter: {
            include_keywords: document.getElementById('include_keywords').value.split('
').filter(k => k.trim()),
            exclude_keywords: document.getElementById('exclude_keywords').value.split('
').filter(k => k.trim()),
            min_content_length: parseInt(document.getElementById('min_content_length').value),
            enable_content_filter: document.getElementById('enable_content_filter').checked
        },
        schedule: {
            enable_schedule: document.getElementById('enable_schedule').checked,
            cron_expression: document.getElementById('cron_expression').value
        },
        advanced: {
            request_delay_min: parseFloat(document.getElementById('request_delay_min').value),
            request_delay_max: parseFloat(document.getElementById('request_delay_max').value),
            max_search_attempts: parseInt(document.getElementById('max_search_attempts').value),
            enable_logging: document.getElementById('enable_logging').checked,
            log_level: document.getElementById('log_level').value
        }
    };
}

// 加载默认配置
function loadDefaultConfig() {
    if (confirm('确定要恢复默认配置吗？当前配置将丢失。')) {
        fetch('/api/config/default', { method: 'POST' })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    loadConfig();
                    showAlert('默认配置已恢复', 'success');
                } else {
                    showAlert('恢复默认配置失败', 'error');
                }
            });
    }
}

// 导出配置
function exportConfig() {
    const config = collectFormData();
    const dataStr = JSON.stringify(config, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'xiaohongshu_collector_config.json';
    link.click();
}

// 运行收集器
function runCollector() {
    if (confirm('确定要立即运行收集器吗？')) {
        fetch('/api/run', { method: 'POST' })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    showAlert('收集任务已启动', 'success');
                    startTaskMonitoring();
                } else {
                    showAlert('启动失败: ' + result.message, 'error');
                }
            })
            .catch(error => {
                console.error('启动任务失败:', error);
                showAlert('启动失败: ' + error.message, 'error');
            });
    }
}

// 开始任务监控
function startTaskMonitoring() {
    if (taskInterval) {
        clearInterval(taskInterval);
    }
    
    taskInterval = setInterval(() => {
        checkTaskStatus();
    }, 2000); // 每2秒检查一次
}

// 检查任务状态
function checkTaskStatus() {
    fetch('/api/task/status')
        .then(response => response.json())
        .then(status => {
            updateTaskStatus(status);
            
            // 如果任务完成或出错，停止监控
            if (!status.running && status.end_time) {
                clearInterval(taskInterval);
                taskInterval = null;
                
                if (status.error) {
                    showAlert('任务执行失败: ' + status.error, 'error');
                } else {
                    showAlert('任务执行完成！', 'success');
                }
            }
        });
}

// 更新任务状态显示
function updateTaskStatus(status) {
    const taskStatusEl = document.getElementById('task-status');
    const lastRunEl = document.getElementById('last-run');
    const progressEl = document.getElementById('progress-fill');
    const progressTextEl = document.getElementById('progress-text');
    const progressMessageEl = document.getElementById('progress-message');
    
    if (status.running) {
        taskStatusEl.textContent = '运行中';
        taskStatusEl.className = 'status-value status-online';
        
        // 更新进度条
        if (progressEl) {
            progressEl.style.width = status.progress + '%';
        }
        if (progressTextEl) {
            progressTextEl.textContent = status.progress + '%';
        }
        if (progressMessageEl) {
            progressMessageEl.textContent = status.message || '处理中...';
        }
    } else {
        taskStatusEl.textContent = '空闲';
        taskStatusEl.className = 'status-value';
        
        if (status.end_time) {
            const endTime = new Date(status.end_time);
            lastRunEl.textContent = endTime.toLocaleString();
        }
    }
}

// 检查系统状态
function checkStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(status => {
            updateStatus('skills-status', status.skills_available ? '已找到' : '未找到', 
                        status.skills_available ? 'success' : 'warning');
            
            if (status.task_status) {
                updateTaskStatus(status.task_status);
            }
        });
}

// 更新状态显示
function updateStatus(elementId, text, type) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = text;
        element.className = `status-value status-${type}`;
    }
}

// 显示提示消息
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} slide-in`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // 3秒后自动消失
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// 设置表单验证
function setupFormValidation() {
    const forms = document.querySelectorAll('input, textarea, select');
    forms.forEach(form => {
        form.addEventListener('input', function() {
            validateField(this);
        });
    });
}

// 验证字段
function validateField(field) {
    const value = field.value.trim();
    
    // 清除之前的错误状态
    field.classList.remove('error');
    
    // 根据字段类型进行验证
    switch(field.type) {
        case 'number':
            if (field.min && parseInt(value) < parseInt(field.min)) {
                field.classList.add('error');
            }
            if (field.max && parseInt(value) > parseInt(field.max)) {
                field.classList.add('error');
            }
            break;
        case 'text':
            if (field.required && !value) {
                field.classList.add('error');
            }
            break;
    }
}

// 工具函数：格式化时间
function formatTime(date) {
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
