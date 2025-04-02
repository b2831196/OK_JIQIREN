from PublicData import PublicAPI

def get_trading_pairs():
    # 初始化API，使用模拟交易模式
    flag = "1"  # 模拟交易: 1, 实盘交易: 0
    api = PublicAPI(flag=flag)
    
    # 获取所有SWAP合约交易对信息
    result = api.get_instruments(instType="SWAP")
    
    if result.get('code') == '0' and 'data' in result:
        # 提取交易对ID
        trading_pairs = [item['instId'] for item in result['data']]
        return trading_pairs
    else:
        print("获取交易对失败:", result.get('msg', 'Unknown error'))
        return []

if __name__ == "__main__":
    print("获取OKX所有合约交易对列表...")
    pairs = get_trading_pairs()
    
    if pairs:
        print(f"成功获取 {len(pairs)} 个交易对:")
        for i, pair in enumerate(pairs, 1):
            print(f"{i}. {pair}")
    else:
        print("未获取到交易对信息") 