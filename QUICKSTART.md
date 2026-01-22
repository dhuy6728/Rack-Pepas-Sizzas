# Hướng dẫn Bắt đầu Nhanh 🚀

## Bước 1: Chuẩn bị
- ✅ Tạo thư mục dự án
- ✅ Cài đặt Python 3.8+ (nếu chưa có)

## Bước 2: Cài đặt Virtual Environment
```powershell
# Trên Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Trên Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

## Bước 3: Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

## Bước 4: Thiết lập Token
1. Vào Discord Developer Portal: https://discord.com/developers/applications
2. Tạo "New Application" và "Add Bot"
3. Copy bot token
4. Tạo file `.env` (copy từ `.env.example`)
5. Dán token vào `DISCORD_TOKEN=your_token_here`

## Bước 5: Thêm Bot vào Server
1. OAuth2 → URL Generator
2. Chọn: `bot`
3. Chọn permissions: `Send Messages, Read Messages, Manage Messages` (tuỳ chọn)
4. Copy URL và mở trong trình duyệt
5. Chọn server và thêm bot

## Bước 6: Chạy Bot
```bash
python main.py
```

## Các Lệnh Test
- `!ping` - Kiểm tra latency
- `!hello` - Bot chào bạn
- `!dice` - Tung xúc xắc
- `!help_custom` - Xem tất cả lệnh

## Cấu trúc File

```
📁 Discord Bot/
├── 📄 main.py              ← Chạy file này
├── 📄 config.py            ← Cấu hình
├── 📄 requirements.txt      ← Các package cần thiết
├── 📄 .env.example         ← Mẫu file (sao chép thành .env)
├── 📄 README.md            ← Tài liệu đầy đủ
├── 📄 QUICKSTART.md        ← File này
├── 📁 cogs/                ← Các module tính năng
│   ├── fun.py              ← Lệnh giải trí
│   └── moderation.py       ← Lệnh quản lý
└── 📁 logs/                ← Lưu log
```

## Thêm Lệnh Mới

Tạo file `.py` trong thư mục `cogs/`:

```python
from discord.ext import commands

class MyFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def mycommand(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyFeature(bot))
```

## Giải quyết Vấn đề

| Vấn đề | Giải pháp |
|--------|----------|
| Bot không kết nối | Kiểm tra token, restart bot |
| Lệnh không làm việc | Kiểm tra prefix, restart bot |
| Module không tải | Kiểm tra syntax file cogs |
| Bot không có quyền | Cấp thêm permissions trên server |

## Liên kết Hữu ích
- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Discord API](https://discord.com/developers/)

**Good luck! 🎉**
