import tweepy
import os
import json

class XAutoBot:
    def __init__(self):
        # سحب المفاتيح من متغيرات البيئة (Environment Variables)
        # هذا هو المكان الذي سيقرأ فيه الكود المفاتيح من GitHub Secrets
        self.api_key = os.getenv("X_API_KEY")
        self.api_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        # التحقق من وجود المفاتيح قبل البدء
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("⚠️ خطأ: لم يتم العثور على مفاتيح X API المطلوبة في متغيرات البيئة!")

        # إعداد المصادقة
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def post_tweet(self, text):
        """نشر تغريدة جديدة على حساب X."""
        try:
            response = self.client.create_tweet(text=text)
            print(f"✅ تم النشر بنجاح! ID: {response.data['id']}")
            return response.data
        except Exception as e:
            print(f"❌ خطأ أثناء النشر: {e}")
            return None

    def get_account_report(self):
        """جلب تقرير إحصائي عن الحساب."""
        try:
            user = self.client.get_me(user_fields=['public_metrics', 'description', 'created_at'])
            if user.data:
                metrics = user.data.public_metrics
                report = {
                    "username": user.data.username,
                    "followers": metrics['followers_count'],
                    "following": metrics['following_count'],
                    "tweets": metrics['tweet_count']
                }
                print(f"📊 تقرير الحساب لـ @{report['username']}: {report['followers']} متابع، {report['tweets']} تغريدة.")
                return report
            return None
        except Exception as e:
            print(f"❌ خطأ أثناء جلب التقرير: {e}")
            return None

if __name__ == "__main__":
    # هذا الجزء لتجربة البوت محلياً أو من قبل الوكلاء الأذكياء
    try:
        bot = XAutoBot()
        bot.get_account_report()
    except Exception as e:
        print(e)
