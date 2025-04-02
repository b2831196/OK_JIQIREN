import os
import json
import time

# 定义存储交易对信息的JSON文件路径
TRADING_PAIRS_FILE = "trading_pairs.json"

def load_trading_pairs():
    """
    加载交易对信息
    
    返回:
    - 字典格式的交易对信息 {交易对: USDT金额}
    """
    # 如果文件不存在，返回空字典
    if not os.path.exists(TRADING_PAIRS_FILE):
        return {}
    
    try:
        with open(TRADING_PAIRS_FILE, 'r', encoding='utf-8') as f:
            trading_pairs = json.load(f)
            return trading_pairs
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"加载交易对数据失败: {e}")
        # 如果文件损坏或为空，返回空字典
        return {}

def save_trading_pairs(trading_pairs):
    """
    保存交易对信息到JSON文件
    
    参数:
    - trading_pairs: 字典格式的交易对信息 {交易对: {"amount": USDT金额, "timestamp": 时间戳}}
    """
    try:
        with open(TRADING_PAIRS_FILE, 'w', encoding='utf-8') as f:
            json.dump(trading_pairs, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存交易对数据失败: {e}")
        return False

def add_trading_pair(trade_pair, usdt_amount):
    """
    添加或更新交易对信息
    
    参数:
    - trade_pair: 交易对字符串，例如 "BTC-USDT"
    - usdt_amount: USDT金额数值
    
    返回:
    - 布尔值，表示操作是否成功
    """
    # 确保交易对格式统一，去除可能的额外空格
    trade_pair = trade_pair.strip()
    
    # 规范化交易对格式，确保使用SWAP格式
    # 如果不是SWAP格式，则转换为SWAP格式
    if not trade_pair.endswith("-SWAP"):
        # 基础交易对先去掉可能的SWAP后缀，再添加SWAP
        base_pair = trade_pair.replace("-SWAP", "")
        trade_pair = f"{base_pair}-SWAP"
        print(f"已规范化交易对格式: {base_pair} -> {trade_pair}")
    
    # 加载现有数据
    trading_pairs = load_trading_pairs()
    
    # 删除可能存在的非SWAP版本交易对
    base_pair = trade_pair.replace("-SWAP", "")
    if base_pair in trading_pairs:
        print(f"删除非SWAP格式的交易对: {base_pair}")
        del trading_pairs[base_pair]
    
    # 检查交易对是否已存在
    if trade_pair in trading_pairs:
        # 如果已存在且金额没变，不做操作
        if trading_pairs[trade_pair]["amount"] == usdt_amount:
            print(f"交易对 {trade_pair} 已存在且金额相同，无需更新")
            return True
    
    # 添加或更新交易对
    trading_pairs[trade_pair] = {
        "amount": usdt_amount,
        "timestamp": int(time.time())
    }
    
    # 保存更新后的数据
    return save_trading_pairs(trading_pairs)

def remove_trading_pair(trade_pair):
    """
    从存储中删除指定交易对
    
    参数:
    - trade_pair: 要删除的交易对字符串
    
    返回:
    - 布尔值，表示操作是否成功
    """
    # 确保交易对格式统一，去除可能的额外空格
    trade_pair = trade_pair.strip()
    
    # 加载现有数据
    trading_pairs = load_trading_pairs()
    
    # 尝试删除SWAP版本和非SWAP版本
    swap_pair = trade_pair if trade_pair.endswith("-SWAP") else f"{trade_pair}-SWAP"
    base_pair = trade_pair.replace("-SWAP", "")
    
    deleted = False
    
    # 删除SWAP版本
    if swap_pair in trading_pairs:
        del trading_pairs[swap_pair]
        print(f"已删除SWAP格式交易对: {swap_pair}")
        deleted = True
        
    # 删除非SWAP版本
    if base_pair in trading_pairs:
        del trading_pairs[base_pair]
        print(f"已删除非SWAP格式交易对: {base_pair}")
        deleted = True
    
    # 如果都不存在，返回成功
    if not deleted:
        print(f"交易对 {trade_pair} 不存在，无需删除")
        return True
    
    # 保存更新后的数据
    return save_trading_pairs(trading_pairs)

def get_all_trading_pairs():
    """
    获取所有存储的交易对信息
    
    返回:
    - 字典格式的交易对信息 {交易对: {"amount": USDT金额, "timestamp": 时间戳}}
    """
    return load_trading_pairs()

def get_trading_pair(trade_pair):
    """
    获取指定交易对的信息
    
    参数:
    - trade_pair: 交易对字符串
    
    返回:
    - 字典格式的交易对信息 {"amount": USDT金额, "timestamp": 时间戳}，如果不存在则返回None
    """
    trading_pairs = load_trading_pairs()
    
    # 尝试查找SWAP版本
    if trade_pair.endswith("-SWAP"):
        return trading_pairs.get(trade_pair)
    
    # 如果未找到，尝试查找SWAP版本
    swap_pair = f"{trade_pair}-SWAP"
    return trading_pairs.get(swap_pair)

# 如果直接运行此文件，进行简单测试
if __name__ == "__main__":
    # 测试添加交易对
    add_trading_pair("BTC-USDT", 1000)
    add_trading_pair("ETH-USDT", 500)
    
    # 打印所有交易对
    print("所有交易对:", get_all_trading_pairs())
    
    # 测试获取特定交易对
    print("BTC-USDT信息:", get_trading_pair("BTC-USDT"))
    
    # 测试删除交易对
    remove_trading_pair("ETH-USDT")
    print("删除后的交易对:", get_all_trading_pairs()) 