# Discord Bot đơn giản 🤖

Một Discord Bot được xây dựng bằng Python sử dụng library `discord.py`.

## Tính năng

✨ **Các lệnh cơ bản:**
- `!ping` - Kiểm tra độ trễ của bot
- `!hello` - Bot sẽ chào bạn
- `!user [@user]` - Hiển thị thông tin về người dùng
- `!help_custom` - Hiển thị danh sách tất cả lệnh

🎮 **Các lệnh giải trí (Fun):**
- `!dice` - Tung xúc xắc 6 mặt
- `!coin` - Tung đồng xu
- `!random [min] [max]` - Chọn số ngẫu nhiên
- `!choose [option1] [option2] ...` - Chọn một lựa chọn

🎲 **Oẳn tù tì Multiplayer (Rock Paper Scissors):**
- `!rps @opponent` - Chơi Oẳn tù tì với người khác (2 người)
  - Gửi DM để chọn (lựa chọn ẩn từ đối thủ)
  - Nhấp nút 🪨 📄 ✂️ để chọn
  - Kết quả hiển thị khi cả 2 đều chọn hoặc hết 30 giây
  - Nếu chỉ 1 người chọn = thua
- `!rpshelp` - Xem hướng dẫn chi tiết

🔨 **Các lệnh Moderation:**
- `!kick [@member] [reason]` - Kick một thành viên (cần quyền)
- `!ban [@member] [reason]` - Ban một thành viên (cần quyền)
- `!mute [@member]` - Mute một thành viên (cần quyền)
- `!clear [amount]` - Xóa tin nhắn (cần quyền)

## Yêu cầu

- Python 3.8+
- pip (Package installer for Python)

## Cài đặt

### 1. Clone hoặc tải xuống dự án

```bash
cd "d:\Python Project\Discord Bot"
```

### 2. Tạo Virtual Environment (tuỳ chọn nhưng được khuyến khích)

**Trên Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Trên Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt các package cần thiết

```bash
pip install -r requirements.txt
```

### 4. Tạo file `.env`

Sao chép file `.env.example` và đổi tên thành `.env`:

```bash
cp .env.example .env
```

Hoặc tạo file `.env` thủ công và thêm:

```
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
BOT_STATUS=Hello World!
```

### 5. Lấy Bot Token

1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications)
2. Tạo "New Application"
3. Đặt tên cho bot của bạn
4. Vào tab "Bot" và click "Add Bot"
5. Copy token và dán vào file `.env`
6. Bật các intents cần thiết:
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT

### 6. Thêm bot vào server

1. Vào tab "OAuth2" → "URL Generator"
2. Chọn scopes: `bot`
3. Chọn permissions cần thiết (e.g., Send Messages, Manage Messages, etc.)
4. Copy URL được tạo ra và mở trong trình duyệt
5. Chọn server và thêm bot

## Chạy Bot

```bash
python main.py
```

Bạn sẽ thấy thông báo:
```
2024-XX-XX XX:XX:XX,XXX - __main__ - INFO - YourBotName#0000 đã kết nối!
```

Điều này có nghĩa là bot đã sẵn sàng!

## Cấu trúc Dự án

```
Discord Bot/
├── main.py                 # File chính của bot
├── config.py               # File cấu hình
├── requirements.txt        # Danh sách các package cần thiết
├── .env.example           # Mẫu file .env
├── .gitignore             # Git ignore file
├── README.md              # File này
├── cogs/                  # Các module tính năng
│   ├── fun.py             # Lệnh giải trí
│   └── moderation.py      # Lệnh quản lý
└── logs/                  # Thư mục lưu log
```

## Tạo Cog (Module) mới

Để thêm các lệnh mới, tạo file mới trong thư mục `cogs/`:

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mycommand', help='Mô tả lệnh')
    async def my_command(self, ctx):
        await ctx.send('Hello!')

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

Lưu file và bot sẽ tự động tải nó!

## Troubleshooting

### Bot không kết nối
- Kiểm tra token trong file `.env`
- Kiểm tra bot đã được thêm vào server chưa
- Kiểm tra intents trong Developer Portal

### Lệnh không hoạt động
- Kiểm tra prefix (mặc định là `!`)
- Kiểm tra bot có quyền cần thiết không
- Xem logs để tìm lỗi

### Module không tải được
- Kiểm tra tên file trong thư mục `cogs/`
- Kiểm tra syntax của file

## Hữu ích

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)

## Giấy phép

MIT License

## Liên hệ

Nếu bạn có câu hỏi hoặc gặp vấn đề, vui lòng mở issue!

---

**Chúc bạn xây dựng bot thành công!** 🚀
