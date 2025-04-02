from flask import Flask, request, session, render_template, redirect, url_for, jsonify
import time
import subprocess
# from python-okx-master
import pandas as pd
import sys
import requests
import zhibiao

# 初始化市场API（仅在需要时才引用）
try:
    from MarketData import MarketAPI
    from PublicData import PublicAPI
    from pprint import pprint
    import numpy as np
    api_key = "77e4b443-85f6-4dbb-91f7-af4e4553c8a8"
    secret_key = "9A6A0C8DA1A690BD73DCCCDD9A962175"
    passphrase = "0618Power~"
    
    # 设置zhibiao模块的API凭证
    zhibiao.set_api_credentials(api_key, secret_key, passphrase)
    
except ImportError as e:
    print(f"警告：无法导入部分模块: {e}")

# 尝试导入交易对管理模块
try:
    import trading_pairs
except ImportError:
    print("警告: 未找到trading_pairs模块，将使用zhibiao提供的替代函数")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置秘钥用于session

# 测试用户，便于演示
test_users = {
    "13800138000": "123456",
    "13602958586": "abcd8312"  # 添加目标网站的测试账号
}

@app.route('/')
def index():
    if 'user_id' in session:
        # 获取钱包数据以避免'wallet'未定义错误
        wallet_data = get_wallet_data(session.get('user_id', 'default_user'))
        return render_template('dashboard.html', wallet=wallet_data)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取钱包数据，检查燃料情况
    wallet_data = get_wallet_data(session['user_id'])
    return render_template('dashboard.html', wallet=wallet_data)

@app.route('/home')
def home():
    """新的首页路由，"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取钱包数据，检查燃料情况
    wallet_data = get_wallet_data(session['user_id'])
    return render_template('dashboard.html', wallet=wallet_data)

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    invite_code = request.args.get('invite_code', '')
    return render_template('register.html', invite_code=invite_code)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/robot')
def robot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('robot.html')

@app.route('/spot')
def spot():
    """现货交易页面路由"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    trade_type = request.args.get('type', 'spot')
    return render_template('spot.html', trade_type=trade_type)

@app.route('/position/control')
def position_control():
    """仓位控制页面路由"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # 获取交易所ID（如果有的话）
    exchange_id = request.args.get('exchange', 'binance')  # 默认使用binance
    return render_template('position_control.html', exchange=exchange_id)

@app.route('/contract')
def contract():
    """合约交易页面路由 - 为了兼容性，重定向到spot页面并设置类型为contract"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('spot', type='contract'))

@app.route('/strategy')
def strategy():
    """策略页面路由"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('strategy.html')

@app.route('/strategy/settings')
def strategy_settings():
    """策略设置页面路由"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取最新的交易对数据
    trading_pairs = get_usdt_trading_pairs()
    
    # 获取策略ID（如果有的话）
    strategy_id = request.args.get('id', '1')  # 默认使用ID 1
    
    # 在实际应用中，这里会根据ID从数据库获取策略信息
    # 为演示目的，我们使用硬编码的数据
    strategy_info = {
        "id": strategy_id,
        "name": "智能网格策略",  # 默认名称
        "status": "running",
        "run_days": 24,
        "run_hours": 12,
        "total_return": "+45.6%",
        "invested": "$12,345",
        "current_value": "$17,975",
        "risk_level": "低",
        "grid_count": 12,
        "price_range": "$50,000 - $70,000",
        "auto_adjust": True,
        "trade_pair": "BTC-USDT"  # 添加交易对信息
    }
    
    # 根据不同的策略ID设置不同的策略名称和数据
    if strategy_id == '1':
        strategy_info["name"] = "智能网格策略"
    elif strategy_id == '2':
        strategy_info["name"] = "趋势跟踪策略"
        strategy_info["total_return"] = "+32.8%"
        strategy_info["invested"] = "$8,500"
        strategy_info["current_value"] = "$11,288"
        strategy_info["risk_level"] = "中"
        strategy_info["grid_count"] = 8
        strategy_info["price_range"] = "$45,000 - $60,000"
    elif strategy_id == '3':
        strategy_info["name"] = "AI智能预测策略"
        strategy_info["total_return"] = "+62.3%"
        strategy_info["invested"] = "$15,200"
        strategy_info["current_value"] = "$24,670"
        strategy_info["risk_level"] = "高"
        strategy_info["grid_count"] = 16
        strategy_info["price_range"] = "$40,000 - $75,000"
    elif strategy_id == '4':
        strategy_info["name"] = "蓝龙综合策略"
        strategy_info["total_return"] = "+48.7%"
        strategy_info["invested"] = "$18,750"
        strategy_info["current_value"] = "$27,881"
        strategy_info["risk_level"] = "中高"
        strategy_info["grid_count"] = 14
        strategy_info["price_range"] = "$48,000 - $72,000"
    elif strategy_id == '5':
        strategy_info["name"] = "蓝龙出海"
        strategy_info["total_return"] = "+39.5%"
        strategy_info["invested"] = "$10,500"
        strategy_info["current_value"] = "$14,647"
        strategy_info["risk_level"] = "高"
        strategy_info["grid_count"] = 10
        strategy_info["price_range"] = "$42,000 - $65,000"
        strategy_info["trade_pair"] = "ETH-USDT"  # 不同的交易对
    elif strategy_id == '6':
        strategy_info["name"] = "网格量化"
        strategy_info["total_return"] = "+35.8%"
        strategy_info["invested"] = "$14,200"
        strategy_info["current_value"] = "$19,283"
        strategy_info["risk_level"] = "低"
        strategy_info["grid_count"] = 15
        strategy_info["price_range"] = "$52,000 - $68,000"
        strategy_info["trade_pair"] = "SOL-USDT"  # 不同的交易对
    
    # 初始化默认杠杆倍数选项
    default_leverages = [1, 2, 3, 5, 10, 20, 50, 100]
    
    return render_template('strategy_settings.html', strategy=strategy_info, trading_pairs=trading_pairs, default_leverages=default_leverages)

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    # 检查是否是测试用户
    if data and data.get('mobile') and data.get('password'):
        username = data.get('mobile')
        password = data.get('password')
        
        # 检查是否是测试用户
        if username in test_users and test_users[username] == password:
            session['user_id'] = username
            return jsonify({"code": 200, "message": "登录成功"})
            
        # 实际应用中，这里需要进行数据库查询和密码验证
        # 为了演示，我们简化处理
        session['user_id'] = username  # 存储用户ID到session
        return jsonify({"code": 200, "message": "登录成功"})
    return jsonify({"code": 400, "message": "用户名或密码错误"})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    # 检查必要字段
    if not data or not data.get('mobile') or not data.get('password'):
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    # 测试模式: 验证码验证总是通过
    # 实际生产环境中应该验证验证码是否正确
    
    # 这里处理注册逻辑，例如存储到数据库
    # 邀请码是可选的，不做强制检查
    
    # 为演示添加测试用户
    username = data.get('mobile')
    password = data.get('password')
    test_users[username] = password
    
    # 模拟注册成功
    return jsonify({"code": 200, "message": "注册成功"})

@app.route('/api/robots', methods=['GET'])
def api_get_robots():
    # 此处应该从数据库获取机器人列表
    # 为演示目的，返回模拟数据
    robots = [
        {
            "id": 1,
            "name": "客服机器人",
            "description": "专业客服，7x24小时在线",
            "avatar": "bot1.png",
            "status": "online",
            "conversations": 3250,
            "users": 125
        },
        {
            "id": 2,
            "name": "销售助手",
            "description": "智能销售，促进成交",
            "avatar": "bot2.png",
            "status": "online",
            "conversations": 1420,
            "users": 87
        },
        {
            "id": 3,
            "name": "知识百科",
            "description": "知识问答，回答各类问题",
            "avatar": "bot3.png",
            "status": "offline",
            "conversations": 875,
            "users": 56
        }
    ]
    return jsonify({"code": 200, "data": robots})

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    # 此处应该从数据库获取实际统计数据
    # 为演示目的，返回模拟数据
    stats = {
        "robot_count": 5,
        "conversation_today": 128,
        "active_users": 42,
        "knowledge_base_count": 8
    }
    return jsonify({"code": 200, "data": stats})

@app.route('/api/crypto/prices', methods=['GET'])
def api_get_crypto_prices():
    """获取加密货币价格数据"""
    # 为演示目的，返回模拟数据
    crypto_prices = [
        {
            "name": "Bitcoin",
            "symbol": "BTC",
            "price": 63245.87,
            "change": 2.34,
            "volume": "32.5B"
        },
        {
            "name": "Ethereum",
            "symbol": "ETH",
            "price": 3245.65,
            "change": -1.25,
            "volume": "15.8B"
        },
        {
            "name": "BNB",
            "symbol": "BNB",
            "price": 563.24,
            "change": 0.78,
            "volume": "5.2B"
        },
        {
            "name": "Solana",
            "symbol": "SOL",
            "price": 125.43,
            "change": 4.12,
            "volume": "3.7B"
        },
        {
            "name": "Ripple",
            "symbol": "XRP",
            "price": 0.5678,
            "change": -0.45,
            "volume": "2.3B"
        },
        {
            "name": "Cardano",
            "symbol": "ADA",
            "price": 0.4328,
            "change": 1.23,
            "volume": "1.9B"
        }
    ]
    return jsonify({"code": 200, "data": crypto_prices})

@app.route('/api/crypto/contract_data', methods=['GET'])
def api_get_contract_data():
    """获取合约数据API"""
    contract_data = {
        "total_balance": "12450.89",
        "btc_equivalent": "0.19632481",
        "position": "0",
        "available_balance": "12450.89",
        "floating_pnl": "0",
        "recommended_strategies": [
            {
                "name": "蓝龙综合策略",
                "description": "马丁+网格+趋势指标+风险控制综合策略",
                "users": "8104",
                "image": "https://newrobot.mydbc.cn/image/20231229/dc8aba958eda4f373939a06404f1fa52.png"
            },
            {
                "name": "蓝龙出海",
                "description": "根据趋势反向做单",
                "users": "518",
                "image": "https://newrobot.mydbc.cn/image/20231229/dc8aba958eda4f373939a06404f1fa52.png"
            },
            {
                "name": "网格量化",
                "description": "高频小额挂单，捕捉波段收益",
                "users": "12023",
                "image": "https://newrobot.mydbc.cn/image/20231229/dc8aba958eda4f373939a06404f1fa52.png"
            }
        ],
        "pairs": [
            {
                "name": "BTC/USDT永续",
                "price": 68523.21,
                "volume": "3.24亿",
                "change": 2.34
            },
            {
                "name": "ETH/USDT永续",
                "price": 3548.63,
                "volume": "1.83亿",
                "change": 1.89
            },
            {
                "name": "SOL/USDT永续",
                "price": 148.25,
                "volume": "5642万",
                "change": -2.17
            },
            {
                "name": "DOGE/USDT永续",
                "price": 0.1392,
                "volume": "2184万",
                "change": 5.63
            },
            {
                "name": "XRP/USDT永续",
                "price": 0.5721,
                "volume": "1845万",
                "change": -0.82
            }
        ]
    }

    return jsonify({
        "code": 200,
        "message": "success",
        "data": contract_data
    })

@app.route('/wallet', methods=['GET'])
def wallet_page():
    """钱包页面路由"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取钱包数据（实际应用中从数据库获取）
    wallet_data = get_wallet_data(session['user_id'])
    return render_template('wallet.html', wallet=wallet_data)

@app.route('/user/profile', methods=['GET'])
def user_profile():
    """用户个人中心页面路由"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取用户信息（包括钱包数据）
    wallet_data = get_wallet_data(session['user_id'])
    
    # 为个人中心页面准备用户数据
    user_data = {
        "user_id": session['user_id'],
        "username": session['user_id'],  # 这里使用手机号作为用户名
        "avatar": url_for('static', filename='images/avatar-default.svg'),
        "join_date": "2023-01-01",  # 示例数据
        "vip_level": "普通用户",
        "invitation_code": "ABCD123",
        "wallet": wallet_data
    }
    
    return render_template('user_profile.html', user=user_data)

def get_wallet_data(user_id):
    """获取用户钱包数据（模拟）"""
    # 实际应用中，这里应该从数据库获取用户钱包数据
    # 为演示返回模拟数据
    return {
        "total_balance": "15426.89",
        "btc_equivalent": "0.24372481",
        "fuel_balance": "5.00", # 添加燃料余额，设置较低的值触发提示
        "fuel_status": "low", # 燃料状态：low, normal, high
        "assets": [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "amount": "0.18524",
                "value_usd": "11705.32",
                "change": 2.34,
                "balance": 0.18524,
                "usdt_value": 11705.32
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "amount": "1.15",
                "value_usd": "3732.50",
                "change": -1.25,
                "balance": 1.15,
                "usdt_value": 3732.50
            },
            {
                "name": "Binance Coin",
                "symbol": "BNB",
                "amount": "0.25",
                "value_usd": "140.81",
                "change": 0.78,
                "balance": 0.25,
                "usdt_value": 140.81
            },
            {
                "name": "Tether",
                "symbol": "USDT",
                "amount": "452.65",
                "value_usd": "452.65",
                "change": 0.01,
                "balance": 452.65,
                "usdt_value": 452.65
            },
            {
                "name": "Solana",
                "symbol": "SOL",
                "amount": "1.75",
                "value_usd": "185.31",
                "change": 3.25,
                "balance": 1.75,
                "usdt_value": 185.31
            },
            {
                "name": "Dogecoin",
                "symbol": "DOGE",
                "amount": "1250.0",
                "value_usd": "104.38",
                "change": -0.45,
                "balance": 1250.0,
                "usdt_value": 104.38
            }
        ],
        "records": [
            {
                "type": "充值",
                "symbol": "BTC",
                "amount": "+0.05",
                "time": "2023-10-15 15:32:45",
                "status": "已完成"
            },
            {
                "type": "提现",
                "symbol": "ETH",
                "amount": "-0.5",
                "time": "2023-10-10 09:15:22",
                "status": "已完成"
            },
            {
                "type": "划转",
                "symbol": "BTC",
                "amount": "-0.01",
                "time": "2023-10-05 12:42:18",
                "status": "已完成"
            }
        ]
    }

@app.route('/api/wallet', methods=['GET'])
def api_get_wallet():
    """获取钱包数据API"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "未登录"})
    
    # 获取钱包数据
    wallet_data = get_wallet_data(session['user_id'])
    return jsonify({"code": 200, "data": wallet_data})

@app.route('/api/wallet/deposit', methods=['POST'])
def api_wallet_deposit():
    """处理充值请求"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "未登录"})
    
    data = request.json
    if not data or not data.get('amount') or not data.get('currency'):
        return jsonify({"code": 400, "message": "参数错误"})
    
    # 实际应用中，这里处理充值逻辑
    # 为演示返回成功
    return jsonify({
        "code": 200, 
        "message": "充值请求已提交",
        "data": {
            "transaction_id": "TX" + str(int(time.time())),
            "status": "处理中"
        }
    })

@app.route('/api/wallet/withdraw', methods=['POST'])
def api_wallet_withdraw():
    """处理提现请求"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "未登录"})
    
    data = request.json
    if not data or not data.get('amount') or not data.get('currency') or not data.get('address'):
        return jsonify({"code": 400, "message": "参数错误"})
    
    # 实际应用中，这里处理提现逻辑
    # 为演示返回成功
    return jsonify({
        "code": 200, 
        "message": "提现请求已提交",
        "data": {
            "transaction_id": "TX" + str(int(time.time())),
            "status": "处理中"
        }
    })

@app.route('/api/wallet/transfer', methods=['POST'])
def api_wallet_transfer():
    """处理钱包间的转账请求"""
    data = request.json
    if not data:
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    from_wallet = data.get('from_wallet')
    to_wallet = data.get('to_wallet')
    amount = data.get('amount')
    
    if not from_wallet or not to_wallet or not amount:
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    # 在实际应用中，这里会进行转账操作逻辑...
    # 为演示目的，直接返回成功
    time.sleep(1)  # 模拟操作延时
    
    return jsonify({
        "code": 200, 
        "message": "转账成功", 
        "data": {
            "from_wallet": from_wallet,
            "to_wallet": to_wallet,
            "amount": amount,
            "transaction_id": "TX" + str(int(time.time()))
        }
    })

@app.route('/api_auth')
def api_auth():
    """API授权页面路由"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('api_auth.html')

@app.route('/api/exchange/list', methods=['GET'])
def api_exchange_list():
    """获取已绑定的交易所API列表"""
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "请先登录"})
    
    # 在实际应用中，这里会从数据库获取用户绑定的交易所API
    # 为演示目的，返回模拟数据
    
    # 检查是否请求特定交易所
    exchange = request.args.get('exchange')
    
    # 模拟数据
    exchanges = [
        {
            "exchange": "binance",
            "name": "币安 Binance",
            "api_key": "84f9********************",
            "status": "active",
            "bound_time": "2023-10-15 15:32:45",
            "features": ["spot", "futures", "margin"]
        },
        {
            "exchange": "okx",
            "name": "欧易 OKX",
            "api_key": "a12b********************",
            "status": "inactive",
            "bound_time": "2023-09-20 09:15:22",
            "features": ["spot", "futures"]
        }
    ]
    
    # 如果请求特定交易所，则过滤结果
    if exchange:
        exchanges = [e for e in exchanges if e["exchange"] == exchange]
    
    return jsonify({"code": 200, "data": exchanges})

@app.route('/api/exchange/bind', methods=['POST'])
def api_exchange_bind():
    """绑定交易所API"""
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "请先登录"})
    
    data = request.json
    if not data:
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    # 检查必要参数
    exchange = data.get('exchange')
    api_key = data.get('api_key')
    secret_key = data.get('secret_key')
    password = data.get('password')
    
    if not exchange or not api_key or not secret_key or not password:
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    # 在实际应用中，这里会验证API密钥是否有效，并将它们保存到数据库
    # 为演示目的，直接返回成功
    
    # 模拟验证API密钥
    time.sleep(1)  # 模拟处理时间
    
    # 可以添加更多的验证逻辑，例如检查交易密码是否正确
    
    return jsonify({
        "code": 200, 
        "message": "API绑定成功", 
        "data": {
            "exchange": exchange,
            "api_key": api_key[:4] + "********************",
            "status": "active",
            "bound_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "features": ["spot", "futures", "margin"]
        }
    })

@app.route('/api/exchange/unbind', methods=['POST'])
def api_exchange_unbind():
    """解绑交易所API"""
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "请先登录"})
    
    data = request.json
    if not data or not data.get('exchange'):
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    exchange = data.get('exchange')
    
    # 在实际应用中，这里会从数据库中删除对应的API密钥
    # 为演示目的，直接返回成功
    time.sleep(1)  # 模拟处理时间
    
    return jsonify({
        "code": 200, 
        "message": "API解绑成功", 
        "data": {
            "exchange": exchange,
            "unbind_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

# 仓位控制相关API
@app.route('/api/position/data', methods=['GET'])
def api_get_position_data():
    """获取仓位控制数据"""
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "请先登录"})
    
    exchange = request.args.get('exchange', 'binance')
    
    # 在实际应用中，这里会从数据库获取用户特定交易所的仓位设置
    # 为演示目的，返回模拟数据
    position_data = {
        "exchange": exchange,
        "available_balance": "1258.4567",
        "total_allowed": "5000.0000",
        "used_amount": "756.3456",
        "remaining_amount": "4243.6544",
        "short_position_limit": 8,
        "long_position_limit": 12
    }
    
    return jsonify({"code": 200, "data": position_data})

@app.route('/api/position/update', methods=['POST'])
def api_update_position_settings():
    """更新仓位控制设置"""
    if 'user_id' not in session:
        return jsonify({"code": 401, "message": "请先登录"})
    
    data = request.json
    if not data:
        return jsonify({"code": 400, "message": "缺少必要信息"})
    
    exchange = data.get('exchange', 'binance')
    total_allowed = data.get('total_allowed')
    short_position_limit = data.get('short_position_limit')
    long_position_limit = data.get('long_position_limit')
    
    if total_allowed is None:
        return jsonify({"code": 400, "message": "缺少必要信息：允许量化总U数"})
    
    # 在实际应用中，这里会更新数据库中的用户仓位设置
    # 为演示目的，直接返回成功
    time.sleep(1)  # 模拟操作延时
    
    # 计算剩余可用数量（示例）
    used_amount = 756.3456  # 假设已使用
    remaining_amount = float(total_allowed) - used_amount
    
    return jsonify({
        "code": 200, 
        "message": "设置更新成功", 
        "data": {
            "exchange": exchange,
            "total_allowed": total_allowed,
            "used_amount": str(used_amount),
            "remaining_amount": str(remaining_amount),
            "short_position_limit": short_position_limit,
            "long_position_limit": long_position_limit
        }
    })

@app.route('/api/strategy/save', methods=['POST'])
def save_strategy():
    """处理策略保存请求"""
    # 获取请求数据
    data = request.json
    
    if not data:
        return jsonify({"code": 400, "message": "请求数据无效"})
    
    strategy_id = data.get('strategyId', '1')
    margin_value = data.get('marginValue', '0')
    trade_pair = data.get('tradePair', 'BTC-USDT')
    trade_direction = data.get('tradeDirection', 'buy')  # 获取交易方向，默认为buy(做多)
    leverage = data.get('leverage', 10)  # 获取杠杆倍数，默认为10
    
    # 将数据转换为合适的格式
    try:
        margin_value = float(margin_value)
        # 解决浮点数精度问题：将margin_value保留到2位小数，避免精度丢失
        margin_value = round(margin_value, 2)
        
        # 确保杠杆倍数是整数
        leverage = int(leverage)
    except ValueError:
        return jsonify({"code": 400, "message": "数值格式错误"})
    
    # 确保最小保证金值
    if margin_value <= 0:
        return jsonify({"code": 400, "message": "保证金必须大于0"})
    
    # 记录实际传递的保证金值和杠杆倍数，便于调试
    app.logger.info(f"处理保证金值: {margin_value} USDT (类型: {type(margin_value)}), 杠杆倍数: {leverage}X")
    
    # 规范化交易对格式
    # 如果交易对不包含SWAP后缀，确保添加它用于合约交易
    original_trade_pair = trade_pair  # 保存原始交易对，用于记录
    if not trade_pair.endswith("-SWAP"):
        # 先去掉可能的SWAP后缀，再添加，确保格式一致
        base_pair = trade_pair.replace("-SWAP", "")
        trade_pair_with_swap = f"{base_pair}-SWAP"
        app.logger.info(f"规范化交易对格式: {trade_pair} -> {trade_pair_with_swap}")
        # 更新trade_pair为带SWAP后缀的版本
        trade_pair = trade_pair_with_swap
    
    # 提取币种名称，用于日志和特殊处理
    coin_name = trade_pair.split('-')[0] if '-' in trade_pair else trade_pair
    app.logger.info(f"处理币种: {coin_name}")
    
    # 保存交易对到JSON文件 - 使用规范化后的交易对
    try:
        # 更新: 添加保存杠杆倍数参数
        save_result = zhibiao.add_trading_pair_to_json(trade_pair, margin_value, leverage)
        if save_result:
            print(f"交易对 {trade_pair} 已成功保存到JSON文件")
        else:
            print(f"保存交易对 {trade_pair} 到JSON文件失败")
    except Exception as e:
        print(f"保存交易对时出错: {e}")
    
    # 在终端打印信息，使用我们设计的标记格式
    print("="*50)
    print(f"## 交易数据开始 ##")
    print(f">> 前端提交的交易对: {original_trade_pair}")
    print(f">> 规范化后的交易对: {trade_pair}")
    print(f">> 保证金金额: {margin_value} USDT")
    print(f">> 交易方向: {trade_direction}")
    print(f">> 杠杆倍数: {leverage}X")
    print(f">> 币种名称: {coin_name}")

    # 保留原始输出格式以便向后兼容
    print(f"交易对: {trade_pair}, 保证金: {margin_value} USDT, 方向: {trade_direction}, 杠杆: {leverage}X")
    
    try:
        # 直接调用zhibiao模块中的函数进行计算 - 使用规范化后的交易对
        # 更新: 传递杠杆倍数参数给contract_size计算函数
        contract_size = zhibiao.usdt_to_contract_size(trade_pair, margin_value, leverage)
        
        # 创建交易信息字典，像subprocess方法一样收集信息
        trade_info = {
            '前端提交的交易对': original_trade_pair,
            '规范化后的交易对': trade_pair,
            '保证金金额': f"{margin_value} USDT",
            '交易方向': trade_direction,
            '杠杆倍数': f"{leverage}X",
            '合约张数': str(contract_size),
            '币种名称': coin_name
        }
        
        # 获取当前持仓状态 - 添加这部分代码，使用规范化后的交易对
        try:
            position_status = zhibiao.dingdan_for(trade_pair)
            buy_flag = position_status.get('buy_flag', False)
            sell_flag = position_status.get('sell_flag', False)
        except Exception as pos_err:
            app.logger.error(f"获取持仓状态失败: {pos_err}")
            buy_flag = False
            sell_flag = False
        
        # 尝试获取订单结果
        order_result = None
        try:
            # 调用下单函数，传递必要的参数
            # 获取账户配置信息（假设已设置）
            # 使用固定值进行测试
            zhanyong_baozhengjin = 5000  # 使用固定值代替
            USDT_quanyi = 1000  # 使用固定值代替
            buy_AD = True
            
            # 更新: 传递杠杆倍数参数给下单函数
            order_result = zhibiao.xiadan_Order_System(buy_AD, zhanyong_baozhengjin, USDT_quanyi, contract_size, trade_pair, trade_direction, leverage)
            
            # 更新交易信息中的订单状态
            trade_info['订单状态'] = '成功' if order_result.get('code') == '0' else '失败'
            
            # 检查下单是否成功
            if order_result.get('code') == '0' or order_result.get('data', [{}])[0].get('sCode') == '0':
                print(f"订单结果: {order_result}")
                # 将订单结果转换为可读格式
                formatted_result = {
                    "orderId": order_result.get('data', [{}])[0].get('ordId', '未知'),
                    "status": "成功",
                    "exchangeId": "OKX",
                    "direction": "做多" if trade_direction == "buy" else "做空",
                    "contractSize": contract_size,
                    "margin": f"{margin_value} USDT",
                    "leverage": f"{leverage}X",  # 添加杠杆倍数信息
                    "tradePair": trade_pair,  # 使用规范化的交易对
                    "originalTradePair": original_trade_pair,  # 保存原始交易对
                    "coinName": coin_name,
                    "time": time.strftime("%Y-%m-%d %H:%M:%S")
                }               
                
                # 返回成功响应，并包含订单结果和合约张数
                return jsonify({
                    "code": 200, 
                    "message": "下单成功！", 
                    "contractSize": contract_size,
                    "orderResult": formatted_result,
                    "positionStatus": {
                        "buy_flag": buy_flag,
                        "sell_flag": sell_flag
                    },
                    "tradeInfo": trade_info,  # 添加交易信息到返回值
                })
            else:
                # 订单失败，返回错误信息
                error_code = order_result.get('code', 'unknown')
                error_msg = order_result.get('msg', '')
                if 'data' in order_result and order_result['data']:
                    sCode = order_result['data'][0].get('sCode', '')
                    sMsg = order_result['data'][0].get('sMsg', '')
                    error_detail = f"错误码={error_code}, 信息={error_msg}, 子错误码={sCode}, 子信息={sMsg}"
                else:
                    error_detail = f"错误码={error_code}, 信息={error_msg}"
                
                return jsonify({
                    "code": 400, 
                    "message": f"下单失败: {error_detail}", 
                    "contractSize": contract_size,
                    "tradeInfo": trade_info,  # 添加交易信息到返回值
                })
                
        except requests.exceptions.RequestException as req_err:
            # 捕获网络请求异常
            app.logger.error(f"网络请求失败: {req_err}")
            return jsonify({
                "code": 503, 
                "message": "网络连接失败，请检查您的网络设置",
                "contractSize": contract_size,
                "tradeInfo": trade_info,  # 添加交易信息到返回值
            })
        except TimeoutError:
            # 捕获超时异常
            app.logger.error("请求超时")
            return jsonify({
                "code": 504, 
                "message": "请求超时，请稍后再试",
                "contractSize": contract_size,
                "tradeInfo": trade_info,  # 添加交易信息到返回值
            })
        
    except requests.exceptions.RequestException as e:
        # 网络错误处理
        app.logger.error(f"网络请求失败: {e}")
        return jsonify({
            "code": 503, 
            "message": "网络连接失败，请检查您的网络设置",
        })
    except Exception as e:
        app.logger.error(f"处理策略保存请求时出错: {e}")
        import traceback
        traceback.print_exc()
        
        # 尝试使用subprocess作为备用方法
        try:
            # 构造命令并执行，将交易对、保证金值、交易方向和杠杆倍数传递给脚本
            cmd = ["python", "zhibiao.py", trade_pair, str(margin_value), trade_direction, str(leverage)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 获取脚本输出
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            # 检查是否有错误
            if result.returncode != 0:
                app.logger.error(f"zhibiao.py执行错误: {stderr}")
                return jsonify({"code": 500, "message": f"脚本执行错误: {stderr}"})
            
            # 解析特殊标记的输出信息
            trade_info = {}
            for line in stdout.split('\n'):
                if line.startswith('>>'):
                    parts = line[3:].split(':', 1)  # 去掉'>> '前缀并分割
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        trade_info[key] = value
            
            # 输出解析结果，帮助调试
            app.logger.info(f"解析到的交易信息: {trade_info}")
            
            # 为确保前端始终能看到交易对信息，添加一个检查
            if '前端提交的交易对' not in trade_info:
                trade_info['前端提交的交易对'] = trade_pair
                
            if '保证金金额' not in trade_info:
                trade_info['保证金金额'] = f"{margin_value} USDT"
                
            if '交易方向' not in trade_info:
                trade_info['交易方向'] = trade_direction
                
            if '杠杆倍数' not in trade_info:
                trade_info['杠杆倍数'] = f"{leverage}X"
                
            # 打印解析后的交易信息，帮助查看接收到的信息
            app.logger.info(f"最终交易信息: 交易对={trade_info.get('前端提交的交易对')}, 保证金={trade_info.get('保证金金额')}")
            
            # 尝试解析输出中的张数信息
            contract_size = 0  # 默认值
            if '合约张数' in trade_info:
                try:
                    contract_size = int(trade_info['合约张数'])
                except (ValueError, TypeError):
                    app.logger.error(f"解析合约张数失败: {trade_info.get('合约张数')}")
            else:
                # 原有的解析方式作为备用
                for line in stdout.split('\n'):
                    if '张' in line:
                        try:
                            # 提取张数的数字部分
                            contract_size = int(line.split('张')[0].strip().split()[-1])
                        except Exception as e:
                            app.logger.error(f"解析张数失败: {e}")
            
            # 判断是否下单成功
            order_success = False
            order_info = {}
            
            # 先检查新格式中是否有成功标识
            if trade_info.get('订单状态') == '成功':
                order_success = True
            else:
                # 原有的检测方式作为备用
                for line in stdout.split('\n'):
                    if '已经买入' in line or '已经卖出' in line:
                        order_success = True
                        break
            
            # 如果下单成功，构建订单信息
            if order_success:
                # 尝试从新格式中提取信息
                try:
                    # 尝试解析订单详情行
                    parts = []
                    for line in stdout.split('\n'):
                        if '已经买入' in line or '已经卖出' in line:
                            parts = line.split()
                            break
                    
                    order_id = [p for p in parts if p.startswith('订单号：')]
                    order_id = order_id[0].replace('订单号：', '') if order_id else '未知'
                    price = [p for p in parts if p.startswith('买入价：') or p.startswith('卖出价：')]
                    price = price[0].split('：')[1] if price else '未知'
                    
                    order_info = {
                        "orderId": order_id,
                        "status": "成功",
                        "exchangeId": "OKX",
                        "direction": "做多" if trade_direction == "buy" else "做空",
                        "contractSize": contract_size,
                        "margin": f"{margin_value} USDT",
                        "leverage": f"{leverage}X",
                        "tradePair": trade_info.get('前端提交的交易对', trade_pair),
                        "price": price,
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "coinName": coin_name
                    }
                    
                        
                except Exception as e:
                    app.logger.error(f"解析订单信息失败: {e}")
                    # 设置默认订单信息
                    order_info = {
                        "orderId": "未知",
                        "status": "成功",
                        "exchangeId": "OKX",
                        "direction": "做多" if trade_direction == "buy" else "做空",
                        "contractSize": contract_size,
                        "margin": f"{margin_value} USDT",
                        "leverage": f"{leverage}X",
                        "tradePair": trade_info.get('前端提交的交易对', trade_pair),
                        "price": "未知",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "coinName": coin_name
                    }
                    
            
            # 返回成功响应及合约张数
            if order_success:
                return jsonify({
                    "code": 200, 
                    "message": "下单成功！", 
                    "contractSize": contract_size,
                    "orderResult": order_info,
                    "positionStatus": {
                        "buy_flag": buy_flag,
                        "sell_flag": sell_flag
                    },
                    "tradeInfo": trade_info,  # 添加解析出的交易信息

                })
            else:
                return jsonify({
                    "code": 200, 
                    "message": "设置已保存",
                    "contractSize": contract_size,
                    "positionStatus": {
                        "buy_flag": buy_flag,
                        "sell_flag": sell_flag
                    },
                    "tradeInfo": trade_info,  # 添加解析出的交易信息

                })
        except Exception as sub_e:
            app.logger.error(f"使用子进程执行脚本时出错: {sub_e}")
            return jsonify({
                "code": 500, 
                "message": f"服务器错误: {str(sub_e)}",
            })

@app.route('/api/position/check', methods=['POST'])
def check_position_status():
    """检查某个交易对的持仓状态"""
    data = request.json
    if not data:
        return jsonify({"code": 400, "message": "请求数据无效"})
    
    trade_pair = data.get('tradePair', 'BTC-USDT')
    trade_direction = data.get('tradeDirection', 'buy')
    
    # 添加控制台输出，表明策略状态检查被调用
    print(f"[策略状态检查] 交易对: {trade_pair}, 交易方向: {trade_direction}, 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 检查是否请求所有持仓数据
        if trade_pair == 'ALL':
            # 直接返回OKX_chichang_Order()获取的所有持仓数据
            all_positions = zhibiao.OKX_chichang_Order()
            position_count = len(all_positions.get('data', []))
            print(f"[持仓查询] 获取所有持仓，总数: {position_count}")
            
            # 直接返回所有持仓数据
            return jsonify({
                "code": 200,
                "positionStatus": all_positions,
                "hasOrder": position_count > 0,
                "statusSummary": f"已激活 - 共{position_count}个持仓" if position_count > 0 else "未激活"
            })
        
        # 规范化交易对格式，确保使用-SWAP后缀
        original_trade_pair = trade_pair  # 保存原始值
        if not trade_pair.endswith("-SWAP"):
            # 先去掉可能的SWAP后缀，再添加，确保格式一致
            base_pair = trade_pair.replace("-SWAP", "")
            trade_pair = f"{base_pair}-SWAP"
            print(f"[策略状态检查] 规范化交易对格式: {original_trade_pair} -> {trade_pair}")
        
        # 获取单个交易对的持仓状态，使用规范化后的交易对
        position_status = zhibiao.dingdan_for(trade_pair)
        buy_flag = position_status.get('buy_flag', False)
        sell_flag = position_status.get('sell_flag', False)
        
        # 输出持仓状态
        print(f"[策略状态结果] 交易对: {trade_pair}, 多头持仓: {'激活' if buy_flag else '未激活'}, 空头持仓: {'激活' if sell_flag else '未激活'}")
        
        # 检查是否有持仓，并设置状态摘要
        has_order = buy_flag or sell_flag
        
        status_result = "未激活"
        if buy_flag or sell_flag:
            status_result = f"已激活 - 持有{'多头' if buy_flag else ''}{'空头' if sell_flag else ''}"
            
        print(f"[策略状态总结] {status_result}")
        
        # 添加原始交易对和规范化后的交易对到响应中
        position_status['originalTradePair'] = original_trade_pair
        position_status['normalizedTradePair'] = trade_pair
        
        return jsonify({
            "code": 200,
            "positionStatus": position_status,  # 直接返回完整的持仓状态
            "hasOrder": has_order,
            "statusSummary": status_result  # 添加状态摘要到响应
        })
        
    except Exception as e:
        app.logger.error(f"检查持仓状态时出错: {e}")
        print(f"[策略状态严重错误] {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}"
        })

@app.route('/api/position/count', methods=['GET'])
def get_position_count():
    """获取当前OKX持仓数量的简单API"""
    try:
        # 直接调用OKX_chichang_Order获取所有持仓
        all_positions = zhibiao.OKX_chichang_Order()
        position_count = len(all_positions.get('data', []))
        
        # 显示持仓数量信息
        print(f"[持仓计数API] 当前持仓总数: {position_count}")
        
        # 返回简单的数量信息
        return jsonify({
            "code": 200,
            "position_count": position_count,
            "timestamp": int(time.time())
        })
        
    except Exception as e:
        app.logger.error(f"获取持仓数量时出错: {e}")
        print(f"[持仓计数API错误] {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}",
            "position_count": 0
        })

def get_usdt_trading_pairs():
    """获取OKX所有USDT结算的合约交易对"""
    try:
        from PublicData import PublicAPI
        
        # 初始化API，使用模拟交易模式
        flag = "1"  # 模拟交易: 1, 实盘交易: 0
        api = PublicAPI(flag=flag)
        
        # 获取所有SWAP合约交易对信息
        result = api.get_instruments(instType="SWAP")
        
        if result.get('code') == '0' and 'data' in result:
            # 提取交易对ID并过滤出USDT结算的交易对
            all_pairs = [item['instId'] for item in result['data']]
            usdt_pairs = [pair for pair in all_pairs if pair.endswith("-USDT-SWAP")]
            
            # 格式化为显示格式 (例如: BTC-USDT-SWAP -> BTC/USDT)
            formatted_pairs = []
            for pair in usdt_pairs:
                parts = pair.split("-")
                if len(parts) >= 2:
                    symbol = parts[0]
                    quote = parts[1]
                    formatted_pairs.append({
                        "symbol": symbol,
                        "display": f"{symbol}/{quote}",
                        "original": pair,
                        "icon_url": f"https://ai.hkd.red/symbolImage/{symbol}.png"
                    })
            
            return formatted_pairs
        else:
            print("获取交易对失败:", result.get('msg', 'Unknown error'))
            return []
    except Exception as e:
        import traceback
        print(f"获取交易对时出错: {e}")
        traceback.print_exc()
        
        # 如果API调用失败，使用硬编码的列表作为备份
        backup_pairs = [
            "BTC-USDT-SWAP", "ETH-USDT-SWAP", "LTC-USDT-SWAP", "BCH-USDT-SWAP", 
            "DOGE-USDT-SWAP", "SOL-USDT-SWAP", "XRP-USDT-SWAP", "1INCH-USDT-SWAP"
            # ... 其他交易对 ...
        ]
        
        formatted_pairs = []
        for pair in backup_pairs:
            parts = pair.split("-")
            if len(parts) >= 2:
                symbol = parts[0]
                quote = parts[1]
                formatted_pairs.append({
                    "symbol": symbol,
                    "display": f"{symbol}/{quote}",
                    "original": pair,
                    "icon_url": f"https://ai.hkd.red/symbolImage/{symbol}.png"
                })
        
        return formatted_pairs

# 交易对管理API路由
@app.route('/api/trading_pairs/list', methods=['GET'])
def list_trading_pairs():
    """获取所有保存的交易对信息"""
    try:
        trading_pairs_data = zhibiao.get_all_trading_pairs_from_json()
        
        # 转换为前端友好的格式
        result = []
        for pair, info in trading_pairs_data.items():
            result.append({
                "tradePair": pair,
                "amount": info["amount"],
                "timestamp": info["timestamp"],
                "formattedTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info["timestamp"]))
            })
            
        return jsonify({
            "code": 200,
            "message": "获取交易对列表成功",
            "data": result
        })
    except Exception as e:
        print(f"获取交易对列表时出错: {e}")
        return jsonify({
            "code": 500,
            "message": f"获取交易对列表失败: {str(e)}",
            "data": []
        })

@app.route('/api/trading_pairs/delete', methods=['POST'])
def delete_trading_pair():
    """删除指定的交易对"""
    data = request.json
    
    if not data or 'tradePair' not in data:
        return jsonify({
            "code": 400,
            "message": "请求数据无效，缺少交易对信息"
        })
    
    trade_pair = data['tradePair']
    
    try:
        # 删除交易对
        result = zhibiao.remove_trading_pair_from_json(trade_pair)
        
        if result:
            return jsonify({
                "code": 200,
                "message": f"成功删除交易对 {trade_pair}"
            })
        else:
            return jsonify({
                "code": 400,
                "message": f"删除交易对 {trade_pair} 失败"
            })
    except Exception as e:
        print(f"删除交易对时出错: {e}")
        return jsonify({
            "code": 500,
            "message": f"删除交易对时发生错误: {str(e)}"
        })

# 添加新的API端点，用于获取交易对可用杠杆倍数
@app.route('/api/trading/leverage', methods=['GET'])
def get_leverage_options():
    """获取指定交易对可用的杠杆倍数选项"""
    # 获取交易对参数
    trade_pair = request.args.get('trade_pair', 'BTC-USDT-SWAP')
    
    try:
        # 确保交易对格式正确
        if not trade_pair.endswith("-SWAP"):
            # 为合约交易添加SWAP后缀
            base_pair = trade_pair.replace("-SWAP", "")
            trade_pair = f"{base_pair}-SWAP"
            print(f"[获取杠杆] 规范化交易对格式: {request.args.get('trade_pair')} -> {trade_pair}")
        
        # 实例化Account API
        import Account
        accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
        
        # 获取杠杆信息
        result = accountAPI.get_leverage(trade_pair, "cross")
        
        if result.get('code') == '0' and 'data' in result:
            # 从响应中提取最大杠杆倍数
            # OKX API返回的data结构通常包含long和short两种仓位的杠杆信息
            leverage_data = result['data']
            
            # 获取多头和空头的杠杆倍数
            long_leverage = int(leverage_data.get('long', {}).get('lever', '10'))
            short_leverage = int(leverage_data.get('short', {}).get('lever', '10'))
            max_leverage = int(leverage_data.get('maxLever', '100'))
            
            print(f"[获取杠杆] 交易对: {trade_pair}, 多头杠杆: {long_leverage}, 空头杠杆: {short_leverage}, 最大杠杆: {max_leverage}")
            
            # 根据最大杠杆倍数生成推荐的杠杆级别
            if max_leverage >= 100:
                leverage_options = [1, 2, 3, 5, 10, 20, 50, 75, 100]
            elif max_leverage >= 50:
                leverage_options = [1, 2, 3, 5, 10, 20, 30, 50]
            elif max_leverage >= 20:
                leverage_options = [1, 2, 3, 5, 10, 15, 20]
            elif max_leverage >= 10:
                leverage_options = [1, 2, 3, 5, 8, 10]
            elif max_leverage >= 5:
                leverage_options = [1, 2, 3, 5]
            else:
                leverage_options = [1, 2, 3]
            
            # 确保不超过最大杠杆值
            leverage_options = [lev for lev in leverage_options if lev <= max_leverage]
            
            # 返回杠杆倍数选项
            return jsonify({
                "code": 200,
                "message": "获取杠杆倍数成功",
                "data": {
                    "trade_pair": trade_pair,
                    "long_leverage": long_leverage,
                    "short_leverage": short_leverage,
                    "max_leverage": max_leverage,
                    "leverage_options": leverage_options,
                    "current_leverage": long_leverage  # 默认使用多头杠杆值作为当前值
                }
            })
        else:
            # 处理API返回错误
            error_msg = result.get('msg', '未知错误')
            print(f"[获取杠杆] 获取交易对杠杆数据失败: {error_msg}")
            
            # 返回默认杠杆倍数选项
            return jsonify({
                "code": 400,
                "message": f"获取杠杆倍数失败: {error_msg}",
                "data": {
                    "trade_pair": trade_pair,
                    "leverage_options": [1, 2, 3, 5, 10, 20, 50, 100],
                    "current_leverage": 10  # 默认值
                }
            })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[获取杠杆] 系统错误: {str(e)}")
        
        # 返回默认杠杆倍数选项
        return jsonify({
            "code": 500,
            "message": f"系统错误: {str(e)}",
            "data": {
                "trade_pair": trade_pair,
                "leverage_options": [1, 2, 3, 5, 10, 20, 50, 100],
                "current_leverage": 10  # 默认值
            }
        })

if __name__ == '__main__':
    # 确保应用监听所有IP地址，同时设置适当的处理器
    app.config['SESSION_COOKIE_DOMAIN'] = None  # 允许所有域名共享session
    app.config['SESSION_COOKIE_PATH'] = '/'     # 设置cookie路径为根路径
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # 允许同站点cookie传递
    app.run(host="0.0.0.0", port=5678, debug=True)
