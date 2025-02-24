from django.shortcuts import render
from yt_dlp import YoutubeDL
import os
from moviepy.editor import VideoFileClip

def download_video(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with YoutubeDL({'outtmpl': f'{output_dir}/%(title)s.%(ext)s'}) as ydl:
        ydl.download([url])
    
    # Return the path of the downloaded video
    downloaded_files = os.listdir(output_dir)
    return next((os.path.join(output_dir, f) for f in downloaded_files if f.endswith(('.mp4', '.webm', '.mkv'))), None)

def convert_video_to_mp3(video_path):
    mp3_path = os.path.splitext(video_path)[0] + '.mp3'
    with VideoFileClip(video_path) as clip:
        clip.audio.write_audiofile(mp3_path)
    return mp3_path

def home(request):
    result = ""
    converted_message = ""
    video_path = request.session.get('video_path')  # Get the video path from session

    if request.method == "POST":
        if 'download' in request.POST:
            url = request.POST.get('url')
            output_dir = 'downloads'
            
            video_path = download_video(url, output_dir)  # Download video
            if video_path:
                request.session['video_path'] = video_path  # Store video path in session
                result = "Download complete!"
            else:
                result = "Download failed: No video found."
        
        elif 'convert' in request.POST and video_path:  # Handle conversion
            mp3_path = convert_video_to_mp3(video_path)
            converted_message = f"MP3 saved at: {mp3_path}"

    return render(request, 'myapp/home.html', {
        'result': result,
        'converted_message': converted_message,
        'video_path': video_path
    })