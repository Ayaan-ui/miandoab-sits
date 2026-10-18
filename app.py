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
<meta name="keywords" content="instagram video download, reels download, insta video saver, instagram downloader, videodropper alternative, download instagram reels hd">
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
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{{
    "@type": "Question",
    "name": "How to download Instagram videos?",
    "acceptedAnswer": {{"@type": "Answer","text": "Paste Instagram video URL in our downloader and click Download to save in HD without watermark."}}
  }},{{
    "@type": "Question",
    "name": "Is this Instagram downloader free?",
    "acceptedAnswer": {{"@type": "Answer","text": "Yes, 100% free, no watermark, no ads popups."}}
  }}]
}}
</script>
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
© 2026 VideoDropper - Best Instagram Video Downloader | No Watermark<br>
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
<h1>Instagram Video Downloader - HD</h1>
<p>Download Instagram Videos, Reels, Photos, Stories in HD without watermark. Fast, Free, No Ads.</p>
<div class="search-box">
<input id="urlInput" placeholder="https://www.instagram.com/reel/...">
<button id="dlBtn" onclick="downloadVideo()">Download</button>
</div>
<div id="error" style="color:red;margin-top:15px;display:none"></div>
<div id="result" class="result">
<video id="videoPreview" controls playsinline></video>
<a id="finalLink" class="download-btn" href="#" target="_blank" download>⬇️ Download Video (HD)</a>
<p style="font-size:12px;opacity:0.5;margin-top:10px">Long press video > Save Video on Mobile</p>
</div>

<!-- ADS PLACEHOLDER - Yahan Monetag / Adsterra ka code lagana -->
<div class="ad-box">AD SPACE - Paste Your Adsterra / Monetag Code Here - 300x250
<!-- <script> your ad code </script> -->
</div>

<div class="faq">
<h2>Why Choose Our VideoDropper?</h2>
<details><summary><b>1. How to download Instagram Reels?</b></summary><p style="margin-top:10px;opacity:0.7">Copy reel link from Instagram app > Paste here > Click Download > Save HD video.</p></details>
<details><summary><b>2. Is it safe and free?</b></summary><p style="margin-top:10px;opacity:0.7">Yes 100% free, safe, no login required, no watermark like VideoDropper.app</p></details>
<details><summary><b>3. Can I download private videos?</b></summary><p style="margin-top:10px;opacity:0.7">No, we only support public Instagram videos, reels and photos.</p></details>
<h2 style="margin-top:30px">How to Use Instagram Downloader - 3 Steps</h2>
<p style="opacity:0.7;line-height:1.6;margin-top:10px">Instagram video download is very easy. Our tool is best alternative to videodropper.app. Just copy the Instagram video link and paste it. Our server fetches the HD video URL using yt-dlp API and gives you direct download link. No need to install any app.</p>
</div>
</div>
<script>
async function downloadVideo(){
  let url = document.getElementById('urlInput').value.trim();
  if(!url.includes('instagram.com')){ showError('Please paste a valid Instagram link'); return; }
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
    return layout("Instagram Video Downloader - HD Reels, Photos, Story - No Watermark | VideoDropper", "Download Instagram Videos, Reels, Photos, Stories in HD without watermark. Fast, Free, No Login. Best VideoDropper Alternative 2026.", content)

@app.route('/about')
def about():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>About Us</h1><p style='margin-top:15px;opacity:0.8'>VideoDropper is a free Instagram video downloader tool launched in 2026. Our mission is to provide fast, clean, no-ads experience to download public Instagram content in HD. We do not host any copyrighted content. This is best alternative to videodropper.app</p></div>"
    return layout("About Us - VideoDropper", "About VideoDropper Instagram downloader", c)

@app.route('/privacy')
def privacy():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>Privacy Policy</h1><p style='margin-top:15px;opacity:0.8'>We do not store any videos. All videos are directly fetched from Instagram CDN. We do not collect personal data. We use cookies for ads (AdSense, Adsterra, Monetag). Contact us for any DMCA removal.</p></div>"
    return layout("Privacy Policy - VideoDropper", "Privacy Policy", c)

@app.route('/contact')
def contact():
    c = "<div style='margin-top:40px;line-height:1.7'><h1>Contact Us</h1><p style='margin-top:15px;opacity:0.8'>Email: support@yourdomain.com<br>If you have any copyright issue, please email us we will remove content in 24 hours.</p></div>"
    return layout("Contact Us - VideoDropper", "Contact Us", c)

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://yourdomain.com/</loc><priority>1.0</priority></url>
<url><loc>https://yourdomain.com/about</loc><priority>0.8</priority></url>
<url><loc>https://yourdomain.com/privacy</loc><priority>0.5</priority></url>
<url><loc>https://yourdomain.com/contact</loc><priority>0.5</priority></url>
</urlset>"""
    return Response(xml, mimetype='text/xml')

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: https://yourdomain.com/sitemap.xml", mimetype='text/plain')

@app.route('/api/download', methods=['POST'])
def download_api():
    try:
        insta_url = request.get_json().get('url','')
        ydl_opts = {'quiet': True,'no_warnings': True,'format': 'best','noplaylist': True,}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(insta_url, download=False)
            video_url = info.get('url') or info.get('entries',[{}])[0].get('url') or info.get('formats', [{}])[-1].get('url')
            if not video_url: return jsonify({"error": "Could not extract. Public link use karein."}), 400
            return jsonify({"video_url": video_url})
    except Exception as e:
        return jsonify({"error": f"Failed: {str(e)[:100]}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
