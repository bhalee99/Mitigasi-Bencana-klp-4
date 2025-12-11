import tweepy
import pandas as pd

# =========================================================
# ⚠ GANTI DENGAN BEARER TOKEN ANDA DI SINI! ⚠
# Bearer Token ini harus dirahasiakan!
BEARER_TOKEN = "YOUR_BEARER_TOKENAAAAAAAAAAAAAAAAAAAAAG625wEAAAAAlaa6w1fZ2M%2BYM%2BbmaBAJDdFII%2Bg%3DY7IGsPVI4qKIvkhHghtZU9QtaJE4qxgL10b1MZhR0AcDWcTTUl"
# =========================================================

# --- 1. Inisialisasi Klien Tweepy ---
client = tweepy.Client(BEARER_TOKEN)

# --- 2. Parameter Pencarian BANJIR ---
# Query spesifik banjir di Indonesia (bahasa Indonesia)
QUERY = '"banjir" OR "banjir bandang" OR "terendam" OR "genangan" OR "evakuasi banjir" lang:id -is:retweet'
MAX_TWEETS_PER_REQUEST = 100  # Maksimal 100 per request pada akses dasar

# --- 3. Mengambil Data (search_recent_tweets) ---
tweets_data = []

print("Mulai mengambil tweet terbaru tentang BANJIR...")

try:
    response = client.search_recent_tweets(
        query=QUERY,
        max_results=MAX_TWEETS_PER_REQUEST,
        tweet_fields=["created_at", "public_metrics"]
    )

    if response.data:
        for tweet in response.data:
            tweets_data.append([
                tweet.text,
                tweet.created_at,
                tweet.public_metrics.get("like_count", 0),
                tweet.public_metrics.get("retweet_count", 0),
            ])
        print(f"Berhasil mengambil {len(tweets_data)} tweet terbaru.")
    else:
        print("Peringatan: Tidak ada tweet yang ditemukan dengan query ini.")

except tweepy.errors.TweepyException as e:
    print("ERROR API Tweepy: Terjadi masalah. Cek Bearer Token dan izin API.")
    print(e)
    raise SystemExit(1)

# --- 4. Menyimpan ke CSV ---
df = pd.DataFrame(tweets_data, columns=["Text", "Date", "Likes", "Retweets"])

output_file = "banjir_data_realtime.csv"
df.to_csv(output_file, index=False)

print("\n" + "="*50)
print(f"Selesai! Data tersimpan di: {output_file}")
print("="*50)
