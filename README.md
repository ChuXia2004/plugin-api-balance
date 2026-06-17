# API余额查询插件2.5.0

查询 DeepSeek、SiliconFlow、Moonshot 以及自定义 New API 站点余额的 KiraAI 插件。

## 功能

- 查询 DeepSeek 账户余额
- 查询 SiliconFlow 账户余额
- 查询 Moonshot 账户余额
- 查询自定义 New API 站点余额（支持多个站点，JSON 或简易文本格式）
- 支持通过 LLM 工具调用触发
- 支持关键词触发（可选）

## 配置

### DeepSeek
| 配置项 | 类型 | 说明 |
|--------|------|------|
| `deepseek_base_url` | string | DeepSeek API 基础 URL |
| `deepseek_api_key` | sensitive | DeepSeek API Key |

### SiliconFlow
| 配置项 | 类型 | 说明 |
|--------|------|------|
| `siliconflow_base_url` | string | SiliconFlow API 基础 URL |
| `siliconflow_api_key` | sensitive | SiliconFlow API Key |

### 月之暗面 (Kimi)
| 配置项 | 类型 | 说明 |
|--------|------|------|
| `moonshot_base_url` | string | Moonshot API 基础 URL |
| `moonshot_api_key` | sensitive | Moonshot API Key |

### 自定义 New API 站点

支持两种配置方式（可同时使用，但非必要不用同用户同站点重复，没有意义）：

#### 1. 简易文本格式（推荐，简洁）
在 `section_newapi_simple` 中每行填写一个站点，格式为：

```
名称;base_url;系统访问令牌;纯数字用户ID;换算比例(可选，即可不填)
```

- **名称**：任意标识
- **base_url**：站点 API 地址（如 `https://api.example.com`）
- **系统访问令牌**：在站点「个人设置 → 安全设置」中生成，**注意这不是模型调用用的 API Key，而是用于管理接口的令牌**
- **纯数字用户ID**：在站点「个人中心」或「设置」页面中通常显示为 `ID: 12345` 的纯数字编号
- **换算比例**（可选）：`quota ÷ 该值 = 元`，默认 `500000`

示例：
```
我的站点1;https://api.example.com;sk-xxxxxxxx;123456;500000
我的站点2;https://api2.example.com;sk-yyyyyyyy;789012
```

#### 2. JSON 格式
在 `section_newapi` 中以 JSON 数组填写：

```json
[
  {
    "name": "示例站1",
    "base_url": "https://api.example.com",
    "api_key": "系统访问令牌",
    "api_user": "纯数字用户ID",
    "quota_conversion": 500000
  }
]
```

- `api_key`：系统访问令牌（非模型 API Key）
- `api_user`：纯数字用户 ID（在个人设置页面可见）

### 其他
| 配置项 | 类型 | 说明 |
|--------|------|------|
| `enable_keyword_trigger` | switch | 是否启用关键词触发 |

## 使用方法

配置好 API Key 后，直接向 AI 发送类似以下指令：

- "查询 DeepSeek 余额"
- "看看 SiliconFlow 还有多少钱"
- "帮我看看 Moonshot 余额"
- "查询所有 New API 站点的余额"
- "帮我查一下 API 余额"

AI 会自动调用工具查询对应平台的余额。

## 注意事项

- New API 站点的 **系统访问令牌** 与 **模型调用 API Key** 通常是不同的，请勿混淆。
- **纯数字用户 ID** 可在站点的个人设置/账户信息页面找到（通常显示为 `ID: 12345`）。
- `quota_conversion` 换算比例需根据站点实际规则调整，可参考站点设置的 `quota_warning_threshold` 值。

## 作者

- 代码：ChuXia+znq19
- 上传助手：小染（被初夏抓来当苦力的(｀へ´)）
