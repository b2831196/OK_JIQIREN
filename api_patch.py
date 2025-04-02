"""
这个模块用于修复API导入问题，提供兼容层
"""
import sys
import os

# 确保当前目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入需要的模块
import client
import consts
import utils

# 为了解决相对导入，我们创建了一些补丁模块
class Trade:
    class TradeAPI(client.Client):
        def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain='https://www.okx.com', debug=True):
            client.Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug)
        
        def place_order(self, instId, tdMode, side, ordType, sz, ccy='', clOrdId='', tag='', posSide='', px='',
                    reduceOnly='', tgtCcy='', tpTriggerPx='', tpOrdPx='', slTriggerPx='', slOrdPx='',
                    tpTriggerPxType='', slTriggerPxType='', quickMgnType='', stpId='', stpMode=''):
            params = {'instId': instId, 'tdMode': tdMode, 'side': side, 'ordType': ordType, 'sz': sz, 'ccy': ccy,
                  'clOrdId': clOrdId, 'tag': tag, 'posSide': posSide, 'px': px, 'reduceOnly': reduceOnly,
                  'tgtCcy': tgtCcy, 'tpTriggerPx': tpTriggerPx, 'tpOrdPx': tpOrdPx, 'slTriggerPx': slTriggerPx,
                  'slOrdPx': slOrdPx, 'tpTriggerPxType': tpTriggerPxType, 'slTriggerPxType': slTriggerPxType,
                  'quickMgnType': quickMgnType, 'stpId': stpId, 'stpMode': stpMode}
            return self._request_with_params(consts.POST, consts.PLACR_ORDER, params)
        
        def get_order(self, instId, ordId='', clOrdId=''):
            params = {'instId': instId, 'ordId': ordId, 'clOrdId': clOrdId}
            return self._request_with_params(consts.GET, consts.ORDER_INFO, params)

class Account:
    class AccountAPI(client.Client):
        def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain='https://www.okx.com', debug=True):
            client.Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug)
        
        def get_positions(self, instType='', instId=''):
            params = {'instType': instType, 'instId': instId}
            return self._request_with_params(consts.GET, consts.POSITION_INFO, params) 