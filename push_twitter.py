import json
import requests
import feedparser
import os

CONFIG_FILE = "config.json"
STATE_FILE = "state.json"

# 读取配置
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

# 读取上次抓取状态
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {}

for account in config["accounts"]:
    twitter_user = account["twitter"]
    webhook_url = account["webhook"]

    nitter_url = f"https://nitter.net/{twitter_user}/rss"
    feed = feedparser.parse(nitter_url)

    if twitter_user not in state:
        state[twitter_user] = []

    new_posts = []
    for entry in feed.entries:
        if entry.id not in state[twitter_user]:
            new_posts.append(entry)
            state[twitter_user].append(entry.id)

    # 发送到企业微信
    for post in reversed(new_posts):
        content = f"{post.title}\n{post.link}"
        requests.post(webhook_url, json={"msgtype": "text", "text": {"content": content}})

# 保存状态
with open(STATE_FILE, "w") as f:
    json.dump(state, f)
