from flask import Flask, Response, request, jsonify
import yt_dlp

app = Flask(__name__)

# --- MAIN SEO TEMPLATE ---
def layout(title, description, content):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="video downloader, instagram downloader, tiktok downloader, facebook video downloader, youtube downloader, all in one downloader">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://yourdomain.com/">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif}}
body{{background:#fff;color:#111;}}
.container{{max-width:800px;margin:0 auto;padding:20px}}
.header{{display:flex;justify-content:space-between;align-items:center;padding:18px 0;border-bottom:1px solid #eee}}
.logo{{font-weight:800;font-size:22px}} .logo span{{background:#111;color:white;padding:2px 8px;border-radius:8px}}
.nav a{{margin-left:15px;text-decoration:none;color:#111;font-size:13px;opacity:0.7}}
.hero{{text-align:center;margin-top:50px}}
.hero h1{{font-size:44px;font-weight:800;line-height:1.05;letter-spacing:-1.5px}}
.hero p{{margin-top:12px;opacity:0.6;font-size:16px}}
.search-box{{margin-top:30px;background:#f3f3f5;border:1px solid #e5e5e5;border-radius:16px;padding:8px;display:flex;gap:8px}}
.search-box input{{flex:1;border:none;background:transparent;padding:14px 16px;font-size:16px;outline:none}}
.search-box button{{background:#111;color:white;border:none;padding:14px 26px;border-radius:12px;font-weight:700;cursor:pointer}}
.result{{display:none;margin-top:25px;background:#fafafa;border:1px solid #eee;border-radius:20px;padding:20px;text-align:center}}
.result video{{width:100%;max-height:500px;border-radius:16px;background:black}}
.download-btn{{display:block;margin-top:16px;background:#111;color:white;text-align:center;padding:16px;border-radius:12px;text-decoration:none;font-weight:700}}
.ad-box{{background:#f9f9f9;border:1px dashed #ccc;border-radius:12px;padding:20px;margin:20px 0;text-align:center;font-size:12px;opacity:0.6}}
.faq{{text-align:left;margin-top:60px}} .faq h2{{font-size:22px;margin-bottom:15px}} .faq details{{background:#f9f9f9;padding:15px;border-radius:12px;margin-bottom:10px}}
.footer{{text-align:center;margin-top:60px;padding:20px 0;border-top:1px solid #eee;opacity:0.6;font-size:12px}}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="logo">📥 <span>Video</span>Dropper</div>
<div class="nav">
<a href="/">Home</a><a href="/about">About</a><a href="/privacy">Privacy</a><a href="/contact">Contact</a>
</div>
</div>
{content}
<div class="footer">
© 2026 VideoDropper - All Video Downloader | No Watermark<br>
<a href="/about">About</a> | <a href="/privacy">Privacy</a> | <a href="/contact">Contact</a> | <a href="/sitemap.xml">Sitemap</a>
<br><br>Disclaimer: This tool is for public videos only. We do not host any content.
</div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
<div class="hero">
<h1>All Video Downloader - HD</h1>
<p>Download Instagram, TikTok, Facebook, YouTube, Twitter Videos in HD without watermark. Fast & Free.</p>
<div class="search-box">
<input id="urlInput" placeholder="Paste any link - Instagram / TikTok / FB / YouTube...">
<button id="dlBtn" onclick="downloadVideo()">Download</button>
</div>
<div id="error" style="color:red;margin-top:15px;display:none"></div>
<div id="result" class="result">
<video id="videoPreview" controls playsinline></video>
<a id="finalLink" class="download-btn" href="#" target="_blank" download>⬇️ Download Video (HD)</a>
<p style="font-size:12px;opacity:0.5;margin-top:10px">Long press video > Save Video on Mobile</p>
</div>

<div class="ad-box">AD SPACE - Paste Your Adsterra / Monetag Code Here - 300x250</div>

<div class="faq">
<h2>Supported Platforms</h2>
<p style="opacity:0.7">✅ Instagram Reels, Stories ✅ TikTok No Watermark ✅ Facebook Reels & Videos ✅ YouTube Shorts & Videos ✅ Twitter / X</p>
<h2 style="margin-top:30px">How to Use - 3 Steps</h2>
<p style="opacity:0.7;line-height:1.6;margin-top:10px">Copy any video link and paste here. Our server fetches HD video URL using yt-dlp API. Supports 1000+ sites.</p>
</div>
</div>
<script>
async function downloadVideo(){
  let url = document.getElementById('urlInput').value.trim();
  if(url.length < 10){ showError('Please paste a valid link'); return; }
  let btn = document.getElementById('dlBtn'); btn.innerText = 'Fetching...'; btn.disabled = true;
  document.getElementById('error').style.display='none'; document.getElementById('result').style.display='none';
  try{
    let res = await fetch('/api/download', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({url:url}) });
    let data = await res.json();
    if(data.error){ showError(data.error); }
    else{
      document.getElementById('videoPreview').src = data.video_url;
      document.getElementById('finalLink').href = data.video_url;
      document.getElementById('result').style.display='block';
    }
  }catch(e){ showError('Server error, try again'); }
  btn.innerText='Download'; btn.disabled=false;
}
function showError(msg){ let el=document.getElementById('error'); el.innerText=msg; el.style.display='block'; }
</script>
"""
    return layout("All Video Downloader - Instagram, TikTok, Facebook, YouTube - HD No Watermark", "Download any video from Instagram, TikTok, Facebook, YouTube, Twitter in HD without watermark. Free All-in-One downloader.", content)

@app.route('/about')
def about():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>About Us</h1><p style='margin-top:15px;opacity:0.8'>VideoDropper is a free all-in-one video downloader. Supports 1000+ sites via yt-dlp.</p></div>"
    return layout("About Us - VideoDropper", "About VideoDropper", c)

@app.route('/privacy')
def privacy():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>Privacy Policy</h1><p style='margin-top:15px;opacity:0.8'>We do not store any videos. All videos are directly fetched from CDN.</p></div>"
    return layout("Privacy Policy - VideoDropper", "Privacy Policy", c)

@app.route('/contact')
def contact():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>Contact Us</h1><p style='margin-top:15px;opacity:0.8'>Email: support@yourdomain.com</p></div>"
    return layout("Contact Us - VideoDropper", "Contact Us", c)

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://yourdomain.com/</loc><priority>1.0</priority></url>
</urlset>"""
    return Response(xml, mimetype='text/xml')

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: https://yourdomain.com/sitemap.xml", mimetype='text/plain')

@app.route('/api/download', methods=['POST'])
def download_api():
    try:
        insta_url = request.get_json
