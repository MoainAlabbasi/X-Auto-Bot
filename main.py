import tweepy
import os
import sys
import json

class XAutoBot:
    def __init__(self):
        # سحب المفاتيح من متغيرات البيئة (GitHub Secrets)
        self.api_key = os.getenv("X_API_KEY")
        self.api_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("⚠️ خطأ: لم يتم العثور على مفاتيح X API المطلوبة في متغيرات البيئة!")

        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    def post_tweet(self, text):
        """نشر تغريدة جديدة على حساب X."""
        try:
            response = self.client.create_tweet(text=text)
            print(f"✅ تم النشر بنجاح! ID: {response.data['id']}")
            return response.data
        except Exception as e:
            print(f"❌ خطأ أثناء النشر: {e}")
            raise

    def post_thread(self, tweets):
        """نشر سلسلة تغريدات (Thread)."""
        last_id = None
        ids = []
        for t in tweets:
            resp = self.client.create_tweet(text=t, in_reply_to_tweet_id=last_id)
            last_id = resp.data["id"]
            ids.append(last_id)
            print(f"✅ تغريدة في السلسلة: {last_id}")
        return ids

    def get_account_report(self):
        """جلب تقرير إحصائي عن الحساب."""
        try:
            user = self.client.get_me(user_fields=['public_metrics', 'description', 'created_at'])
            if user.data:
                m = user.data.public_metrics
                print(f"📊 @{user.data.username}: {m['followers_count']} متابع، {m['tweet_count']} تغريدة.")
                return {"username": user.data.username, **m}
            return None
        except Exception as e:
            print(f"❌ خطأ أثناء جلب التقرير: {e}")
            return None


if __name__ == "__main__":
    bot = XAutoBot()
    # الوضع: post (نشر) أو report (تقرير) أو thread
    mode = os.getenv("MODE", "report").strip()
    if mode == "post":
        text = os.getenv("TWEET_TEXT", "").strip()
        if not text:
            print("⚠️ لا يوجد نص تغريدة (TWEET_TEXT فارغ).")
            sys.exit(1)
        bot.post_tweet(text)
    elif mode == "thread":
        raw = os.getenv("THREAD_JSON", "[]")
        tweets = json.loads(raw)
        bot.post_thread(tweets)
    else:
        bot.get_account_report()
