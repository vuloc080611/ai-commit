# 🤖 ai-commit

> Viết commit message thông minh bằng AI – không còn "fix bug", "update code" nhàm chán nữa.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![tests](https://github.com/YOUR_USERNAME/ai-commit/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/ai-commit/actions/workflows/test.yml)
[![Gemini](https://img.shields.io/badge/Gemini-API-orange)](https://ai.google.dev/)

## ✨ Tính năng

- Tự động phân tích `git diff` và sinh ra commit message chuẩn Conventional Commits.
- Hỗ trợ **Gemini** (miễn phí) và **OpenAI** (ChatGPT).
- Có thể dùng như CLI hoặc cài làm **Git hook** (tự động gợi ý mỗi khi bạn gõ `git commit`).
- Tuỳ chỉnh style: vui nhộn, nghiêm túc, hoặc theo yêu cầu riêng.
- Không gửi code của bạn lên cloud nếu bạn dùng local model (tuỳ chọn).

## 📦 Cài đặt

```bash
pip install ai-commit
