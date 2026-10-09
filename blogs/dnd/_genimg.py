"""Generate blog illustrations with Aliyun Bailian qwen-image-3.0-pro.

Usage: python _genimg.py specs.json
specs.json: [{"name": "assets/hero_cover", "size": "2048*1024", "prompt": "..."}]
"""
import json
import sys
import urllib.request

import os

# 请通过环境变量提供 dashscope API key（不要提交到仓库）：
#   PowerShell:  $env:DASHSCOPE_API_KEY="sk-..."   |   bash: export DASHSCOPE_API_KEY=sk-...
KEY = os.environ.get("DASHSCOPE_API_KEY", "")
if not KEY:
    sys.exit("DASHSCOPE_API_KEY 未设置；导出环境变量后重试。")
URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"


def gen(prompt, size, path):
    payload = {
        "model": "qwen-image-3.0-pro",
        "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]},
        "parameters": {"size": size, "n": 1, "watermark": False},
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.loads(r.read().decode())
    img = data["output"]["choices"][0]["message"]["content"][0]["image"]
    urllib.request.urlretrieve(img, path)
    return path


if __name__ == "__main__":
    specs = json.load(open(sys.argv[1], encoding="utf-8"))
    for s in specs:
        out = s["name"] + ".jpg"
        try:
            gen(s["prompt"], s["size"], out)
            print("OK", out)
        except Exception as e:
            print("FAIL", out, type(e).__name__, e)
