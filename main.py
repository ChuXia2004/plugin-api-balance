import aiohttp

from core.plugin import BasePlugin, on, Priority
from core.provider import LLMRequest
from core.utils.tool_utils import BaseTool


class ApiBalanceTool(BaseTool):

    name = "query_api_balance"

    description = "查询 DeepSeek 或 SiliconFlow 余额"

    parameters = {
        "type": "object",
        "properties": {
            "provider": {
                "type": "string",
                "description": "deepseek 或 siliconflow"
            }
        },
        "required": ["provider"]
    }

    def __init__(self, ctx, plugin):
        self.ctx = ctx
        self.plugin = plugin

    async def execute(
        self,
        event,
        provider: str,
        *args,
        **kwargs
    ):
        provider = str(provider).lower()

        if provider == "deepseek":
            return await self.plugin.query_deepseek_balance()

        if provider == "siliconflow":
            return await self.plugin.query_siliconflow_balance()

        return f"\u4e0d\u652f\u6301\u7684\u4f9b\u5e94\u5546: {provider}"




class ApiBalancePlugin(BasePlugin):

    def __init__(self, ctx, cfg: dict):
        super().__init__(ctx, cfg)

        self.deepseek_api_key = ""
        self.siliconflow_api_key = ""

    async def initialize(self):

        self.deepseek_api_key = self.plugin_cfg.get(
            "deepseek_api_key",
            ""
        )

        self.siliconflow_api_key = self.plugin_cfg.get(
            "siliconflow_api_key",
            ""
        )

    async def terminate(self):
        pass

    @on.llm_request(priority=Priority.HIGH)
    async def inject_tools(
        self,
        event,
        req: LLMRequest,
        *args,
        **kwargs
    ):

        try:
            req.tool_set.add(
                ApiBalanceTool(
                    ctx=self.ctx,
                    plugin=self
                )
        )

        except Exception as e:
            print(
                f"[api_balance] tool register failed: {e}"
            )

    async def query_deepseek_balance(self):

        if not self.deepseek_api_key:
            return "\u672a\u914d\u7f6e DeepSeek API Key"

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    "https://api.deepseek.com/user/balance",
                    headers={
                        "Authorization":
                            f"Bearer {self.deepseek_api_key}"
                    }
                ) as resp:

                    data = await resp.json()

                    if "balance_infos" not in data:
                        return f"\u67e5\u8be2\u5931\u8d25: {data}"

                    total = 0

                    for item in data["balance_infos"]:
                        total += float(
                            item.get(
                                "total_balance",
                                0
                            )
                        )

                    return (
                        f"DeepSeek\u5f53\u524d\u4f59\u989d\uff1a"
                        f"{total:.2f} \u5143"
                    )

        except Exception as e:
            return f"DeepSeek\u67e5\u8be2\u5931\u8d25\uff1a{e}"

    async def query_siliconflow_balance(self):

        if not self.siliconflow_api_key:
            return "\u672a\u914d\u7f6e SiliconFlow API Key"

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    "https://api.siliconflow.cn/v1/user/info",
                    headers={
                        "Authorization":
                            f"Bearer {self.siliconflow_api_key}"
                    }
                ) as resp:

                    data = await resp.json()

                    balance = (
                        data
                        .get("data", {})
                        .get("balance")
                    )

                    if balance is None:
                        return f"\u67e5\u8be2\u5931\u8d25: {data}"

                    return (
                        f"SiliconFlow\u5f53\u524d\u4f59\u989d\uff1a"
                        f"{balance} \u5143"
                    )

        except Exception as e:
            return f"SiliconFlow\u67e5\u8be2\u5931\u8d25\uff1a{e}"