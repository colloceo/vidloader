from flask import Flask, request, send_file, Response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import yt_dlp
import uuid
import os
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import threading
import shutil

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('access.log')
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per minute"])

# Download folder
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Thread lock for concurrent downloads
download_lock = threading.Lock()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/download', methods=['POST'])
@limiter.limit("5 per minute")
def download():
    url = request.form.get('url')
    format_type = request.form.get('format')
    
    if not url or not format_type:
        logger.error("Missing URL or format")
        return jsonify({'error': 'Missing URL or format'}), 400

    filename_base = str(uuid.uuid4())
    extension = 'mp3' if format_type == 'audio' else 'mp4'
    filename = f"{filename_base}.{extension}"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'logger': logger,
        'ffmpeg_location': os.getenv('FFMPEG_PATH', './ffmpeg/ffmpeg'),
    }

    if format_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-loglevel', 'error', '-threads', '1', '-preset', 'ultrafast'],
        })
    else:
        ydl_opts['format'] = 'best[ext=mp4]/best'

    def download_with_ydl():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.error(f"yt_dlp download failed: {str(e)}")
            raise

    try:
        with download_lock:
            with ThreadPoolExecutor(max_workers=1) as executor:
                timeout = 600 if format_type == 'audio' and 'instagram.com' in url.lower() else 300
                future = executor.submit(download_with_ydl)
                future.result(timeout=timeout)

        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(filename_base):
                final_filename = f"{'audio' if format_type == 'audio' else 'video'}_{filename_base}.{extension}"
                file_path = os.path.join(DOWNLOAD_FOLDER, file)
                logger.debug(f"Sending file: {file_path}")

                def cleanup():
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            logger.debug(f"Deleted file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {str(e)}")

                response = send_file(
                    file_path,
                    as_attachment=True,
                    download_name=final_filename,
                    mimetype='audio/mpeg' if format_type == 'audio' else 'video/mp4'
                )
                response.call_on_close(cleanup)
                return response

        logger.error("File not found after download")
        return jsonify({'error': 'File not found after download'}), 500

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        logger.error(f"DownloadError: {error_msg}")
        if 'ffmpeg' in error_msg or 'ffprobe' in error_msg:
            logger.debug("Falling back to raw audio download")
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [],
                'ffmpeg_location': os.getenv('FFMPEG_PATH', './ffmpeg/ffmpeg'),
            })
            filename = f"{filename_base}.webm"
            output_path = os.path.join(DOWNLOAD_FOLDER, filename)
            try:
                with download_lock:
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(download_with_ydl)
                        future.result(timeout=180)

                for file in os.listdir(DOWNLOAD_FOLDER):
                    if file.startswith(filename_base):
                        final_filename = f"audio_{filename_base}.webm"
                        file_path = os.path.join(DOWNLOAD_FOLDER, file)
                        logger.debug(f"Sending fallback file: {file_path}")

                        def cleanup():
                            try:
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    logger.debug(f"Deleted file: {file_path}")
                            except Exception as e:
                                logger.error(f"Error deleting file {file_path}: {str(e)}")

                        response = send_file(
                            file_path,
                            as_attachment=True,
                            download_name=final_filename,
                            mimetype='audio/webm'
                        )
                        response.call_on_close(cleanup)
                        return response

                logger.error("Fallback file not found")
                return jsonify({'error': 'Fallback file not found'}), 500
            except Exception as fallback_e:
                logger.error(f"Fallback download failed: {str(fallback_e)}")
                return jsonify({'error': 'Audio download failed. Try video format.'}), 500
        elif 'sign in' in error_msg or 'login' in error_msg:
            return jsonify({'error': 'This content requires login. Please use a publicly accessible URL.'}), 403
        elif 'geo-restricted' in error_msg:
            return jsonify({'error': 'This content is geo-restricted and cannot be downloaded.'}), 403
        elif 'not available' in error_msg or 'unavailable' in error_msg:
            return jsonify({'error': 'The video is not available or private.'}), 404
        else:
            return jsonify({'error': f'Failed to download: {str(e)}'}), 500
    except TimeoutError:
        logger.error(f"Download timed out after {timeout} seconds")
        return jsonify({'error': 'Download timed out. Try a shorter video or select video format.'}), 504
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)