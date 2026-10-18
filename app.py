from flask import Flask, request, jsonify
import requests, re
import yt_dlp

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Video Dropper - All Video Downloader</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;text-align:center;padding:20px;background:#fff}
.box{max-width:500px;margin:50px auto}
input{width:70%;padding:15px;border-radius:10px;border:2px solid #ddd}
button{padding:15px 20px;background:#000;color:#fff;border-radius:10px;border:0;margin-left:5px}
h1{font-size:32px;font-weight:900}
</style>
</head>
<body>
<div class="box">
<h1>📥 Video Dropper - ALL Video Downloader</h1>
<p>Download TikTok, Instagram, Facebook, YouTube in HD</p>
<input id="url" placeholder="Paste any video link (TikTok, Insta, FB, YT)...">
<button onclick="download()">Download</button>
<p id="result"></p>
</div>
<script>
async function download(){
 let u=document.getElementById('url').value;
 if(!u){alert('Paste link');return}
 document.getElementById('result').innerText='Processing...';
 let res=await fetch('/download?url='+encodeURIComponent(u));
 let data=await res.json();
 if(data.url){
   document.getElementById('result').innerHTML='<a href=\"'+data.url+'\" target=\"_blank\" style=\"background:green;color:white;padding:10px;display:block;border-radius:10px;text-decoration:none\">✅ Click to Download HD Video</a><br>'+data.title;
 }else{
   document.getElementById('result').innerText='Error: '+data.error;
 }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/download')
def dl():
    url = request.args.get('url','')
    if not url:
        return jsonify({"error":"No url"}), 400
    try:
        # Resolve short TikTok links
        if 'vt.tiktok.com' in url or 'vm.tiktok.com' in url:
            r = requests.get(url, allow_redirects=True, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
            url = r.url
        
        ydl_opts = {'quiet':True,'no_warnings':True,'format':'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url') or info.get('entries',[{}])[0].get('url') or info['formats'][-1]['url']
            title = info.get('title','Video')
            return jsonify({"url":video_url,"title":title})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == '__main__':
    app.run()
