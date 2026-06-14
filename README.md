# API余额查询插件

查询 DeepSeek 和 SiliconFlow API 余额的 KiraAI 插件。

## 功能

- 查询 DeepSeek 账户余额
- 查询 SiliconFlow 账户余额
- 支持通过 LLM 工具调用触发
- 支持关键词触发（可选）

## 配置

在插件配置中填写以下项：

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `deepseek_api_key` | sensitive | DeepSeek API Key |
| `siliconflow_api_key` | sensitive | SiliconFlow API Key |
| `enable_keyword_trigger` | switch | 是否启用关键词触发 |

## 使用方法

配置好 API Key 后，直接向 AI 发送类似以下指令：

- "查询 DeepSeek 余额"
- "看看 SiliconFlow 还有多少钱"
- "帮我查一下 API 余额"

AI 会自动调用工具查询对应平台的余额。

## 作者

- 代码：ChuXia
- 上传助手：小染（被初夏抓来当苦力的(｀へ´)）