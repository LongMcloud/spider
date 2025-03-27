import websocket
import json
import threading


class MiKuaiSpider(object):
    def __init__(self):
        self.__url = "ws://jk.minekuai.com:8008/api/v1/ws/server"
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    # WebSocket 连接成功的回调
    def on_open(self, ws):
        print("WebSocket连接已打开")

    # WebSocket 关闭时的回调
    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket连接关闭，状态码: {close_status_code}")

    # WebSocket 错误时的回调
    def on_error(self, ws, error):
        import traceback
        print(f"WebSocket错误: {error}")
        traceback.print_exc()

    # 处理接收到的消息
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if "servers" in data:
                for server in data["servers"]:
                    name = server["name"]
                    cpu_usage = server["state"]["cpu"]
                    mem_used = server["state"]["mem_used"]
                    mem_total = server["host"]["mem_total"]
                    mem_usage = (mem_used / mem_total) * 100
                    print(f"服务器名称: {name}, CPU使用率: {cpu_usage}%, 内存使用率: {mem_usage:.2f}%")
            else:
                print("没有找到服务器列表字段")
        except json.JSONDecodeError:
            print("消息解析失败")
        except KeyError as e:
            print(f"数据结构错误，缺少字段: {e}")

    def connect_websocket(self):
        # 使用WebSocketApp来连接 WebSocket
        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        # WebSocket连接打开时执行的回调
        ws.on_open = self.on_open

        # 启动WebSocket连接，保持连接直到关闭
        ws.run_forever()

    def start_spider(self):
        # 启动WebSocket连接
        threading.Thread(target=self.connect_websocket, daemon=True).start()

        print("爬虫正在运行，等待WebSocket数据...")
        input("按回车键退出...")


if __name__ == '__main__':
    spider = MiKuaiSpider()
    spider.start_spider()