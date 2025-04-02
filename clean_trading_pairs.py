#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
交易对清理工具
用于检查并规范化trading_pairs.json中的交易对，确保只保留SWAP格式的交易对
"""

import os
import json
import time
import logging
from datetime import datetime

# 设置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_pairs_cleanup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingPairsCleanup")

# 定义文件路径
TRADING_PAIRS_FILE = "trading_pairs.json"
BACKUP_FILE = f"trading_pairs_backup_{int(time.time())}.json"

def load_trading_pairs():
    """加载交易对信息"""
    if not os.path.exists(TRADING_PAIRS_FILE):
        logger.warning(f"文件不存在: {TRADING_PAIRS_FILE}")
        return {}
    
    try:
        with open(TRADING_PAIRS_FILE, 'r', encoding='utf-8') as f:
            trading_pairs = json.load(f)
            logger.info(f"成功加载交易对数据，包含 {len(trading_pairs)} 个交易对")
            return trading_pairs
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
        return {}
    except Exception as e:
        logger.error(f"加载文件时出错: {e}")
        return {}

def save_trading_pairs(trading_pairs):
    """保存交易对信息"""
    try:
        with open(TRADING_PAIRS_FILE, 'w', encoding='utf-8') as f:
            json.dump(trading_pairs, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存 {len(trading_pairs)} 个交易对到文件")
        return True
    except Exception as e:
        logger.error(f"保存文件时出错: {e}")
        return False

def backup_trading_pairs():
    """备份原始交易对文件"""
    if not os.path.exists(TRADING_PAIRS_FILE):
        logger.warning(f"无需备份，文件不存在: {TRADING_PAIRS_FILE}")
        return False
    
    try:
        with open(TRADING_PAIRS_FILE, 'r', encoding='utf-8') as source:
            with open(BACKUP_FILE, 'w', encoding='utf-8') as target:
                target.write(source.read())
        logger.info(f"已备份原始文件到: {BACKUP_FILE}")
        return True
    except Exception as e:
        logger.error(f"备份文件时出错: {e}")
        return False

def clean_trading_pairs():
    """清理交易对，规范化格式"""
    # 备份原始文件
    backup_trading_pairs()
    
    # 加载交易对数据
    trading_pairs = load_trading_pairs()
    if not trading_pairs:
        logger.warning("交易对数据为空，无需清理")
        return
    
    logger.info(f"开始清理交易对数据，当前有 {len(trading_pairs)} 个交易对")
    
    # 统计信息
    stats = {
        "total_before": len(trading_pairs),
        "swap_count": 0,
        "non_swap_count": 0,
        "converted_count": 0,
        "removed_count": 0,
        "total_after": 0
    }
    
    # 创建一个新的字典来存储清理后的交易对
    cleaned_pairs = {}
    
    # 分类交易对
    swap_pairs = {}
    non_swap_pairs = {}
    
    for pair, info in trading_pairs.items():
        if pair.endswith("-SWAP"):
            swap_pairs[pair] = info
            stats["swap_count"] += 1
        else:
            non_swap_pairs[pair] = info
            stats["non_swap_count"] += 1
    
    logger.info(f"发现 {stats['swap_count']} 个SWAP格式交易对和 {stats['non_swap_count']} 个非SWAP格式交易对")
    
    # 处理所有SWAP格式交易对
    for pair, info in swap_pairs.items():
        cleaned_pairs[pair] = info
    
    # 处理非SWAP格式交易对
    for pair, info in non_swap_pairs.items():
        # 创建SWAP格式的交易对名称
        swap_pair = f"{pair}-SWAP"
        
        # 检查是否已经存在对应的SWAP格式交易对
        if swap_pair in cleaned_pairs:
            logger.info(f"跳过 {pair}，因为已存在对应的SWAP格式交易对: {swap_pair}")
            stats["removed_count"] += 1
        else:
            # 添加转换后的SWAP格式交易对
            cleaned_pairs[swap_pair] = info
            logger.info(f"转换 {pair} -> {swap_pair}")
            stats["converted_count"] += 1
    
    # 更新统计信息
    stats["total_after"] = len(cleaned_pairs)
    
    # 保存清理后的交易对
    save_result = save_trading_pairs(cleaned_pairs)
    
    # 输出清理结果
    if save_result:
        logger.info("交易对清理完成")
        logger.info(f"清理前: {stats['total_before']} 个交易对")
        logger.info(f"清理后: {stats['total_after']} 个交易对")
        logger.info(f"SWAP格式: {stats['swap_count']} 个")
        logger.info(f"非SWAP格式: {stats['non_swap_count']} 个")
        logger.info(f"转换为SWAP格式: {stats['converted_count']} 个")
        logger.info(f"移除重复交易对: {stats['removed_count']} 个")
    else:
        logger.error("保存清理后的交易对失败")

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info(f"开始执行交易对清理 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    clean_trading_pairs()
    logger.info("=" * 50) 