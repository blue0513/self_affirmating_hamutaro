# coding: UTF-8
from requests_oauthlib import OAuth1Session
import json
import requests
import sys
import urllib
import os.path
import time
import twitkey

# 別ファイルtwitkey.pyから必要な各パラメータ値を参照します。
twitter = OAuth1Session(twitkey.twkey["CONSUMER_KEY"],
                        twitkey.twkey["CONSUMER_SECRET"],
                        twitkey.twkey["ACCESS_TOKEN"],
                        twitkey.twkey["ACCESS_TOKEN_SECRET"]
)

User_Id = ""
Get_At_Once = 10
target_text = "そう思うだろハム太郎"
reply_word = "そうなのだ！！まったくもってその通りなのだ！！！"

params = {"count": Get_At_Once}
req = twitter.get("https://api.twitter.com/"
                  "1.1/statuses/user_timeline.json"
                  "?screen_name=%s&include_rts=false" % User_Id,
                  params=params)
timeline = json.loads(req.text)

def was_replied(tweet_id):
    f = open('.history')
    history = f.read().split()
    matches = [s for s in history if str(tweet_id) in s]
    f.close()
    return len(matches)

def is_containing(text):
    return text.find(target_text.decode("utf-8")) > -1

def write_in_history(tweet_id):
    f = open('.history', 'a+')
    f.write(str(tweet_id) + '\n')
    f.close()

def send_reply_to(tweet_id):
    post_url = "https://api.twitter.com/1.1/statuses/update.json"
    post_params = {
        "status": '@' + User_Id + reply_word,
        "in_reply_to_status_id": str(tweet_id)
    }
    twitter.post(post_url, params = post_params)
    print "done"

for tweet in timeline:
    if tweet["in_reply_to_status_id"] == None: # 他人へのリプライは弾く
        if not was_replied(tweet["id"]): # 過去にリプライ済みは弾く
            if is_containing(tweet["text"]): # 特定キーワードがあったらリプする
                send_reply_to(tweet["id"])
                write_in_history(tweet["id"])
