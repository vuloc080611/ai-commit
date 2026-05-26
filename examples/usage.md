# Ví dụ sử dụng ai-commit

## Chuẩn bị

1. Cài đặt: `pip install -e .`
2. Export API key: `export GEMINI_API_KEY="your_key"`

## Demo nhanh

```bash
cd ~/my-project
# Sửa vài file
echo "print('hello')" > main.py
git add .

# Sinh commit message
ai-commit suggest

# Hoặc tự động commit tất cả
ai-commit commit
