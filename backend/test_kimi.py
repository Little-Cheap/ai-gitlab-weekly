import httpx
import sys
import json

def test_kimi_api(api_url: str, api_key: str):
    api_url = api_url.rstrip('/')
    if not api_url.endswith('/chat/completions'):
        api_url = f"{api_url}/chat/completions"
    
    print(f"测试 Kimi API...")
    print(f"URL: {api_url}")
    print(f"API Key (前6位): {api_key[:6] if len(api_key) >= 6 else api_key}...")
    print(f"API Key 长度: {len(api_key)}")
    print("-" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "kimi-for-coding",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    with httpx.Client(timeout=60.0) as client:
        try:
            response = client.post(api_url, headers=headers, content=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API 调用成功!")
                print(f"回复: {result['choices'][0]['message']['content']}")
            else:
                print(f"❌ 调用失败: HTTP {response.status_code}")
                print(f"响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 连接错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python test_kimi.py <api_url> <api_key>")
        print("示例: python test_kimi.py https://api.kimi.com/coding/v1 sk-xxxxxx")
        sys.exit(1)
    
    test_kimi_api(sys.argv[1], sys.argv[2])
