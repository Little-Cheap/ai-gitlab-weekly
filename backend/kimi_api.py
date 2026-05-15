import httpx
import json
from typing import List, Dict
import config


async def generate_weekly_report(commits_text: str, start_date: str, end_date: str) -> str:
    if not commits_text or commits_text == "本周没有提交记录":
        return "本周没有工作记录，无法生成周报"
    
    api_key = config.KIMI_API_KEY.strip() if config.KIMI_API_KEY else ""
    api_url = config.KIMI_API_URL.rstrip('/')
    
    if not api_url.endswith('/chat/completions'):
        api_url = f"{api_url}/chat/completions"
    
    print(f"[DEBUG] Kimi API Key (前6位): {api_key[:6] if len(api_key) >= 6 else api_key}...")
    print(f"[DEBUG] Kimi API Key 长度: {len(api_key)}")
    print(f"[DEBUG] Kimi API URL: {api_url}")
    
    prompt = f"""你是一个专业的周报助手。请根据以下Git提交记录，生成一份结构化的工作周报。

时间范围：{start_date} 至 {end_date}

提交记录：
{commits_text}

要求：
1. 按项目/模块分类整理工作内容
2. 将零散的commit信息归纳总结为完整的工作项
3. 突出重点成果和关键进展
4. 语言简洁专业，避免过于技术化的描述
5. 推测并添加合理的下周计划

输出格式：
## 本周工作总结

### 项目名称
- 完成了xxx功能开发
- 修复了xxx问题
- 优化了xxx性能

## 技术亮点
- （总结本周的技术亮点或解决方案）

## 下周计划
- （根据提交趋势推测下周工作方向）

请直接输出周报内容，不要有其他说明文字。"""

    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'KimiCLI/1.6',
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "kimi-for-coding",
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的技术周报撰写助手，擅长将代码提交记录整理成结构清晰的工作周报。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(
                api_url,
                headers=headers,
                content=json.dumps(data)
            )
            
            if response.status_code == 401:
                return "Kimi API Key 认证失败，请检查 API Key 是否正确。\n\n获取方式：\n1. 访问 https://platform.moonshot.cn\n2. 注册/登录账号\n3. 在「API Key 管理」中创建新的 API Key"
            
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except httpx.HTTPStatusError as e:
            print(f"Error calling Kimi API: {e}")
            return f"Kimi API 调用失败 (HTTP {e.response.status_code})：{e.response.text}"
        except httpx.HTTPError as e:
            print(f"Error calling Kimi API: {e}")
            return f"生成周报失败：{str(e)}"
        except (KeyError, IndexError) as e:
            print(f"Error parsing Kimi API response: {e}")
            return f"解析响应失败：{str(e)}"
}]}]}