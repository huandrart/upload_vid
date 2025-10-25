from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import uuid
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Tạo thư mục uploads nếu chưa có
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Định dạng video được phép
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}

def allowed_file(filename):
    """Kiểm tra file có được phép upload không"""
    if not filename or '.' not in filename:
        return False
    
    file_extension = filename.rsplit('.', 1)[1].lower()
    return file_extension in ALLOWED_EXTENSIONS

def init_db():
    """Khởi tạo database"""
    conn = sqlite3.connect('video_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            platform TEXT,
            upload_date TEXT,
            uploader_name TEXT,
            file_size INTEGER,
            views INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_videos():
    """Lấy tất cả video từ database"""
    conn = sqlite3.connect('video_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, description, filename, platform, 
               upload_date, uploader_name, file_size, views 
        FROM videos ORDER BY upload_date DESC
    ''')
    
    videos = []
    for row in cursor.fetchall():
        videos.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'filename': row[3],
            'platform': row[4],
            'upload_date': row[5],
            'uploader_name': row[6],
            'file_size': row[7],
            'views': row[8]
        })
    
    conn.close()
    return videos

def add_video_to_db(video_data):
    """Thêm video vào database"""
    try:
        conn = sqlite3.connect('video_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos (id, title, description, filename, platform, 
                              upload_date, uploader_name, file_size, views)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_data['id'],
            video_data['title'],
            video_data['description'],
            video_data['filename'],
            video_data['platform'],
            video_data['upload_date'],
            video_data['uploader_name'],
            video_data['file_size'],
            0
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        if 'conn' in locals():
            conn.close()
        raise e

def increment_views(video_id):
    """Tăng số lượt xem"""
    conn = sqlite3.connect('video_database.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE videos SET views = views + 1 WHERE id = ?', (video_id,))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Trang chủ - hiển thị tất cả video"""
    videos = get_all_videos()
    return render_template('index.html', videos=videos)

@app.route('/upload')
def upload_page():
    """Trang upload video"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Xử lý upload video"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'Không có file video nào được chọn'}), 400
        
        file = request.files['video']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        platform = request.form.get('platform', 'Website')
        uploader_name = request.form.get('uploader_name', 'Anonymous').strip()
        
        if file.filename == '':
            return jsonify({'error': 'Không có file nào được chọn'}), 400
        
        if not title:
            return jsonify({'error': 'Vui lòng nhập tiêu đề video'}), 400
        
        if file and allowed_file(file.filename):
            try:
                # Tạo tên file an toàn
                original_filename = secure_filename(file.filename)
                if '.' not in original_filename:
                    return jsonify({'error': 'File không có extension hợp lệ'}), 400
                
                file_extension = original_filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                
                # Lưu file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                # Lấy kích thước file
                file_size = os.path.getsize(file_path)
                
                # Thêm vào database
                video_data = {
                    'id': str(uuid.uuid4()),
                    'title': title,
                    'description': description,
                    'filename': unique_filename,
                    'platform': platform,
                    'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'uploader_name': uploader_name,
                    'file_size': file_size
                }
                
                add_video_to_db(video_data)
                
                return jsonify({
                    'success': True,
                    'message': 'Video đã được upload thành công!',
                    'video_id': video_data['id']
                })
            except Exception as e:
                # Xóa file nếu có lỗi
                if 'file_path' in locals() and os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({'error': f'Lỗi xử lý file: {str(e)}'}), 500
        
        return jsonify({'error': 'Định dạng file không được hỗ trợ'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Lỗi server: {str(e)}'}), 500

@app.route('/video/<video_id>')
def watch_video(video_id):
    """Trang xem video"""
    conn = sqlite3.connect('video_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
    video_row = cursor.fetchone()
    
    if not video_row:
        conn.close()
        return "Video không tồn tại", 404
    
    video = {
        'id': video_row[0],
        'title': video_row[1],
        'description': video_row[2],
        'filename': video_row[3],
        'platform': video_row[4],
        'upload_date': video_row[5],
        'uploader_name': video_row[6],
        'file_size': video_row[7],
        'views': video_row[8]
    }
    
    # Tăng lượt xem
    increment_views(video_id)
    video['views'] += 1
    
    conn.close()
    return render_template('video.html', video=video)

@app.route('/stream/<filename>')
def stream_video(filename):
    """Stream video file"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=False,
            mimetype='video/mp4'
        )
    except FileNotFoundError:
        return "File không tồn tại", 404

@app.route('/api/stats')
def get_stats():
    """API lấy thống kê"""
    conn = sqlite3.connect('video_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM videos')
    total_videos = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(views) FROM videos')
    total_views = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(file_size) FROM videos')
    total_size = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'total_videos': total_videos,
        'total_views': total_views,
        'total_size_mb': round(total_size / (1024 * 1024), 2)
    })

if __name__ == '__main__':
    init_db()
    # Support for Heroku deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)