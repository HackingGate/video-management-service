from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
# Use the environment variable for UPLOAD_FOLDER if it's set, otherwise default to a local folder
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './test-video')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024  # 10GB max-limit.


# Home page route
@app.route('/')
def index():
    # list all videos in the UPLOAD_FOLDER, filter out non-video files
    videos = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.m3u8')]
    return render_template('index.html', videos=videos)


# Upload video route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert video to HLS format
        output_m3u8 = os.path.splitext(file_path)[0] + '.m3u8'
        segment_prefix = os.path.splitext(file_path)[0] + '_segment'
        ffmpeg_command = [
            'ffmpeg', '-i', file_path, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-sc_threshold', '0', '-g',
            '48', '-keyint_min', '48', '-hls_time', '10', '-hls_playlist_type', 'vod', '-b:v', '2000k', '-maxrate',
            '2147k', '-bufsize', '2000k', '-b:a', '128k', '-hls_segment_filename', f"{segment_prefix}%03d.ts",
            output_m3u8
        ]
        subprocess.run(ffmpeg_command)

        return redirect(url_for('index'))


# Delete video route
@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))


# Route for serving videos
@app.route('/video/<filename>')
def video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='::'
    )
