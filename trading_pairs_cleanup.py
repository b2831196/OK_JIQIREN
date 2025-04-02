#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
交易对清理脚本
作用：确保trading_pairs.json文件中只包含合约格式（以-SWAP结尾）的交易对
"""

import os
import json
import time
import shutil
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_pairs_cleanup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('TradingPairsCleanup')

# 交易对文件路径
TRADING_PAIRS_FILE = "trading_pairs.json"
BACKUP_DIR = "backups"

def create_backup():
    """创建备份文件"""
    if not os.path.exists(TRADING_PAIRS_FILE):
        logger.warning(f"交易对文件 {TRADING_PAIRS_FILE} 不存在，无需备份")
        return None
    
    # 确保备份目录存在
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # 创建备份文件名（使用当前时间戳）
    timestamp = int(time.time())
    backup_file = f"trading_pairs_backup_{timestamp}.json"
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    
    # 复制文件
    try:
        shutil.copy2(TRADING_PAIRS_FILE, backup_path)
        logger.info(f"已备份原始文件到: {backup_file}")
        return backup_path
    except Exception as e:
        logger.error(f"备份失败: {e}")
        return None

def load_trading_pairs():
    """加载交易对信息"""
    if not os.path.exists(TRADING_PAIRS_FILE):
        logger.warning(f"交易对文件 {TRADING_PAIRS_FILE} 不存在")
        return {}
    
    try:
        with open(TRADING_PAIRS_FILE, 'r', encoding='utf-8') as f:
            trading_pairs = json.load(f)
            return trading_pairs
    except Exception as e:
        logger.error(f"加载交易对数据失败: {e}")
        return {}

def save_trading_pairs(trading_pairs):
    """保存交易对信息"""
    try:
        with open(TRADING_PAIRS_FILE, 'w', encoding='utf-8') as f:
            json.dump(trading_pairs, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存 {len(trading_pairs)} 个交易对到文件")
        return True
    except Exception as e:
        logger.error(f"保存交易对数据失败: {e}")
        return False

def cleanup_trading_pairs():
    """清理交易对，只保留合约格式（以-SWAP结尾）的交易对"""
    # 加载交易对数据
    trading_pairs = load_trading_pairs()
    if not trading_pairs:
        logger.info("没有找到交易对数据，无需清理")
        return
    
    logger.info(f"成功加载交易对数据，共有 {len(trading_pairs)} 个交易对")
    
    # 开始清理
    logger.info(f"开始清理交易对数据，当前有 {len(trading_pairs)} 个交易对")
    
    # 分类统计
    swap_pairs = {k: v for k, v in trading_pairs.items() if k.endswith("-SWAP")}
    non_swap_pairs = {k: v for k, v in trading_pairs.items() if not k.endswith("-SWAP")}
    
    logger.info(f"共有 {len(swap_pairs)} 个SWAP格式交易对和 {len(non_swap_pairs)} 个非SWAP格式交易对")
    
    # 自动转换非SWAP格式为SWAP格式（如果可能）
    converted_pairs = {}
    for pair, info in non_swap_pairs.items():
        if pair.endswith("-USDT") or pair.endswith("-USDC"):
            # 可以转换为SWAP格式
            new_pair = f"{pair}-SWAP"
            if new_pair not in swap_pairs:  # 避免覆盖已有的SWAP格式交易对
                converted_pairs[new_pair] = info
                logger.info(f"将 {pair} 转换为 {new_pair}")
    
    # 合并SWAP格式和已转换的交易对
    cleaned_pairs = {**swap_pairs, **converted_pairs}
    
    # 保存清理后的交易对
    save_trading_pairs(cleaned_pairs)
    
    # 输出清理结果
    logger.info("交易对清理结果:")
    logger.info(f"清理前: {len(trading_pairs)} 个交易对")
    logger.info(f"清理后: {len(cleaned_pairs)} 个交易对")
    logger.info(f"SWAP格式: {len(swap_pairs)} 个")
    logger.info(f"非SWAP格式: {len(non_swap_pairs)} 个")
    logger.info(f"转换为SWAP格式: {len(converted_pairs)} 个")
    logger.info(f"移除重复交易对: {len(trading_pairs) - len(non_swap_pairs) - len(swap_pairs) + len(converted_pairs)} 个")

def main():
    """主函数"""
    logger.info("="*50)
    logger.info(f"开始执行交易对清理 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建备份
    backup_path = create_backup()
    
    # 清理交易对
    cleanup_trading_pairs()
    
    logger.info("="*50)

if __name__ == "__main__":
    main() 