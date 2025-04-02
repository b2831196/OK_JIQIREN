with open('templates/strategy_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到我们需要插入策略状态开关的位置
insert_position = content.find('<div class="settings-row">\n                    <div class="setting-label">续下单')

if insert_position != -1:
    # 创建策略状态开关的HTML
    strategy_toggle = '''                <div class="settings-row">
                    <div class="setting-label">策略状态</div>
                    <div class="setting-value">
                        <div role="checkbox" class="toggle-wrapper {% if strategy.status == 'running' %}active-lis{% endif %}">
                            <span class="toggle-background"></span>
                            <span class="toggle-indicator" style="{% if strategy.status == 'running' %}transform: translateX(28px);{% else %}transform: translateX(0px);{% endif %}"></span>
                        </div>
                    </div>
                </div>
'''
    
    # 在续下单按钮前插入策略状态开关
    new_content = content[:insert_position] + strategy_toggle + content[insert_position:]
    
    # 写回文件
    with open('templates/strategy_settings.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("已恢复策略状态开关，同时保留续下单按钮")
else:
    print("无法找到续下单按钮位置，恢复失败") 