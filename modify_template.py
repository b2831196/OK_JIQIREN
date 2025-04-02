with open('templates/strategy_settings.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到策略状态开始的行
start_line = -1
for i, line in enumerate(lines):
    if '策略状态' in line:
        # 找到"策略状态"所在的行
        start_line = i - 1  # 包括<div class="settings-row">这一行
        break

if start_line >= 0:
    # 寻找结束的行 - 匹配完整的div块
    end_line = -1
    div_count = 0
    
    # 计算需要找到的</div>数量
    for i in range(start_line, min(start_line + 20, len(lines))):
        line = lines[i]
        if '<div' in line:
            div_count += 1
        if '</div>' in line:
            div_count -= 1
            if div_count == 0:
                end_line = i
                break
    
    if end_line > 0:
        # 删除策略状态部分
        new_lines = lines[:start_line] + lines[end_line+1:]
        
        # 写回文件
        with open('templates/strategy_settings.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f'成功删除策略状态部分，从第{start_line+1}行到第{end_line+1}行')
    else:
        print(f'未能确定策略状态部分的结束位置')
else:
    print('未找到"策略状态"部分') 