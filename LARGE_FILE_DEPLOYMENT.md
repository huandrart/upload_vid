# 🚀 Deploy Video App với Heroku + AWS S3

## 🎯 Tại sao chọn Heroku + S3?
- ✅ **Easy deployment** với Git push
- ✅ **Unlimited storage** trên S3
- ✅ **File size**: Lên đến 5GB per file
- ✅ **CDN**: Fast delivery
- 💰 **Cost**: ~$7-15/tháng

## 📋 Setup Steps

### 1. Tạo AWS S3 Bucket
1. **Đăng ký AWS** (free tier 12 tháng)
2. **Tạo S3 bucket** cho video storage
3. **Setup IAM user** với S3 permissions
4. **Get credentials**: Access Key + Secret Key

### 2. Cài đặt dependencies
```bash
pip install boto3 python-dotenv
```

### 3. Cập nhật app.py cho S3
```python
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            filename,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': file.content_type
            }
        )
        return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
    except ClientError as e:
        print(f"S3 upload error: {e}")
        return None

# Update upload route
@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']
    
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        
        # Upload to S3 instead of local storage
        s3_url = upload_to_s3(file, filename)
        
        if s3_url:
            # Save to database with S3 URL
            video_data = {
                'id': str(uuid.uuid4()),
                'title': request.form.get('title'),
                'filename': filename,
                's3_url': s3_url,
                'file_size': file.content_length,
                # ... other fields
            }
            add_video_to_db(video_data)
            return jsonify({'success': True, 'video_id': video_data['id']})
        
    return jsonify({'error': 'Upload failed'}), 400
```

### 4. Environment Variables (.env)
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=us-east-1
```

### 5. Heroku Deployment
```bash
# Install Heroku CLI
npm install -g heroku

# Login and create app
heroku login
heroku create your-video-app

# Set environment variables
heroku config:set AWS_ACCESS_KEY_ID=your_key
heroku config:set AWS_SECRET_ACCESS_KEY=your_secret
heroku config:set AWS_BUCKET_NAME=your_bucket

# Deploy
git push heroku main
```

### 6. Updated requirements.txt
```
Flask==2.3.3
boto3==1.34.0
python-dotenv==1.0.0
gunicorn==21.2.0
# ... existing packages
```

## 💰 Cost Breakdown

### AWS S3:
- **Storage**: $0.023/GB/month
- **Transfer**: $0.09/GB (first 10TB)
- **Requests**: $0.0004/1000 requests
- **Example**: 100GB video = ~$2.5/month

### Heroku:
- **Hobby tier**: $7/month
- **No sleep**: 24/7 uptime
- **Custom domain**: Free

### Total: ~$10-15/month

## 🎯 Alternative: DigitalOcean (Cheaper)

### DigitalOcean Spaces + Droplet
```
- Droplet (1GB RAM): $6/month
- Spaces (250GB): $5/month
- CDN: Included
Total: $11/month
```

### Setup DigitalOcean:
1. **Create Droplet** (Ubuntu 22.04)
2. **Setup Spaces** bucket
3. **Deploy with docker**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

## 🌟 Recommendation

**For beginners**: Heroku + S3
**For cost-conscious**: DigitalOcean Spaces
**For enterprise**: AWS/GCP with CDN

## 🚀 Next Steps

1. **Choose platform**: Heroku+S3 or DigitalOcean
2. **Setup storage**: S3 bucket or DO Spaces
3. **Update code**: Integration with cloud storage
4. **Deploy**: Push to production
5. **Test**: Upload large videos (1-2GB)

## 📞 Need Help?

I can help you:
1. **Setup AWS S3** integration
2. **Deploy to Heroku** step by step
3. **Configure DigitalOcean** alternative
4. **Optimize** for large files

Choose your preferred option and I'll guide you through!