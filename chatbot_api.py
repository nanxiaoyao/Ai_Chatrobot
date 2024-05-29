# 导入Flask框架及其相关组件
from flask import Flask, request, jsonify
# 导入自定义的ali_api和baidu_api模块
import ali_api
import baidu_api
# 导入Flask的CORS插件，用于处理跨域请求
from flask_cors import CORS

# 初始化Flask应用
app = Flask(__name__)
# 设置CORS策略，允许所有源访问/chat开头的所有路由
CORS(app, resources={r"/chat/*": {"origins": "*"}})

# 定义一个Flask的after_request装饰器，用于在每次响应后添加特定的HTTP头
@app.after_request
def after_request(response):
    # 允许来自所有源的请求
    response.headers.add('Access-Control-Allow-Origin', '*')
    # 允许跨域请求携带Content-Type和Authorization头
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # 允许跨域请求的HTTP方法：GET, POST, PUT, DELETE, OPTIONS
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

# 定义一个路由及其对应的处理函数，用于处理POST请求到/chat的情况
@app.route('/chat', methods=['POST'])
def chat():
    # 从请求的JSON数据中获取用户输入和模型名称
    data = request.get_json()
    user_input = data['message']
    model = data['model']

    # 根据模型名称调用不同的生成回复函数
    if model == 'ali':
        reply = generate_reply_ali(user_input)
    elif model == 'baidu':
        reply = generate_reply_baidu(user_input)
    else:
        reply = "请先选择对话模型！"

    # 将生成的回复以JSON格式返回给客户端
    return jsonify({'reply': reply})

# 定义一个函数，用于调用ali_api生成回复
def generate_reply_ali(user_input):
    reply = ali_api.generate_reply(user_input)
    return reply

# 定义一个函数，用于调用baidu_api生成回复
def generate_reply_baidu(user_input):
    reply = baidu_api.generate_reply(user_input)
    return reply

# 应用的启动入口
if __name__ == '__main__':
    app.run(port=18889)