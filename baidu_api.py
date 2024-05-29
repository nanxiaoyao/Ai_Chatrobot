import erniebot
import os
import logging

# 配置日志记录器，只记录 baidu_api.py 文件的日志
logger = logging.getLogger('baidu_api')
logger.setLevel(logging.INFO)

# 创建一个文件处理器，专门用于 baidu_api.py 的日志
file_handler = logging.FileHandler('baidu_api.log')  # 日志存储的文件路径
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到 baidu_api 日志记录器
logger.addHandler(file_handler)

# 其他代码保持不变...

# 从文件中读取 API 访问令牌
def read_api_token(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        logging.error(f"API token file not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while reading the API token file: {e}")
        return None

# 设置 API 访问令牌,此处输入你api_key正确文件路径
api_token = read_api_token('/Your file path/key/ernie.txt')
if api_token:
    erniebot.api_type = 'aistudio'
    erniebot.access_token = api_token
else:
    logger.error("API token is not set. Please check the file path and contents.")
    exit(1)

# 生成回复的函数，增加错误处理和日志记录
def generate_reply(user_input):
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content': user_input}],
        )
        reply_text = response.get_result()
        # 记录 erniebot 返回的回复内容
        logger.info(f"ErnieBot replied to input '{user_input}': {reply_text}")
        return reply_text
    except erniebot.OpenAIError as e:
        # 记录 API 错误
        logger.error(f"OpenAI error occurred: {e}")
        return str(e)
    except Exception as e:
        # 记录其他意外错误
        logger.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."

# 示例：生成回复
if __name__ == '__main__':
    user_input = "你好，机器人！"
    reply = generate_reply(user_input)
    if reply != "An unexpected error occurred.":
        print(f"User: {user_input}")
        print(f"Bot: {reply}")
        # 可选：记录到日志文件中
        logger.info(f"Final bot response to user: {reply}")
    else:
        print(f"Error: {reply}")
    