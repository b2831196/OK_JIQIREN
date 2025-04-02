#!/usr/bin/env python
import datetime

from flask import Flask, render_template, jsonify, request, json, session
from debugBA2 import main
from debugBA2.celuo import ert as ce
import pyecharts.options as opts
from pyecharts.charts import Kline, EffectScatter, Bar, Grid, Line
from pyecharts.globals import CurrentConfig
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from pyecharts.commons.utils import JsCode
from pyecharts.globals import SymbolType
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"


app = Flask(__name__)


@app.route('/')
def index():
    chart_code = klinechart()
    return render_template('index.html', chart_code=chart_code)

def klinechart():
    data = ce.get_dataBA('ETHUSDT', '4h')

    if data.empty:
        print("数据为空")
        return

    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)
    data['close'] = data['close'].astype(float)
    data['volume'] = data['volume'].astype(float)
    result = ce.is_evening_star(data)
    for idx, item in enumerate(result):
        ratio = item['ratio']
        index = item['index']
        closetime = item['closetime']
        print("Result {}: Ratio={}, K线索引={}, 关闭时间={}".format(idx, ratio, index, closetime))

    # 创建 K 线图对象
    kline = (
        Kline()
        .add_xaxis(data.index.tolist())
        .add_yaxis(
            "K-line",
            data[["open", "close", "high", "low"]].values.tolist(),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Highest Point"),  # 添加最高点标记
                    opts.MarkPointItem(type_="min", name="Lowest Point"),  # 添加最低点标记
                    *[
                        opts.MarkPointItem(
                            type_="buy", name="Buy", value=item['close'], coord=[index, item['close']]
                        )  # 添加买点标记
                        for index, item in enumerate(result)
                    ]
                ]
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts()],
            title_opts=opts.TitleOpts(title="Kline-DataZoom-slider"),
        )
    )


    line = (
        Line()
        .add_xaxis([index for index, _ in enumerate(result)])
        .add_yaxis(
            "Buy",
            [item['close'] for item in result],
            symbol="diamond",  # 使用钻石形状符号
            symbol_size=8,  # 设置符号的大小
            label_opts=opts.LabelOpts(position="top"),  # 设置标签在顶部显示
        )
    )

    # 创建 Overlap 图表
    grid_chart = Grid()
    grid_chart.add(kline, grid_opts=opts.GridOpts(pos_left="11%", pos_right="8%", height="40%"))
    grid_chart.add(line, grid_opts=opts.GridOpts(pos_left="11%", pos_right="8%", height="40%"))

    chart_code = grid_chart.render_embed()
    return chart_code

@app.route('/api/flask-data', methods=['GET'])
def get_flask_data():
    # 获取表单数据
    symbol = request.args.get('symbol')
    quantity = request.args.get('quantity')

    if symbol and quantity:
        result = {'data': main.process_trading(symbol, quantity)}
        print(result)
        return jsonify(result)


@app.route('/api/flask-order', methods=['GET'])
def get_flask_order():
    # 获取表单数据
    symbol = request.args.get('symbol')
    data = main.check_long_position(symbol)
    result = {'data': data}

    return json.dumps(result), 200, {'Content-Type': 'application/json'}


# import time
#
# @app.route('/api/xuan-bi', methods=['GET'])
# def process_xuanbi_result():
#     option1 = request.args.get('celuo')
#     if option1:
#         print('选择的:', option1)
#         data = main.get_xuan_bi(option1)
#         result = {'data': data}
#         print(result)
#     time.sleep(500)
#     return jsonify(result)
app.secret_key = "eyitrreyio"
@app.route('/api/xuan-bi', methods=['POST'])
def process_xuanbi_result():
    option1 = request.form.get('celuo')
    if option1:
        print('选择的:', option1)
        # 存储选币结果到session
        session['xuanbi_result'] = main.get_xuan_bi(option1)
        return jsonify({'message': '处理中'})
    else:
        return jsonify({'error': '缺少参数'})

@app.route('/api/xuan-bi/result', methods=['GET'])
def get_xuanbi_result():
    if 'xuanbi_result' in session:
        result = session['xuanbi_result']
        if result:
            session.pop('xuanbi_result')  # 任务执行完成后删除session中的结果
            print({'data': result})
            return jsonify({'data': result})
    return jsonify({'data': []})


#
# 在HTML中可以使用以下语句来读取symbol和quantity的值：
#
# { % if data %}
# Symbol: {{data.symbol}}
# < br >
# Quantity: {{data.quantity}}
# { % endif %}
#
# 其中，data为后端返回的json数据。可以通过JavaScript或者其它方式将数据传递给HTML页面。

if __name__ == '__main__':
    app.run()


    # except Exception as e:
    #     # 捕获错误并返回友好的错误提示
    #     error_message = '服务器内部错误：{}'.format(str(e))
    #     return jsonify({'error_message': error_message})
