from flask import Flask, request, jsonify, session, redirect
import requests, datetime
import yt_dlp

app = Flask(__name__)
app.secret_key = "ayaan_secret_123"

# Simple database (memory me)
STATS = {"visits": 0, "downloads": []}

HTML_PAGE = """
<!DOCTYPE html><html><head><title>Video Dropper</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;text-align:center;padding:20px}
.box{max-width:500px;margin:50px auto}input{width:70%;padding:15px;border-radius:10px;border:2px solid #ddd}
button{padding:15px 20px;background:#000;color:#fff;border-radius:10px;border:0;cursor:pointer}</style>
</head><body><div class="box">
<h1>Video Dropper - ALL Video Downloader</h1>
<p>TikTok, Insta, FB, YT</p>
<input id="url" placeholder="Paste video link...">
<button onclick="download()">Download</button>
<p id="result"></p>
<a href="/admin" style="font-size:12px;margin-top:30px;display:block">Admin Login</a>
</div>
<script>
async function download(){
 let u=document.getElementById('url').value;
 if(!u){alert('Paste link');return}
 document.getElementById('result').innerText='Processing...';
 let res=await fetch('/download?url='+encodeURIComponent(u));
 let data=await res.json();
 if(data.url){
   document.getElementById('result').innerHTML='<a href="'+data.url+'" target="_blank" style="background:green;color:white;padding:15px;display:block;border-radius:10px;text-decoration:none">Download HD Video</a><br>'+data.title;
 }else{
   document.getElementById('result').innerText='Error: '+data.error;
 }
}
</script></body></html>
"""

LOGIN_HTML = """
<div style="max-width:350px;margin:100px auto;font-family:Arial;text-align:center;border:1px solid #ddd;padding:30px;border-radius:15px">
<h2>Admin Login</h2>
<form method="POST">
<input name="user" placeholder="Username" style="width:90%;padding:12px;margin:10px"><br>
<input name="pass" type="password" placeholder="Password" style="width:90%;padding:12px;margin:10px"><br>
<button style="padding:12px 25px;background:black;color:white;border:0;border-radius:8px">Login</button>
</form></div>
"""

@app.route('/')
def home():
    STATS["visits"] += 1
    return HTML_PAGE

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('user') == 'ayaan' and request.form.get('pass') == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            return LOGIN_HTML + "<p style='color:red'>Wrong password</p>"
    if not session.get('admin'):
        return LOGIN_HTML
    
    html = f"""
    <div style="font-family:Arial;max-width:800px;margin:20px auto">
    <h1>Admin Dashboard</h1>
    <h3>Total Visits: {STATS['visits']}</h3>
    <h3>Total Downloads: {len(STATS['downloads'])}</h3>
    <a href="/logout">Logout</a><hr>
    <table border=1 width=100% cellpadding=8><tr><th>Time</th><th>Platform</th><th>Title</th></tr>
    """
    for d in reversed(STATS['downloads'][-50:]):
        html += f"<tr><td>{d['time']}</td><td>{d['platform']}</td><td>{d['title'][:50]}</td></tr>"
    html += "</table></div>"
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

@app.route('/download')
def dl():
    url = request.args.get('url','').strip()
    if not url: return jsonify({"error":"No url"}), 400
    try:
        platform = "Other"
        if "tiktok" in url: platform="TikTok"
        elif "instagram" in url: platform="Instagram"
        elif "facebook" in url or "fb.watch" in url: platform="Facebook"
        elif "youtube" in url or "youtu.be" in url: platform="Youtube"

        if 'vt.tiktok.com' in url or 'vm.tiktok.com' in url:
            try:
                r = requests.get(url, allow_redirects=True, timeout=15, headers={'User-Agent':'Mozilla/5.0'})
                url = r.url
            except: pass
        if 'tiktok.com' in url:
            try:
                api_url = "https://www.tikwm.com/api/"
                res = requests.post(api_url, data={"url": url}, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
                d = res.json()
                if d.get('code') == 0:
                    vurl = d['data'].get('hdplay') or d['data'].get('play')
                    title = d['data'].get('title','TikTok')
                    if vurl:
                        STATS["downloads"].append({"time":datetime.datetime.now().strftime("%H:%M %d-%m"),"platform":platform,"title":title})
                        return jsonify({"url": vurl, "title": title})
            except Exception as e:
                print(e)
        ydl_opts = {'quiet':True,'no_warnings':True,'format':'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            vurl = info.get('url') or info['formats'][-1]['url']
            title = info.get('title','Video')
            STATS["downloads"].append({"time":datetime.datetime.now().strftime("%H:%M %d-%m"),"platform":platform,"title":title})
            return jsonify({"url": vurl, "title": title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
