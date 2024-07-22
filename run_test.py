#!/usr/bin/env python3

import subprocess
import sys

def main():
  LLAMA_BUILD = "b3436"
  print("downloading llama-server")
  subprocess.check_call(
      [
        "curl",
        "-sSLO",
        f"https://github.com/ggerganov/llama.cpp/releases/download/{LLAMA_BUILD}/llama-{LLAMA_BUILD}-bin-macos-arm64.zip",
      ])

  print("extracting llama-server")
  subprocess.check_call(
      [
        "unzip",
        f"llama-{LLAMA_BUILD}-bin-macos-arm64.zip"
      ])
  print("downloading qwen2 1.5B Q2_K"
  subprocess.check_call(
      [
        "curl",
        "-sSLO",
        "https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/main/qwen2-1_5b-instruct-q2_k.gguf?download=true"
      ])
  subprocess.Popen(["./llama-server", "-ngl", sys.argv[1]])
