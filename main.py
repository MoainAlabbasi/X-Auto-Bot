import tweepy
import os
import sys
import json

class XAutoBot:
    def __init__(self):
        self.api_key = os.getenv("X_API_KEY")
        self.api_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("⚠️ خطأ: مفاتيح X API مفقودة في متغيرات البيئة!")
        # v2 client (posting)
        self.client = tweepy.Client(
            consumer_key=self.api_key, consumer_secret=self.api_secret,
            access_token=self.access_token, access_token_secret=self.access_token_secret,
        )
        # v1.1 api (media upload)
        auth = tweepy.OAuth1UserHandler(
            self.api_key, self.api_secret, self.access_token, self.access_token_secret
        )
        self.api_v1 = tweepy.API(auth)

    def post_tweet(self, text, media_path=None):
        media_ids = None
        if media_path and os.path.isfile(media_path):
            media = self.api_v1.media_upload(media_path)
            media_ids = [media.media_id]
            print(f"🖼️ تم رفع الصورة: media_id={media.media_id}")
        resp = self.client.create_tweet(text=text, media_ids=media_ids)
        tid = resp.data['id']
        print(f"✅ تم النشر! https://x.com/i/web/status/{tid}")
        return resp.data

    def get_account_report(self):
        u = self.client.get_me(user_fields=['public_metrics'])
        if u.data:
            m = u.data.public_metrics
            print(f"📊 @{u.data.username}: {m['followers_count']} متابع، {m['tweet_count']} تغريدة.")
            return {"username": u.data.username, **m}

if __name__ == "__main__":
    bot = XAutoBot()
    mode = os.getenv("MODE", "report").strip()
    if mode == "post":
        text = os.getenv("TWEET_TEXT", "").strip()
        media = os.getenv("MEDIA_PATH", "").strip() or None
        if not text:
            print("⚠️ TWEET_TEXT فارغ"); sys.exit(1)
        bot.post_tweet(text, media)
    else:
        bot.get_account_report()
