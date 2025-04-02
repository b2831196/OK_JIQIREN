#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading

def update_position_count_periodically():
    """定期更新持仓数量"""
    while True:
        try:
            # 运行更新脚本
            os.system('python update_position_count_direct.py')
        except Exception as e:
            print(f"更新持仓数量时出错: {str(e)}")
        
        # 每60秒更新一次
        time.sleep(60)

if __name__ == "__main__":
    # 启动一个后台线程定期更新持仓数量
    update_thread = threading.Thread(target=update_position_count_periodically)
    update_thread.daemon = True
    update_thread.start()
    
    print("持仓数量更新服务已启动")
    
    # 如果需要，可以在这里启动Flask应用
    # 否则，保持脚本运行以定期更新持仓数量
    while True:
        try:
            time.sleep(3600)  # 每小时检查一次
        except KeyboardInterrupt:
            print("服务已停止")
            break
