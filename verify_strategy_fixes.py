#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 读取策略设置页面
with open('templates/strategy_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查关键函数是否存在
key_functions = [
    'function updateButtonStatus',
    'function saveStrategySettings',
    'function checkPositionStatus',
    'function initSettingsPage'
]

# 检查关键变量定义
key_variables = [
    'let strategyRunning = false',
    'let strategyInterval = null',
    'let chichang = false'
]

# 简单输出，以免复杂逻辑错误
print("== 策略功能检查报告 ==")

# 检查函数是否存在
all_functions_exist = True
for func in key_functions:
    exists = func in content
    print(f"函数 {func}: {'存在' if exists else '不存在'}")
    if not exists:
        all_functions_exist = False

# 检查变量是否存在
all_variables_exist = True
for var in key_variables:
    exists = var in content
    print(f"变量 {var}: {'存在' if exists else '不存在'}")
    if not exists:
        all_variables_exist = False

# 检查是否存在策略状态开关代码（应该安全处理）
has_safe_toggle = 'const statusToggle = document.querySelector(\'.toggle-wrapper\');' in content and 'if (statusToggle) {' in content
print(f"策略状态开关安全处理: {'已实现' if has_safe_toggle else '未实现'}")

# 检查续下单按钮是否存在
continue_order_exists = 'id="continue-order-btn"' in content
print(f"续下单按钮: {'存在' if continue_order_exists else '不存在'}")

# 总结判断
if all_functions_exist and all_variables_exist and has_safe_toggle and continue_order_exists:
    print("\n所有检查项都已通过，策略功能应该已恢复正常！")
else:
    print("\n存在一些问题需要解决!") 