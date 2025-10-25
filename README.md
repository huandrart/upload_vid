# 🌐 VideoShare - Nền Tảng Chia Sẻ Video Web

Ứng dụng web cho phép người dùng upload, xem và chia sẻ video trực tuyến.

## ✨ Tính Năng Chính

### 🚀 **Upload Video**
- Upload video lên server (tối đa 100MB)
- Hỗ trợ: MP4, AVI, MOV, MKV, WMV
- Kéo thả file hoặc click để chọn
- Preview thông tin file trước khi upload

### 📺 **Xem Video Online**
- Player HTML5 với đầy đủ tính năng
- Điều khiển âm lượng, tốc độ phát
- Toàn màn hình, tắt tiếng
- Hiển thị thời lượng và độ phân giải

### 👥 **Chia Sẻ Cộng Đồng**
- Xem tất cả video từ người dùng khác
- Thống kê lượt xem, kích thước file
- Tìm kiếm video theo tên, người upload
- Chia sẻ link social media

### 📊 **Quản Lý**
- Database SQLite lưu thông tin video
- Theo dõi lượt xem, ngày upload
- Thống kê tổng video, dung lượng

## 🛠️ Cài Đặt Local

```bash
# Clone hoặc download folder web_video_app
cd web_video_app

# Cài dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python app.py

# Mở browser: http://localhost:5000
```

## 🌐 Deploy Lên Internet

### 1. **Heroku** (Miễn phí)

#### Bước 1: Chuẩn bị file Heroku
```bash
# Tạo Procfile
echo "web: python app.py" > Procfile

# Cập nhật app.py port
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

#### Bước 2: Deploy
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login Heroku
heroku login

# Tạo app
heroku create your-video-app-name

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Mở app
heroku open
```

### 2. **Railway** (Dễ dàng)

#### Bước 1: Tải code lên GitHub
```bash
# Tạo repository GitHub mới
# Upload tất cả file trong web_video_app
```

#### Bước 2: Deploy Railway
1. Vào **railway.app**
2. Login với GitHub
3. **New Project** → Import từ GitHub
4. Chọn repository vừa tạo
5. Railway tự động detect và deploy

### 3. **PythonAnywhere** (Cho Python)

#### Bước 1: Upload code
1. Đăng ký **pythonanywhere.com**
2. Upload file qua Web interface
3. Hoặc clone từ GitHub

#### Bước 2: Config Web App
1. **Web** tab → **Add new web app**
2. Chọn **Flask**
3. Set **Source code** path
4. **Reload** web app

### 4. **Vercel** (Frontend + API)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts
```

## 📁 Cấu Trúc Project

```
web_video_app/
├── app.py                  # Flask server chính
├── requirements.txt        # Dependencies
├── video_database.db      # SQLite database (tự tạo)
├── uploads/               # Thư mục chứa video
├── templates/             # HTML templates
│   ├── base.html         # Layout chung
│   ├── index.html        # Trang chủ
│   ├── upload.html       # Trang upload
│   └── video.html        # Trang xem video
└── static/               # CSS, JS, images (nếu có)
```

## 🔧 Config Nâng Cao

### Database Production
```python
# Thay SQLite bằng PostgreSQL cho production
# requirements.txt thêm: psycopg2-binary

import os
if os.environ.get('DATABASE_URL'):
    # PostgreSQL for production
    DATABASE_URL = os.environ.get('DATABASE_URL')
else:
    # SQLite for development
    DATABASE_URL = 'sqlite:///video_database.db'
```

### File Storage Cloud
```python
# Upload lên AWS S3, Google Cloud Storage
# Thay vì lưu local

import boto3
# Config S3 bucket cho video files
```

### Domain Tùy Chỉnh
```bash
# Heroku custom domain
heroku domains:add yourdomain.com

# Config DNS records
# CNAME: yourdomain.com → your-app.herokuapp.com
```

## 🚀 Tính Năng Mở Rộng

### 1. **User Authentication**
```python
# Thêm đăng ký, đăng nhập
from flask_login import LoginManager
```

### 2. **Video Streaming**
```python
# Stream video chunks thay vì download full
@app.route('/stream/<filename>')
def stream_video(filename):
    # Range requests support
```

### 3. **Comments & Likes**
```sql
-- Thêm bảng comments
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    video_id TEXT,
    user_name TEXT,
    comment TEXT,
    timestamp TEXT
);
```

### 4. **Video Processing**
```python
# Compress video, generate thumbnails
import ffmpeg
```

## 📊 Monitoring & Analytics

### Google Analytics
```html
<!-- Thêm vào base.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
```

### Database Backup
```bash
# Heroku Postgres backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download
```

## 🔒 Bảo Mật

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)
```

### File Validation
```python
def validate_video_file(file):
    # Check file signature, not just extension
    # Scan for malware
    # Limit file size
```

## 📞 Hỗ Trợ Deploy

### Lỗi Thường Gặp

**Port Error:**
```python
# Sửa app.py
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

**Database Error:**
```bash
# Check database permissions
# Create uploads folder
mkdir uploads
```

**Memory Limit:**
```bash
# Heroku upgrade dyno
heroku ps:scale web=1:standard-1x
```

### Test Production
```bash
# Test app locally with production settings
export FLASK_ENV=production
python app.py
```

---

**🎉 Sau khi deploy thành công:**
- Chia sẻ URL với bạn bè
- Mọi người có thể upload và xem video
- Database lưu trữ tất cả video
- Accessible từ mọi nơi có internet!

**📱 Mobile-friendly:** App đã responsive, hoạt động tốt trên điện thoại.