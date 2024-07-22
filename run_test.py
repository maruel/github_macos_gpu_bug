#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
import textwrap

import requests

def main():
  if len(sys.argv) != 2:
    print("Usage: run_test.py <ngl value>")
    return 1

  LLAMA_BUILD = "b3436"
  if not os.path.isfile(f"llama-{LLAMA_BUILD}-bin-macos-arm64.zip"):
    print("downloading llama-server")
    url = f"https://github.com/ggerganov/llama.cpp/releases/download/{LLAMA_BUILD}/llama-{LLAMA_BUILD}-bin-macos-arm64.zip"
    subprocess.check_call(["curl", "-sLO", url])

  if not os.path.isfile("build/bin/llama-server"):
    print("extracting llama-server")
    subprocess.check_call(["unzip", f"llama-{LLAMA_BUILD}-bin-macos-arm64.zip"])

  model = "qwen2-1_5b-instruct-q2_k.gguf"
  if not os.path.isfile(model):
    print("downloading qwen2 1.5B Q2_K")
    url = f"https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/main/{model}?download=true"
    subprocess.check_call(["curl", "-sLO", url])

  p = subprocess.Popen(
      ["./build/bin/llama-server", "-ngl", sys.argv[1], "--model", model])
  try:
    headers = {"Content-Type": "application/json"}
    for i in range(50):
      result = requests.get(f"http://localhost:8080/health", headers=headers)
      if result.status_code == 200:
        j = result.json()
        if j["status"] == "ok":
          print("Server ready!")
          break
      time.sleep(0.1)
    data = {"prompt": "<|im_start|>user\nWhat are the benefits of GPU acceleration to run large language models?<|im_end|>\n<|im_start|>assistant"}
    result = requests.post(f"http://localhost:8080/completion", headers=headers, json=data).json()
    assert data.get("error") is None, data
    print("Result:\n%s", textwrap.indent(json.dumps(result, indent=2), "  "))
  finally:
    print("killing llama-server")
    p.kill()
    p.wait()
  return 0


if __name__ == "__main__":
  sys.exit(main())
