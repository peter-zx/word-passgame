



理解 pyngrok 的使用步骤

安装 pyngrok： 这是第一步，您需要安装 pyngrok 库，它允许您在 Python 代码中控制 ngrok。
设置 ngrok 认证令牌： ngrok 需要您的认证令牌才能工作。您需要从 ngrok 网站获取令牌并将其设置到代码中。
启动 ngrok 隧道： 您需要指定要转发的本地端口，ngrok 将创建一个公共 URL，该 URL 将流量转发到您的本地端口。
使用公共 URL： 您可以使用 ngrok 提供的公共 URL 从外部访问您的本地应用程序。
在 Google Colab 中使用 pyngrok 的具体步骤

打开 Google Colab 笔记本： 打开您要运行 word-passgame 项目的 Google Colab 笔记本。

安装 pyngrok： 在您的代码中，确保在任何使用 pyngrok 的代码之前运行以下命令。通常在第一个代码块中运行：

Python

!pip install pyngrok
设置 ngrok 认证令牌： 获取您的 ngrok 认证令牌，然后将其插入到以下代码中：

Python

from pyngrok import ngrok

ngrok.set_auth_token("您的 ngrok 认证令牌") #请替换为你自己的token
!ngrok authtoken 37P752QOOSEWEKSXZIZR3K6Z4LAV5Q2M  # 替换为你的 ngrok 认证令牌

重要提示： 请务必将 "您的 ngrok 认证令牌" 替换为您自己的 ngrok 认证令牌。
启动 ngrok 隧道： 确定您的应用程序正在监听的端口号。例如，如果您的应用程序正在监听端口 5000，请使用以下代码：

Python

http_tunnel = ngrok.connect(5000)
获取公共 URL： ngrok 将创建一个公共 URL，您可以使用以下代码获取该 URL：

Python

public_url = http_tunnel.public_url

print("ngrok 公共 URL:", public_url)
您可以使用 public_url 从外部访问您的应用程序。