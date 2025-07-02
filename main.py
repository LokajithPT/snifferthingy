# server.py
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    jsonify,
)
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "dns_logs.db"
# List of sus/blacklisted domains
SUS_DOMAINS = {
    # 🔴 Time-wasting video & entertainment
    "www.youtube.com",
    "www.tiktok.com",
    "www.netflix.com",
    "www.primevideo.com",
    "www.hotstar.com",
    "www.hulu.com",
    "www.crunchyroll.com",
    "www.dailymotion.com",
    # 🔞 NSFW/adult content
    "www.pornhub.com",
    "www.xvideos.com",
    "www.xnxx.com",
    "www.redtube.com",
    "www.youporn.com",
    "www.youjizz.com",
    "www.spankbang.com",
    # 🧠 Social media distractions
    "www.facebook.com",
    "www.instagram.com",
    "www.twitter.com",
    "www.snapchat.com",
    "www.reddit.com",
    "www.pinterest.com",
    "www.discord.com",
    # 🎮 Gaming platforms / streaming
    "www.twitch.tv",
    "www.roblox.com",
    "www.epicgames.com",
    "www.steampowered.com",
    "www.miniclip.com",
    "www.leagueoflegends.com",
    # 💸 Shady or time-wasting shopping
    "www.shein.com",
    "www.temu.com",
    "www.wish.com",
    "www.alibaba.com",
    "www.aliexpress.com",
    "www.flipkart.com",
    "www.amazon.in",
    # ☠️ Sketchy sites or general distractions
    "www.omegle.com",
    "www.9gag.com",
    "www.quora.com",
    "www.ask.fm",
    "www.tumblr.com",
    "www.buzzfeed.com",
}


@app.route("/api/logs")
def api_logs():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dns_requests ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        timestamp, ip, domain = row
        is_sus = domain.lower() in SUS_DOMAINS
        logs.append(
            {"timestamp": timestamp, "ip": ip, "domain": domain, "is_sus": is_sus}
        )

    return jsonify(logs)


# Init DB
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dns_requests (
        timestamp TEXT,
        ip TEXT,
        domain TEXT
    )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/clear", methods=["POST"])
def clear_logs():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dns_requests")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# Endpoint to receive DNS logs
@app.route("/log", methods=["POST"])
def log():
    data = request.json
    ip = data.get("ip")
    domain = data.get("domain")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if ip and domain:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO dns_requests (timestamp, ip, domain) VALUES (?, ?, ?)",
            (timestamp, ip, domain),
        )
        conn.commit()
        conn.close()

        if any(sus_domain in domain.lower() for sus_domain in SUS_DOMAINS):
            print(f"⚠️ Sus domain detected: {domain} from {ip}")

        return "Logged", 200

    return "Invalid data", 400


# Web page to view logs
@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dns_requests ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return render_template("index.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
