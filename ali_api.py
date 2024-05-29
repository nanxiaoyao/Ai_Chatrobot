import dashscope
import logging

# 创建一个logger对象，专门用于ali_api的日志记录
ali_logger = logging.getLogger('ali_api')
ali_logger.setLevel(logging.INFO)

# 创建一个handler，用于将日志写入到ali_api.log文件中
log_file_handler = logging.FileHandler('ali_api.log')
log_file_handler.setLevel(logging.INFO)

# 创建一个formatter，定义日志信息的格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file_handler.setFormatter(formatter)

# 将handler添加到logger对象中
ali_logger.addHandler(log_file_handler)

# 从文件中读取阿里云API密钥
def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            ali_logger.info("API密钥读取成功")
            return api_key
    except Exception as e:
        ali_logger.error(f"读取API密钥时发生错误: {str(e)}")
        raise

try:
    # 访问api_key,此处输入你api_key正确文件路径
    dashscope.api_key = read_api_key('/Your file path/key/qianwen.txt')
except Exception as e:
    ali_logger.exception("设置API密钥时发生异常")
    raise

def generate_reply(user_input):
    try:
        response_generator = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=user_input,
            stream=True,
            top_p=0.8
        )

        # 使用列表推导式简化代码，并直接获取最后一段文本
        reply_text = [resp.output.text for resp in response_generator][-1]
        ali_logger.info(f"生成回复: {reply_text}")
        return reply_text
    except Exception as e:
        ali_logger.error(f"生成回复时发生错误: {str(e)}")
        raise
