with open('templates/strategy_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定位并删除整个策略状态的按钮部分
status_toggle_pattern = '''                <div class="settings-row">
                    <div class="setting-label">策略状态</div>
                    <div class="setting-value">
                        <div role="checkbox" class="toggle-wrapper {% if strategy.status == 'running' %}active-lis{% endif %}">
                            <span class="toggle-background"></span>
                            <span class="toggle-indicator" style="{% if strategy.status == 'running' %}transform: translateX(28px);{% else %}transform: translateX(0px);{% endif %}"></span>
                        </div>
                    </div>
                </div>'''

# 移除该部分
modified_content = content.replace(status_toggle_pattern, '')

# 同时移除与策略状态开关相关的JS代码
js_toggle_pattern = '''            // 为策略状态开关添加点击事件
            const strategyToggle = document.querySelector('.toggle-wrapper');
            if(strategyToggle) {
                strategyToggle.addEventListener('click', function() {
                    // 切换active-lis类
                    this.classList.toggle('active-lis');
                    
                    // 切换指示器位置
                    const indicator = this.querySelector('.toggle-indicator');
                    if(indicator) {
                        if(this.classList.contains('active-lis')) {
                            indicator.style.transform = 'translateX(28px)';
                            strategyRunning = true;
                            showToast('策略已启动');
                        } else {
                            indicator.style.transform = 'translateX(0px)';
                            strategyRunning = false;
                            showToast('策略已停止');
                        }
                    }
                    
                    // 更新按钮状态
                    updateButtonStatus(chichang, strategyRunning);
                });
            }'''

modified_content = modified_content.replace(js_toggle_pattern, '')

# 写回文件
with open('templates/strategy_settings.html', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print("策略状态按钮已完全删除，仅保留续下单按钮") 