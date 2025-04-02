import sys
import traceback

print("Python版本:", sys.version)
print("当前工作目录:", sys.path)

try:
    print("尝试导入PublicData模块...")
    from PublicData import PublicAPI
    print("成功导入PublicData模块")
    
    # 使用模拟交易模式
    flag = "1"
    print(f"使用flag={flag}初始化API...")
    api = PublicAPI(flag=flag)
    print("API初始化成功")
    
    # 获取一些简单信息，尝试API是否工作
    print("正在尝试API调用...")
    result = api.get_instruments(instType="SWAP")
    print("API调用完成")
    
    # 检查结果并输出
    if result and isinstance(result, dict):
        print(f"API返回状态码: {result.get('code')}")
        
        if 'data' in result and isinstance(result['data'], list):
            data_count = len(result['data'])
            print(f"返回数据条数: {data_count}")
            
            if data_count > 0:
                # 只打印前5个交易对作为示例
                print("\n前5个交易对示例:")
                for i, item in enumerate(result['data'][:5]):
                    print(f"{i+1}. {item.get('instId')}")
        else:
            print("未找到数据部分")
    else:
        print("API返回结果不是预期的格式:", result)

except Exception as e:
    print(f"发生错误: {e}")
    traceback.print_exc()
    
print("脚本执行完成") 