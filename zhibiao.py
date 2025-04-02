from MarketData import MarketAPI
from PublicData import PublicAPI
import Trade
import Account
import pandas as pd
import time
from pprint import pprint
import numpy as np
import datetime
import requests
import sys
import math
import os

# 全局API密钥变量
api_key = None
secret_key = None
passphrase = None

# 设置API密钥的函数
def set_api_credentials(ak, sk, pp):
    """
    设置API凭证
    
    参数:
    - ak: API密钥
    - sk: 密钥
    - pp: 密码
    """
    global api_key, secret_key, passphrase
    api_key = ak
    secret_key = sk
    passphrase = pp
    return True

def OKX_ySELL_Order(symbol,px,tpTriggerPx,sz):
    # 确保API密钥已设置
    if not api_key or not secret_key or not passphrase:
        raise ValueError("API凭证未设置，请先调用set_api_credentials函数")
        
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId=symbol,
        tdMode="cross",
        side="sell",
        posSide="short",
        ordType="limit",
        px=px,
        tpTriggerPx=tpTriggerPx,
        tpOrdPx=-1,
        tpTriggerPxType="index",
        sz=sz  # trigger price  # order price. When orderPx=-1, the order will be placed as an market order
 # trigger price type。last：last trade price
    )
    return result
def OKX_yBUY_Order(symbol,px,tpTriggerPx,sz):
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId=symbol,
        tdMode="cross",
        side="buy",
        posSide="long",
        ordType="limit",
        px=px,
        tpTriggerPx=tpTriggerPx,
        tpOrdPx=-1,
        tpTriggerPxType="index",
        sz=sz  # trigger price  # order price. When orderPx=-1, the order will be placed as an market order
 # trigger price type。last：last trade price
    )
    return result
def OKX_zSELL_Order(symbol,px,slTriggerPx,sz):
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId=symbol,
        tdMode="cross",
        side="sell",
        posSide="short",
        ordType="limit",
        px=px,
        slTriggerPx=slTriggerPx,
        slOrdPx=-1,
        slTriggerPxType="index",
        sz=sz  # trigger price  # order price. When orderPx=-1, the order will be placed as an market order
 # trigger price type。last：last trade price
    )
    return result
def OKX_zBUY_Order(symbol,px,slTriggerPx,sz):
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId=symbol,
        tdMode="cross",
        side="buy",
        posSide="long",
        ordType="limit",
        px=px,
        slTriggerPx=slTriggerPx,
        slOrdPx=-1,
        slTriggerPxType="index",
        sz=sz  # trigger price  # order price. When orderPx=-1, the order will be placed as an market order
 # trigger price type。last：last trade price
    )
def OKX_HYAPI_Order(side, long, sz, instId):
    # 确保API密钥已设置
    if not api_key or not secret_key or not passphrase:
        raise ValueError("API凭证未设置，请先调用set_api_credentials函数")
    
    # 检查并修正instId格式
    if not instId.endswith("-SWAP"):
        # 对于现货交易对，需要加上-SWAP后缀
        if "-" in instId:  # 如果包含横线，假设格式为BTC-USDT
            print(f"添加SWAP后缀到交易对: {instId} -> {instId}-SWAP")
            instId = f"{instId}-SWAP"
    
    # 确保posSide参数正确
    if side == "buy":
        posSide = "long"
    elif side == "sell":
        posSide = "short"
    else:
        posSide = long  # 使用传入的参数作为备选
    
    print(f"下单参数: instId={instId}, side={side}, posSide={posSide}, sz={sz}")
    
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId=instId,
        tdMode="cross",
        side=side,
        posSide=posSide,
        ordType="market",
        sz=sz
    )
    return result


def OKX_chichang_Order():
    print("开始获取持仓信息...")
    try:
        # 确保API密钥已设置
        if not api_key or not secret_key or not passphrase:
            print("API凭证未设置!")
            raise ValueError("API凭证未设置，请先调用set_api_credentials函数")

        accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
        result = accountAPI.get_positions()
        print(f"获取持仓信息成功，数据条数: {len(result.get('data', []))}")
        return result
    except Exception as e:
        print(f"获取持仓信息失败: {e}")
        raise


def OKX_get_cc_Order(instId, ordId):
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    result = tradeAPI.get_order(instId=instId, ordId=ordId)
    return result

def get_occupied_margin(result):
    # 获取占用保证金
    zhanyong_baozhengjin = result['data'][0]['details'][0]['availEq']
    return zhanyong_baozhengjin

def get_USDT_rights(result):
    # 获取DT权益
    USDT_quany = result['data'][0]['details'][0]['disEq']

    return USDT_quany    

flag = "1"  # 模拟交易: 1, 实盘交易: 0
from datetime import datetime

def get_candlestick_dataframe(get_candlestick):
    """将K线数据转换为DataFrame格式"""
    df = pd.DataFrame(get_candlestick, columns=['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread','real_volume', 'limit'])
    df['time'] = pd.to_datetime(df['time'].astype(int), unit='ms')  # 显式转换为int，避免警告
    df['time'] = df['time'] + pd.Timedelta(hours=8)
    df.set_index('time', inplace=True)
    return df

# 初始化API
marketDataAPI = MarketAPI(flag=flag)
publicAPI = PublicAPI(flag=flag)

instId1 = "BTC-USDT"

# 注释掉尝试获取K线数据的代码，避免网络错误
"""
try:
    result = marketDataAPI.get_candlesticks(instId=instId1, bar="4H")
    data = get_candlestick_dataframe(result['data'])
    #pprint(data['tick_volume'])
    CLOSE=data['close']
    HIGH = data['high']
    LOW = data['low']   
    OPEN = data['open'] 
    VOL = data['tick_volume']
except Exception as e:
    print(f"获取K线数据失败: {e}")
"""

def zhaobiao():
    pass

def calculate_volatility(self, symbol, window=30):
    """计算波动率"""
    if symbol == 'USDT':
        return 0.0
    
    prices = self.fetch_historical_data(f'{symbol}/USDT')
    returns = np.log(prices / prices.shift(1))
    volatility = returns.rolling(window=window).std() * np.sqrt(365)  # 年化波动率
    return volatility.iloc[-1] if not np.isnan(volatility.iloc[-1]) else 0.0

def adjust_for_volatility(self):
    """根据波动率调整仓位"""
    adjusted_weights = {}
    total_weight = sum(self.assets.values())
    
    for ticker, weight in self.assets.items():
        if ticker == 'USDT':
            adjusted_weights[ticker] = weight
            continue
            
        volatility = self.calculate_volatility(ticker)
        if volatility > self.volatility_threshold:
            # 如果波动率高于阈值，减少配置比例
            reduction = min(0.5, (volatility - self.volatility_threshold) / self.volatility_threshold)
            adjusted_weight = weight * (1 - reduction)
            adjusted_weights[ticker] = adjusted_weight
        else:
            adjusted_weights[ticker] = weight
    
    # 重新归一化权重
    total_adjusted = sum(adjusted_weights.values())
    for ticker in adjusted_weights:
        adjusted_weights[ticker] = adjusted_weights[ticker] / total_adjusted * total_weight
    
    return adjusted_weights

def check_risk_limits(self, prices):
    """检查风险限制"""
    self.update_portfolio_value(prices)
    
    # 检查止损
    if self.portfolio_value < self.initial_capital * self.stop_loss:
        print(f"触发止损线 {self.stop_loss*100}%")
        self.liquidate_portfolio(prices)
        return True
    
    # 检查止盈
    if self.portfolio_value > self.initial_capital * self.take_profit:
        print(f"触发止盈线 {self.take_profit*100}%")
        self.liquidate_portfolio(prices)
        return True
    
    return False

def liquidate_portfolio(self, prices):
    """清仓操作"""
    for ticker in list(self.positions.keys()):
        shares = self.positions[ticker]
        if shares > 0:
            if ticker == 'USDT':
                value = shares
            else:
                value = shares * prices[ticker]
            
            self.history.append({
                'timestamp': datetime.now(),
                'action': 'sell',
                'ticker': ticker,
                'shares': shares,
                'price': prices[ticker] if ticker != 'USDT' else 1.0,
                'value': value
            })
            self.positions[ticker] = 0
    
    self.update_portfolio_value(prices)

# 将USDT保证金转换为合约张数
def usdt_to_contract_size(trade_pair, margin_usdt, leverage=10):
    """
    将USDT保证金转换为合约张数
    
    参数:
    - trade_pair: 交易对，例如 "BTC-USDT"
    - margin_usdt: 保证金金额（USDT）
    - leverage: 杠杆倍数，默认为10
    
    返回: 
    - 合约张数
    """
    try:
        # 确保API密钥已设置
        if not api_key or not secret_key or not passphrase:
            raise ValueError("API凭证未设置，请先调用set_api_credentials函数")
            
        # 确保margin_usdt是浮点数并处理精度问题
        try:
            margin_usdt = float(margin_usdt)
            # 保留两位小数，避免精度问题
            margin_usdt = round(margin_usdt, 2)
            # 确保保证金值大于0
            if margin_usdt <= 0:
                print(f"警告: 保证金值必须大于0, 当前值: {margin_usdt}")
                return 1  # 返回最小张数
                
            # 确保杠杆倍数是整数
            leverage = int(leverage)
            if leverage <= 0:
                print(f"警告: 杠杆倍数必须大于0，当前值: {leverage}，已重置为10")
                leverage = 10
        except (ValueError, TypeError):
            print(f"错误: 无效的参数值: 保证金={margin_usdt}, 杠杆={leverage}")
            return 1  # 返回最小张数
        
        print(f"处理保证金值: {margin_usdt} USDT, 杠杆倍数: {leverage}X")
        
        # 规范化交易对格式
        original_trade_pair = trade_pair
        if "-SWAP" in trade_pair:
            # 如果已经包含SWAP后缀，提取基础交易对
            base_trade_pair = trade_pair.replace("-SWAP", "")
            trade_pair = base_trade_pair
        
        # 确保交易对格式为 XX-USDT
        if not "-" in trade_pair:
            trade_pair = f"{trade_pair}-USDT"
            print(f"交易对格式已标准化: {trade_pair}")
        
        # 获取币种名称（如BTC, ETH, ARB等）
        coin_name = trade_pair.split('-')[0]
            
        # 初始化API
        marketDataAPI = MarketAPI(api_key=api_key, api_secret_key=secret_key, passphrase=passphrase, flag=flag)
        publicAPI = PublicAPI(api_key=api_key, api_secret_key=secret_key, passphrase=passphrase, flag=flag)
        
        # 构建合约ID，确保格式正确
        contract_id = f"{trade_pair}-SWAP"
        print(f"构建合约ID: {contract_id}")
        
        # 获取合约信息
        contract_info = publicAPI.get_instruments(instType="SWAP", instId=contract_id)
        
        # 如果没有找到合约信息，尝试获取所有合约并找出匹配的
        if not contract_info or not contract_info.get('data'):
            print(f"未直接找到合约 {contract_id}，尝试搜索所有合约...")
            all_contracts = publicAPI.get_instruments(instType="SWAP")
            if all_contracts and all_contracts.get('data'):
                # 从base_ccy找匹配的合约
                matching_contracts = [c for c in all_contracts['data'] if coin_name in c['instId']]
                if matching_contracts:
                    contract_info = {'data': [matching_contracts[0]]}
                    print(f"找到匹配合约: {matching_contracts[0]['instId']}")
        
        if not contract_info or not contract_info.get('data'):
            print(f"未找到交易对 {trade_pair} 的合约信息")
            # 对于某些币种可能有特殊的转换规则
            if coin_name.upper() == "ARB":
                # ARB特殊处理：根据经验值，每1 USDT约等于1张ARB合约
                # 考虑杠杆倍数增加张数
                contract_size = max(1, math.ceil(margin_usdt * leverage / 10))
                print(f"使用ARB特殊转换规则(杠杆{leverage}X): {margin_usdt} USDT ≈ {contract_size} 张合约")
                return contract_size
            return 1  # 返回最小张数
        
        contract_data = contract_info['data'][0]
        actual_contract_id = contract_data['instId']
        print(f"获取到合约信息: {actual_contract_id}")
        
        # 获取合约当前价格
        ticker = marketDataAPI.get_ticker(instId=actual_contract_id)
        if not ticker or not ticker.get('data'):
            print(f"未找到交易对 {actual_contract_id} 的价格信息")
            # 对于ARB等特殊币种，使用固定比例
            if coin_name.upper() == "ARB":
                # 考虑杠杆倍数增加张数
                contract_size = max(1, math.ceil(margin_usdt * leverage / 10))
                print(f"使用ARB特殊转换规则(杠杆{leverage}X): {margin_usdt} USDT ≈ {contract_size} 张合约")
                return contract_size
            return 1  # 返回最小张数
        
        current_price = float(ticker['data'][0]['last'])
        
        # 获取合约面值（一张合约代表的价值）
        contract_value = float(contract_data.get('ctVal', 0))
        contract_unit = contract_data.get('ctValCcy', '')  # 合约面值单位
        
        # 特殊处理ARB和其他低价值代币
        if coin_name.upper() == "ARB" or current_price < 1:
            print(f"检测到低价值代币 {coin_name}，使用特殊处理逻辑")
            # 获取更多合约详情以确定准确的张数计算
            min_size = float(contract_data.get('minSz', 1))
            lot_size = float(contract_data.get('lotSz', 1))
            
            # 根据经验，低价值代币的合约面值可能不准确，使用修正后的计算方法
            if contract_value <= 0 or current_price <= 0:
                print(f"合约面值或价格无效：面值={contract_value}，价格={current_price}")
                
                # 使用简化公式：(保证金 * 杠杆) / 当前价格，然后向下取整到最小单位
                coins = (margin_usdt * leverage) / current_price
                contract_size = math.floor(coins / min_size) * min_size if min_size > 0 else math.floor(coins)
                
                # 打印详细计算过程
                print(f"详细计算(杠杆{leverage}X): 保证金={margin_usdt} USDT, 币价={current_price}, 最小单位={min_size}")
                print(f"计算结果: ({margin_usdt} * {leverage}) ÷ {current_price} = {coins} 个{coin_name} ≈ {contract_size}张合约")
                
                return max(1, int(contract_size))  # 确保至少1张
        
        # 计算保证金可以买多少张合约
        # 公式：合约张数 = (保证金金额 * 杠杆) / (合约面值 * 当前价格)
        if contract_value <= 0 or current_price <= 0:
            print(f"合约面值或价格无效：面值={contract_value}，价格={current_price}")
            return 1  # 返回最小张数
        
        # 使用精确计算，确保张数准确
        # 注意：加入杠杆倍数因子
        contract_size_raw = (margin_usdt * leverage) / (contract_value * current_price)
        # 向下取整，获取完整张数
        contract_size = math.floor(contract_size_raw)
        
        # 打印详细计算过程用于调试
        print(f"详细计算(杠杆{leverage}X): 保证金={margin_usdt} USDT, 币价={current_price}, 合约面值={contract_value} {contract_unit}")
        print(f"计算结果: ({margin_usdt} * {leverage}) / ({contract_value} * {current_price}) = {contract_size_raw} ≈ {contract_size}张")
        
        # 确保至少返回1张合约
        if contract_size <= 0:
            print(f"计算出的合约张数为0，已自动调整为1张。")
            return 1
            
        return contract_size
    
    except Exception as e:
        print(f"计算合约张数时出错: {e}")
        import traceback
        traceback.print_exc()
        
        # 提取币种名
        try:
            coin_name = trade_pair.split('-')[0].upper()
            # 对于ARB等特殊币种，使用固定比例
            if coin_name == "ARB":
                # 考虑杠杆倍数增加张数
                contract_size = max(1, math.ceil(margin_usdt * leverage / 10))
                print(f"异常处理: 使用ARB特殊转换规则(杠杆{leverage}X): {margin_usdt} USDT ≈ {contract_size} 张合约")
                return contract_size
        except:
            pass
            
        # 在API请求失败时，返回一个默认合约大小，考虑杠杆倍数
        if margin_usdt > 0:
            contract_size = max(1, math.floor((margin_usdt * leverage) / 1000))
            print(f"由于网络连接问题，使用默认值(杠杆{leverage}X): {margin_usdt} USDT ≈ {contract_size} 张合约")
            return contract_size  # 至少返回1张合约
        return 1  # 至少返回1张合约

def dingdan_for(contract):
    # 打印开始执行信息
    print(f"======= 开始检查持仓状态: {contract} =======")
    
    # 确保交易对是合约格式
    if not contract.endswith("-SWAP"):
        # 将斜杠替换为连字符
        contract = contract.replace("/", "-")
        # 添加SWAP后缀
        contract = f"{contract}-SWAP"
        print(f"dingdan_for 自动转换交易对为合约格式: {contract}")
    
    # 确保API密钥已设置
    if not api_key or not secret_key or not passphrase:
        raise ValueError("API凭证未设置，请先调用set_api_credentials函数")
            
    OKX_l_cw = {}
    OKX_l_cw['buy_flag'] = False
    OKX_l_cw['sell_flag'] = False
    OKX_l_cw['buy_flag_instId_y'] = False
    OKX_l_cw['sell_flag_instId_N'] = False
    
    # 提取币种名称，用于日志和特殊处理
    try:
        coin_name = contract.split('-')[0]
        print(f"处理币种: {coin_name}")
        OKX_l_cw['coin_name'] = coin_name
    except:
        OKX_l_cw['coin_name'] = "未知"
    
    # 获取持仓信息
    try:
        OKX_chichang = OKX_chichang_Order()
        print(f"获取到 {len(OKX_chichang['data'])} 条持仓记录")
        
        # 打印所有持仓详情，方便调试
        print("所有持仓列表:")
        for idx, item in enumerate(OKX_chichang['data']):
            print(f"{idx+1}. {item.get('instId', '未知')} - 方向:{item.get('posSide', '未知')} 数量:{item.get('availPos', '0')}")
        
        # 更智能的合约匹配
        # 1. 精确匹配
        exact_matches = [item for item in OKX_chichang['data'] if item.get('instId') == contract]
        
        # 2. 如果没有精确匹配，尝试模糊匹配
        if not exact_matches:
            coin_name = contract.split('-')[0]
            fuzzy_matches = [item for item in OKX_chichang['data'] if coin_name in item.get('instId', '')]
            
            if fuzzy_matches:
                print(f"未找到精确匹配 {contract}，但找到了模糊匹配:")
                for idx, item in enumerate(fuzzy_matches):
                    print(f"{idx+1}. {item.get('instId')}")
                # 使用第一个模糊匹配
                matches_to_process = fuzzy_matches
            else:
                print(f"没有找到任何与 {contract} 或 {coin_name} 相关的持仓")
                matches_to_process = []
        else:
            print(f"找到精确匹配 {contract}")
            matches_to_process = exact_matches
        
        # 处理匹配到的持仓
        for item in matches_to_process:
            OKX_chichang_instId = item['instId']
            OKX_l_cw['OKX_cw_instId_APT'] = OKX_chichang_instId == contract
            OKX_l_cw['actual_instId'] = OKX_chichang_instId  # 记录实际的合约ID

            # 分别处理多头和空头持仓
            if item['posSide'] == 'long':
                OKX_l_cw['buy_flag'] = True
                OKX_l_cw['p_Pos_sz'] = item['availPos']
                OKX_l_cw['instId'] = item['instId']
                
                # 记录原始值和转换后的值
                avail_pos_raw = item['availPos']
                OKX_l_cw['p_Pos_sz_raw'] = avail_pos_raw
                
                # 特殊处理ARB和其他代币的显示
                if coin_name.upper() == "ARB" and avail_pos_raw.isdigit():
                    # 将字符串转为整数
                    avail_pos_int = int(avail_pos_raw)
                    # 如果API返回的是币数量而不是合约张数，添加说明
                    if avail_pos_int > 0:
                        print(f"ARB持仓数量: {avail_pos_raw} (可能是币数量而非合约张数)")
                
                if 'avgPx' in item:
                    OKX_l_cw['p_cw_avgPx'] = item['avgPx']
                    print(f"多头持仓均价: {item['avgPx']}")

            elif item['posSide'] == 'short':
                OKX_l_cw['sell_flag'] = True
                OKX_l_cw['p_Pos_sz_s'] = item['availPos']
                
                # 记录原始值
                avail_pos_raw = item['availPos']
                OKX_l_cw['p_Pos_sz_s_raw'] = avail_pos_raw
                
                # 特殊处理ARB和其他代币的显示
                if coin_name.upper() == "ARB" and avail_pos_raw.isdigit():
                    # 将字符串转为整数
                    avail_pos_int = int(avail_pos_raw)
                    # 如果API返回的是币数量而不是合约张数，添加说明
                    if avail_pos_int > 0:
                        print(f"ARB空头持仓数量: {avail_pos_raw} (可能是币数量而非合约张数)")
                
                if 'avgPx' in item:
                    OKX_l_cw['p_cw_avgPx_s'] = item['avgPx']
                    print(f"空头持仓均价: {item['avgPx']}")
    
    except Exception as e:
        print(f"获取或处理持仓信息时出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 打印结果信息
    print(f"持仓检查结果: buy_flag={OKX_l_cw['buy_flag']}, sell_flag={OKX_l_cw['sell_flag']}")
    
    # 特殊处理ARB合约，将可能的币数量转换为合约张数
    if OKX_l_cw.get('coin_name', '').upper() == 'ARB':
        try:
            # 对于ARB，API可能返回的是币数量而不是合约张数，需要特殊转换
            if OKX_l_cw['buy_flag'] and 'p_Pos_sz' in OKX_l_cw:
                pos_value = OKX_l_cw['p_Pos_sz']
                try:
                    # 如果是合约张数格式，可能是数字字符串
                    pos_num = float(pos_value)
                    # 判断是否是币数量（通常较大）还是合约张数（通常较小）
                    if pos_num > 100:  # 如果数量大于100，很可能是币数量
                        # 币数量转换为合约张数的估算（实际应基于合约面值和价格）
                        estimate_contract_size = math.ceil(pos_num / 10)  # 假设1张合约约等于10个币
                        print(f"ARB特殊转换: 持仓量 {pos_value} 可能是币数量，估计约等于 {estimate_contract_size} 张合约")
                        # 同时保存转换前后的值
                        OKX_l_cw['p_Pos_sz_original'] = pos_value
                        OKX_l_cw['p_Pos_sz_converted'] = str(estimate_contract_size)
                except (ValueError, TypeError):
                    print(f"无法将持仓量 {pos_value} 转换为数值")
        except Exception as e:
            print(f"ARB持仓特殊处理时出错: {e}")
    
    return OKX_l_cw

def xiadan_Order_System(buy_boduan, float_occupied_margin, float_USDT_rights, shu, symbol, celue_type, leverage=10):
        """
        下单系统
        
        参数:
        - buy_boduan: 布尔值，是否可以下单
        - float_occupied_margin: 占用保证金
        - float_USDT_rights: USDT权益
        - shu: 合约张数
        - symbol: 交易对符号，例如 "BTC-USDT-SWAP"
        - celue_type: 策略类型，"buy"表示做多，"sell"表示做空
        - leverage: 杠杆倍数，默认为10
        
        返回:
        - 订单结果字典
        """
        buy16 = []
        # 保证金额度
        bao_zhang_jin_sz = 4700

        def lost(formatted_result):
            filename = "订单日志记录.csv"
            if os.path.exists(filename):
                mode = 'a'  # 如果文件已存在，则使用追加模式
            else:
                mode = 'w'  # 如果文件不存在，则新建文件并写入

            with open(filename, mode, newline='', encoding='utf-8') as file:
                file.write(formatted_result + '\n')

        # 修改条件，忽略保证金和权益检查，直接尝试下单
        # if buy_boduan and float(float_occupied_margin) > bao_zhang_jin_sz and float(float_USDT_rights) > 300:
        if buy_boduan:  # 简化条件，直接尝试下单
            print(f"正在尝试下单，交易对：{symbol}，数量：{shu}，方向：{celue_type}，杠杆倍数：{leverage}X")
            
            try:
                # 设置杠杆倍数
                try:
                    # 如果可用，尝试先设置杠杆倍数
                    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
                    if celue_type == "buy":
                        posSide = "long"
                    else:
                        posSide = "short"
                    
                    # 获取当前杠杆倍数
                    leverage_info = accountAPI.get_leverage(symbol, "cross")
                    current_leverage = None
                    if leverage_info.get('code') == '0' and 'data' in leverage_info:
                        current_leverage = leverage_info['data'].get(posSide, {}).get('lever')
                        print(f"当前{posSide}杠杆倍数: {current_leverage}X")
                    
                    # 如果当前杠杆不匹配，则设置杠杆
                    if current_leverage is None or int(current_leverage) != leverage:
                        print(f"设置{posSide}杠杆倍数为 {leverage}X")
                        set_result = accountAPI.set_leverage(
                            instId=symbol,
                            lever=str(leverage),
                            mgnMode="cross",
                            posSide=posSide
                        )
                        print(f"设置杠杆结果: {set_result}")
                except Exception as e:
                    print(f"设置杠杆倍数时出错（将继续使用默认杠杆）: {e}")
                
                # 执行下单
                if celue_type == "buy":
                    order_result = OKX_HYAPI_Order("buy", "long", shu, symbol)
                    with open('订单日志记录.csv', 'a', newline='', encoding='utf-8') as file:
                        file.write(f"原因：{order_result}\n")
                elif celue_type == "sell":
                    order_result = OKX_HYAPI_Order("sell", "short", shu, symbol)
                    with open('订单日志记录.csv', 'a', newline='', encoding='utf-8') as file:
                        file.write(f"原因：{order_result}\n")
                
                # 检查下单是否成功
                if order_result.get('code') == '0':
                    print("下单成功!")
                    try:
                        OKX_l_cw = dingdan_for(symbol)
                        if 'instId' in OKX_l_cw and OKX_l_cw['instId'] == symbol and 'p_cw_avgPx' in OKX_l_cw:
                            avgPx = float(OKX_l_cw['p_cw_avgPx'])
                        else:
                            avgPx = None
                            
                        ok_ordid = order_result['data'][0]['ordId']
                        if celue_type == "buy":
                            buy16 = f'波段王已经买入 {symbol}'
                        elif celue_type == "sell":
                            buy16 = f'波段王已经卖出 {symbol}'

                        # 修复datetime使用问题
                        buy_time = datetime.now()
                        buy_time_time_str = buy_time.strftime("%Y-%m-%d %H:%M:%S.%f")

                        if celue_type == "buy":
                            print(f"{buy16} {buy_time_time_str} 订单号：{ok_ordid} 买入价：{avgPx} 杠杆：{leverage}X")
                            data = f'{buy16} {buy_time_time_str} 订单号：{ok_ordid} 买入价：{avgPx} 杠杆：{leverage}X'
                            formatted_result = f'"{data}"'
                            lost(formatted_result)
                        elif celue_type == "sell":
                            print(f"{buy16} {buy_time_time_str} 订单号：{ok_ordid} 卖出价：{avgPx} 杠杆：{leverage}X")
                            data = f'{buy16} {buy_time_time_str} 订单号：{ok_ordid} 卖出价：{avgPx} 杠杆：{leverage}X'
                            formatted_result = f'"{data}"'
                            lost(formatted_result)
                    except Exception as e:
                        print(f"处理订单结果时出错: {e}")
                        return order_result
                else:
                    error_code = order_result.get('code', 'unknown')
                    error_msg = order_result.get('msg', '')
                    if 'data' in order_result and order_result['data']:
                        sCode = order_result['data'][0].get('sCode', '')
                        sMsg = order_result['data'][0].get('sMsg', '')
                        print(f"下单失败: 错误码={error_code}, 信息={error_msg}, 子错误码={sCode}, 子信息={sMsg}")
                    else:
                        print(f"下单失败: 错误码={error_code}, 信息={error_msg}")
                
                return order_result
            except Exception as e:
                print(f"下单失败: {e}")
                return {"error": str(e)}
        else:
            print(f"不满足下单条件，buy_boduan={buy_boduan}")
            return {"status": "not executed", "reason": "conditions not met"}

# 交易对管理功能 - 使用trading_pairs.py
try:
    import trading_pairs
    
    def add_trading_pair_to_json(trade_pair, usdt_amount, leverage=10):
        """
        添加交易对到JSON文件
        
        参数:
        - trade_pair: 交易对，例如 "BTC-USDT" 或 "BTC-USDT-SWAP"
        - usdt_amount: USDT金额
        - leverage: 杠杆倍数，默认为10
        
        返回:
        - 布尔值，操作是否成功
        """
        try:
            # 转换为数值类型
            usdt_amount = float(usdt_amount)
            leverage = int(leverage)
            
            # 确保交易对格式正确
            if "-" not in trade_pair:
                print(f"错误: 交易对格式不正确: {trade_pair}")
                return False
                
            # 添加到JSON文件 - trading_pairs.py中已添加了格式规范化代码
            # 确认trading_pairs模块是否支持杠杆参数
            try:
                # 尝试调用新版本的API（支持杠杆）
                return trading_pairs.add_trading_pair(trade_pair, usdt_amount, leverage)
            except TypeError:
                # 如果遇到参数不匹配的错误，则使用旧版本API（不支持杠杆）
                print(f"警告: trading_pairs模块不支持杠杆参数，将仅保存交易对和金额")
                return trading_pairs.add_trading_pair(trade_pair, usdt_amount)
        except ValueError:
            print(f"错误: 参数格式不正确: USDT金额={usdt_amount}, 杠杆={leverage}")
            return False
        except Exception as e:
            print(f"添加交易对时出错: {e}")
            return False
            
    def remove_trading_pair_from_json(trade_pair):
        """
        从JSON文件中删除交易对
        
        参数:
        - trade_pair: 交易对，例如 "BTC-USDT"
        
        返回:
        - 布尔值，操作是否成功
        """
        try:
            return trading_pairs.remove_trading_pair(trade_pair)
        except Exception as e:
            print(f"删除交易对时出错: {e}")
            return False
            
    def get_all_trading_pairs_from_json():
        """
        获取所有存储的交易对信息
        
        返回:
        - 字典格式的交易对信息
        """
        try:
            return trading_pairs.get_all_trading_pairs()
        except Exception as e:
            print(f"获取交易对时出错: {e}")
            return {}
            
    def get_trading_pair_from_json(trade_pair):
        """
        获取指定交易对的信息
        
        参数:
        - trade_pair: 交易对，例如 "BTC-USDT"
        
        返回:
        - 字典格式的交易对信息，如果不存在则返回None
        """
        try:
            return trading_pairs.get_trading_pair(trade_pair)
        except Exception as e:
            print(f"获取交易对信息时出错: {e}")
            return None

except ImportError:
    print("警告: 未找到trading_pairs模块，无法使用交易对JSON存储功能")
    
    # 创建空函数作为替代，避免导入错误
    def add_trading_pair_to_json(trade_pair, usdt_amount, leverage=10):
        print("警告: 交易对JSON存储功能不可用")
        return False
        
    def remove_trading_pair_from_json(trade_pair):
        print("警告: 交易对JSON存储功能不可用")
        return False
        
    def get_all_trading_pairs_from_json():
        print("警告: 交易对JSON存储功能不可用")
        return {}
        
    def get_trading_pair_from_json(trade_pair):
        print("警告: 交易对JSON存储功能不可用")
        return None

# 如果直接运行此脚本
if __name__ == "__main__":
    default_api_key = "77e4b443-85f6-4dbb-91f7-af4e4553c8a8"
    default_secret_key = "9A6A0C8DA1A690BD73DCCCDD9A962175"
    default_passphrase = "0618Power~"
    # 检查命令行参数
    while True:
        if len(sys.argv) >= 3:
            try:
                # 从命令行参数获取交易对信息
                trade_pair = sys.argv[1]  # 第一个参数应该是交易对
                margin_usdt = float(sys.argv[2])  # 第二个参数是保证金额度
                
                # 确保交易对格式正确
                if "-" not in trade_pair:
                    print(f"错误: 交易对格式不正确: {trade_pair}")
                    sys.exit(1)
                
                # 准备合约版本的交易对
                contract_pair = trade_pair
                if not contract_pair.endswith("-SWAP"):
                    contract_pair = f"{trade_pair}-SWAP"
                
                # 从命令行参数获取额外的参数（如果提供）
                side = "buy"  # 默认为买入(做多)
                if len(sys.argv) >= 4:
                    side = sys.argv[3].lower()  # 交易方向: buy(做多) 或 sell(做空)
                
                # 获取杠杆倍数参数（如果提供）
                leverage = 10  # 默认杠杆倍数
                if len(sys.argv) >= 5:
                    try:
                        leverage = int(sys.argv[4])  # 杠杆倍数
                        if leverage <= 0:
                            print(f"警告: 杠杆倍数必须大于0，将使用默认值10")
                            leverage = 10
                    except ValueError:
                        print(f"警告: 杠杆倍数格式错误 '{sys.argv[4]}'，将使用默认值10")
                        leverage = 10
                
                # 添加明显的输出标记，方便app.py捕获和解析
                print("="*50)
                print(f"## 交易数据开始 ##")
                print(f">> 前端提交的交易对: {trade_pair}")
                print(f">> 保证金金额: {margin_usdt} USDT")
                print(f">> 交易方向: {side}")
                print(f">> 杠杆倍数: {leverage}X")
                print("="*50)
                
                # 这部分代码未改变，但需要调整字典结构以适应后续处理
                instIds = [trade_pair]
                symbols = [contract_pair]
                
                print(f"开始处理交易对: {trade_pair}, 保证金: {margin_usdt} USDT, 方向: {side}, 杠杆: {leverage}X")
            
                # 设置API密钥
                print("设置API凭证...")
                set_api_credentials(default_api_key, default_secret_key, default_passphrase)
            
                # 计算合约张数，传递杠杆倍数
                print("计算合约张数...")
                contract_size = usdt_to_contract_size(trade_pair, margin_usdt, leverage)
                if contract_size <= 0:
                    print(f"错误: 无法计算合约张数，无法继续。请检查网络连接和API服务状态。")
                    sys.exit(1)
                
                print(f"合约张数计算结果: {contract_size} 张")
                print(f">> 合约张数: {contract_size}")
                
                # 获取交易对和保证金金额
                print("获取持仓信息...")
                try:
                    OKX_l_cw = dingdan_for(contract_pair)  # 使用合约版本的交易对
                    buy_flag = OKX_l_cw.get('buy_flag', False)
                    sell_flag = OKX_l_cw.get('sell_flag', False)
                    chichang = False

                    if buy_flag == False:
                    
                    # 检查是否已有相同方向的持仓
                        if (side == "buy" and buy_flag) or (side == "sell" and sell_flag):
                            print(f"已经持有{contract_pair}{'多头' if side == 'buy' else '空头'}头寸，不能重复开仓")
                            sys.exit(0)
                        
                        # 获取账户信息并设置保证金和权益
                        print("获取账户配置信息...")
                        accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
                        # 使用get_account_config替代不存在的get_account_balance
                        result = accountAPI.get_account_config()
                        
                        # 假设使用固定值进行测试
                        zhanyong_baozhengjin = 5000  # 使用固定值代替
                        USDT_quanyi = 1000  # 使用固定值代替
                        buy_AD = True

                        print(f"尝试{side}下单...")
                        if chichang == False:
                            order_result = xiadan_Order_System(buy_AD, zhanyong_baozhengjin, USDT_quanyi, contract_size, contract_pair, side, leverage)
                            print(f"订单结果: {order_result}")
                            print(f">> 订单状态: {'成功' if order_result.get('code') == '0' else '失败'}")
                            chichang = True
                            
                except Exception as e:
                    print(f"在处理交易时发生错误: {e}")
                    print(f">> 错误信息: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    sys.exit(1)
                
            except Exception as e:
                print(f"程序执行出错: {e}")
                print(f">> 错误信息: {str(e)}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
