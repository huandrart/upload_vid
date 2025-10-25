# 🚀 Hướng Dẫn Deploy Web App lên Railway

## 📋 Tổng Quan
Web app này cho phép:
- ✅ **Upload video** lên server
- ✅ **Xem video** của người khác  
- ✅ **Quản lý video** cá nhân
- ✅ **Chia sẻ link** video
- ✅ **Thống kê** lượt xem

## 🌐 Deploy lên Railway (Miễn phí)

### Bước 1: Chuẩn bị Account
1. Vào [railway.app](https://railway.app)
2. Đăng ký bằng GitHub account
3. Verify email

### Bước 2: Chuẩn bị Code
1. **Tạo GitHub Repository:**
   ```bash
   # Tạo repo mới trên GitHub.com
   # Clone về máy hoặc tải lên trực tiếp
   ```

2. **Upload các file này lên GitHub:**
   ```
   📁 web_video_app/
   ├── app.py              # Web application chính
   ├── requirements.txt    # Dependencies
   ├── Procfile           # Railway config
   ├── README.md          # Hướng dẫn
   └── templates/         # HTML templates
       ├── base.html
       ├── index.html
       ├── upload.html
       └── video.html
   ```

### Bước 3: Deploy trên Railway
1. **Login Railway:**
   - Vào [railway.app](https://railway.app)
   - Nhấn "Login" → "Login with GitHub"

2. **Tạo Project:**
   - Nhấn "New Project"
   - Chọn "Deploy from GitHub repo"
   - Chọn repository `web_video_app`

3. **Cấu hình:**
   - Railway tự động detect Python app
   - Tự động cài requirements.txt
   - Tự động chạy theo Procfile

4. **Chờ Deploy:**
   - Quá trình mất 2-5 phút
   - Xem log để check lỗi
   - Sau khi xong sẽ có domain public

### Bước 4: Cấu hình Production
1. **Environment Variables:**
   ```
   SECRET_KEY=your-random-secret-key-here
   ```

2. **Custom Domain (tùy chọn):**
   - Vào Settings → Domains
   - Thêm custom domain nếu có

## 🔧 File Cấu hình Quan trọng

### requirements.txt
```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
gunicorn==21.2.0
```

### Procfile
```
web: gunicorn app:app
```

### app.py (sửa cho production)
```python
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

## 🎯 Sau Khi Deploy Thành Công

### Bạn sẽ có:
- **Public URL**: `https://your-app-name.railway.app`
- **Upload videos**: Mọi người có thể upload
- **Watch videos**: Xem video của nhau
- **Share links**: Chia sẻ video qua link

### Ví dụ URLs:
```
https://your-app.railway.app/              # Trang chủ
https://your-app.railway.app/upload        # Upload video
https://your-app.railway.app/video/abc123  # Xem video cụ thể
```

## 📊 Quản Lý và Monitor

### Railway Dashboard:
- **Logs**: Xem log real-time
- **Metrics**: CPU, RAM usage
- **Settings**: Environment variables
- **Domains**: Custom domain

### Database:
- SQLite database tự động tạo
- Lưu trữ metadata video
- Không mất dữ liệu khi restart

## 🔒 Bảo Mật & Giới Hạn

### Railway Free Plan:
- ✅ **500 hours/month** runtime
- ✅ **1GB RAM**
- ✅ **1GB storage**
- ✅ **Custom domain** support
- ⚠️ **Sleep sau 1h không activity**

### Lưu ý:
- File upload giới hạn 100MB/file
- Tổng storage 1GB (khoảng 10-20 video)
- App sleep nếu không dùng 1h

## 🚀 Nâng Cấp (Paid Plans)

### Railway Pro ($5/month):
- ⭐ **No sleep**
- ⭐ **Unlimited hours**
- ⭐ **8GB RAM**
- ⭐ **100GB storage**
- ⭐ **Priority support**

## 📞 Troubleshooting

### Lỗi thường gặp:
1. **Build failed**: Check requirements.txt
2. **App crash**: Check logs trong Railway
3. **File not found**: Check file paths
4. **Database error**: SQLite tự tạo

### Debug:
```bash
# Xem logs
railway logs

# Connect to app
railway shell
```

## 🎁 Tips Tối Ưu

1. **Giảm file size**: Compress video trước upload
2. **Cache static files**: Sử dụng CDN
3. **Monitor usage**: Check Railway metrics
4. **Backup database**: Download SQLite file định kỳ

## 🌟 Kết Quả Cuối Cùng

Sau khi deploy, bạn sẽ có:
- ✅ **Website public** cho mọi người truy cập
- ✅ **Upload/download** video thật
- ✅ **Database** lưu thông tin video  
- ✅ **Share links** video với bạn bè
- ✅ **Mobile responsive** interface
- ✅ **Real-time stats** và analytics

**Demo URL**: `https://your-videoshare-app.railway.app`

---
🎉 **Chúc mừng! Bạn đã có một nền tảng video sharing thật sự!** 🎉