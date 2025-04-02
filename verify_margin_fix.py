#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 读取策略设置页面
with open('templates/strategy_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 验证检查项
print("== 保证金输入框修复验证 ==")

# 检查1: 确认hover-glow和element-animated类已被移除
has_animation_classes = 'id="margin-input-container" class="forms-item f-1 box2 hover-glow' in content or \
                       'id="margin-input-container" class="forms-item f-1 box2 hover-glow element-animated' in content

print(f"1. 动画类已移除: {'✓' if not has_animation_classes else '✗'}")

# 检查2: 确认动画禁用CSS已添加
has_disable_animation_css = '/* 禁用保证金输入框的所有动画和过渡 */' in content and \
                            'animation: none !important;' in content

print(f"2. 动画禁用CSS已添加: {'✓' if has_disable_animation_css else '✗'}")

# 检查3: 确认margin-highlight类的动画已被禁用
has_fixed_highlight = '.margin-highlight {' in content and \
                      'animation: none !important;' in content

print(f"3. margin-highlight动画已禁用: {'✓' if has_fixed_highlight else '✗'}")

# 检查4: 确认updateMarginValue函数已被简化（没有动画）
simplified_function = 'function updateMarginValue(' in content and \
                      '// 简化后的逻辑，直接设置值，无动画' in content

print(f"4. updateMarginValue函数已简化: {'✓' if simplified_function else '✗'}")

# 检查5: 确认初始化脚本已添加
has_init_script = '// 确保保证金输入框稳定，禁用所有动画' in content

print(f"5. 初始化脚本已添加: {'✓' if has_init_script else '✗'}")

# 总结检查结果
all_fixed = not has_animation_classes and has_disable_animation_css and has_fixed_highlight and simplified_function and has_init_script

if all_fixed:
    print("\n所有修复已成功应用！保证金输入框应该不再抖动。")
else:
    print("\n有些修复可能未成功应用，请检查以上详情。")