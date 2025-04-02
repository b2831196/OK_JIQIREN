"""
此脚本用于解析和输出OKX交易所的合约交易对列表。
"""

# 硬编码交易对列表（从之前API调用结果手动提取）
trading_pairs = [
    "BTC-USD-SWAP", "ETH-USD-SWAP", "LTC-USD-SWAP", "BCH-USD-SWAP", 
    "DOGE-USD-SWAP", "SOL-USD-SWAP", "1INCH-USD-SWAP", "ADA-USD-SWAP", 
    "ALGO-USD-SWAP", "ATOM-USD-SWAP", "AVAX-USD-SWAP", "BSV-USD-SWAP", 
    "CRV-USD-SWAP", "DOT-USD-SWAP", "EOS-USD-SWAP", "ETC-USD-SWAP", 
    "FIL-USD-SWAP", "GRT-USD-SWAP", "LINK-USD-SWAP", "NEO-USD-SWAP", 
    "SUI-USD-SWAP", "SUSHI-USD-SWAP", "TRX-USD-SWAP", "UNI-USD-SWAP", 
    "XLM-USD-SWAP", "YFI-USD-SWAP", 
    "BTC-USDT-SWAP", "ETH-USDT-SWAP", "LTC-USDT-SWAP", "BCH-USDT-SWAP", 
    "DOGE-USDT-SWAP", "SOL-USDT-SWAP", "XRP-USDT-SWAP", "1INCH-USDT-SWAP", 
    "AAVE-USDT-SWAP", "ACT-USDT-SWAP", "ADA-USDT-SWAP", "AI16Z-USDT-SWAP", 
    "AIDOGE-USDT-SWAP", "ALGO-USDT-SWAP", "ARB-USDT-SWAP", "ATOM-USDT-SWAP", 
    "AUCTION-USDT-SWAP", "AVAX-USDT-SWAP", "AXS-USDT-SWAP", "BAL-USDT-SWAP", 
    "BAND-USDT-SWAP", "BNB-USDT-SWAP", "BNT-USDT-SWAP", "BOME-USDT-SWAP", 
    "BRETT-USDT-SWAP", "CATI-USDT-SWAP", "CAT-USDT-SWAP", "CELO-USDT-SWAP", 
    "CETUS-USDT-SWAP", "CFX-USDT-SWAP", "COMP-USDT-SWAP", "CRO-USDT-SWAP", 
    "CRV-USDT-SWAP", "DOGS-USDT-SWAP", "DOT-USDT-SWAP", "EOS-USDT-SWAP", 
    "ETC-USDT-SWAP", "ETHW-USDT-SWAP", "ETHFI-USDT-SWAP", "FIL-USDT-SWAP", 
    "FLOKI-USDT-SWAP", "FLOW-USDT-SWAP", "GMT-USDT-SWAP", "HBAR-USDT-SWAP", 
    "HMSTR-USDT-SWAP", "ICP-USDT-SWAP", "ID-USDT-SWAP", "IMX-USDT-SWAP", 
    "INJ-USDT-SWAP", "IOTA-USDT-SWAP", "KAITO-USDT-SWAP", "KISHU-USDT-SWAP", 
    "KNC-USDT-SWAP", "KSM-USDT-SWAP", "LDO-USDT-SWAP", "LINK-USDT-SWAP", 
    "LPT-USDT-SWAP", "LQTY-USDT-SWAP", "LRC-USDT-SWAP", "MAGIC-USDT-SWAP", 
    "MAJOR-USDT-SWAP", "MASK-USDT-SWAP", "MAX-USDT-SWAP", "MINA-USDT-SWAP", 
    "MKR-USDT-SWAP", "MSN-USDT-SWAP", "NC-USDT-SWAP", "NEAR-USDT-SWAP", 
    "NEO-USDT-SWAP", "NOT-USDT-SWAP", "OP-USDT-SWAP", "ORBS-USDT-SWAP", 
    "PENGU-USDT-SWAP", "PEPE-USDT-SWAP", "POL-USDT-SWAP", "QTUM-USDT-SWAP", 
    "RENOLD-USDT-SWAP", "RON-USDT-SWAP", "SAND-USDT-SWAP", "SATS-USDT-SWAP", 
    "SCR-USDT-SWAP", "SHELL-USDT-SWAP", "SHIB-USDT-SWAP", "SUI-USDT-SWAP", 
    "SUSHI-USDT-SWAP", "THETA-USDT-SWAP", "TRX-USDT-SWAP", "UNI-USDT-SWAP", 
    "USDC-USDT-SWAP", "VRA-USDT-SWAP", "X-USDT-SWAP", "XLM-USDT-SWAP", 
    "XTZ-USDT-SWAP", "YFI-USDT-SWAP", "YGG-USDT-SWAP", "ZETA-USDT-SWAP", 
    "ZIL-USDT-SWAP", "BTC-USDC-SWAP", "ETH-USDC-SWAP", "ME-USDC-SWAP", 
    "MOODENG-USDC-SWAP", "NC-USDC-SWAP"
]

# 打印所有交易对
print(f"OKX合约交易对列表 (总计: {len(trading_pairs)} 个):")
for i, pair in enumerate(trading_pairs, 1):
    print(f"{i}. {pair}")

# 按结算货币分类
usdt_pairs = [p for p in trading_pairs if p.endswith("-USDT-SWAP")]
usd_pairs = [p for p in trading_pairs if p.endswith("-USD-SWAP")]
usdc_pairs = [p for p in trading_pairs if p.endswith("-USDC-SWAP")]

print("\n按结算货币统计:")
print(f"USDT结算: {len(usdt_pairs)} 个")
print(f"USD结算: {len(usd_pairs)} 个")
print(f"USDC结算: {len(usdc_pairs)} 个")

# 提取主要加密货币列表(USDT对)
main_cryptos = [p.split("-")[0] for p in usdt_pairs]
print("\n支持USDT交易的主要加密货币:", ", ".join(main_cryptos[:10]) + "...等") 