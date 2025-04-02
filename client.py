import json
import httpx
import socket
import time

import consts as c
import utils
import exceptions


class Client(object):

    def __init__(self, api_key = '-1', api_secret_key = '-1', passphrase = '-1', use_server_time=False, flag='1', base_api = c.API_URL, debug = 'True'):
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.use_server_time = use_server_time
        self.flag = flag
        self.domain = base_api
        self.debug = debug
        
        # 创建带有自定义超时和重试功能的客户端
        try:
            # 设置更长的超时时间，并启用HTTP/1.1以提高兼容性
            self.client = httpx.Client(
                base_url=base_api,
                timeout=30.0,  # 增加超时时间
                http2=False,  # 使用HTTP/1.1而不是HTTP/2
                verify=True,  # 验证SSL证书
            )
            if debug:
                print(f"成功初始化客户端连接到: {base_api}")
        except Exception as e:
            print(f"初始化客户端失败: {e}")
            raise

    def _request(self, method, request_path, params):
        # 移除重试次数限制，改为无限重试
        retry_count = 0
        wait_time = 2  # 初始等待时间，单位秒
        
        while True:
            try:
                if method == c.GET:
                    request_path = request_path + utils.parse_params_to_str(params)
                timestamp = utils.get_timestamp()
                if self.use_server_time:
                    timestamp = self._get_timestamp()
                body = json.dumps(params) if method == c.POST else ""
                if self.API_KEY != '-1':
                    sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body), self.debug), self.API_SECRET_KEY)
                    header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag, self.debug)
                else:
                    header = utils.get_header_no_sign(self.flag, self.debug)
                response = None
                if self.debug == True:
                    print('domain:', self.domain)
                    print('url:', request_path)
                    if method == c.POST:
                        print('body: ', body)
                    print('header: ', header)
                if method == c.GET:
                    response = self.client.get(request_path, headers=header)
                elif method == c.POST:
                    response = self.client.post(request_path, data=body, headers=header)
                
                if response.status_code != 200:
                    print(f"请求失败，状态码: {response.status_code}, 响应: {response.text}")
                
                # 成功执行，跳出循环并返回结果
                return response.json()
            except (httpx.ConnectError, httpx.ReadTimeout, socket.gaierror) as e:
                retry_count += 1
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                
                # 无限重试，只记录重试次数，不再有最大次数限制
                print(f"[{current_time}] 连接错误: {e}, 正在进行第{retry_count}次重试...")
                
                # 使用指数退避策略，但最多等待30秒
                wait_time = min(wait_time * 1.5, 5)
                print(f"[{current_time}] 等待{wait_time:.1f}秒后重试...")
                
                try:
                    time.sleep(wait_time)
                except KeyboardInterrupt:
                    print("用户中断，停止重试")
                    raise
                
                # 继续循环，不抛出异常
                continue
            except Exception as e:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{current_time}] 请求处理时发生未知错误: {e}")
                
                # 对于其他异常，也进行重试
                retry_count += 1
                print(f"[{current_time}] 正在进行第{retry_count}次重试...")
                time.sleep(wait_time)
                continue

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _get_timestamp(self):
        try:
            request_path = c.SERVER_TIMESTAMP_URL
            response = self.client.get(request_path)
            if response.status_code == 200:
                return response.json()['data'][0]['ts']
            else:
                print(f"获取服务器时间失败: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            print(f"获取服务器时间出错: {e}")
            return ""
