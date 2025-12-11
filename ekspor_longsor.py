import tweepy
import pandas as pd
import time

# =========================================================
# ⚠ GANTI DENGAN BEARER TOKEN ANDA DI SINI! ⚠
# Bearer Token ini harus dirahasiakan!
BEARER_TOKEN = "YOUR_BEARER_TOKENAAAAAAAAAAAAAAAAAAAAAG625wEAAAAAlaa6w1fZ2M%2BYM%2BbmaBAJDdFII%2Bg%3DY7IGsPVI4qKIvkhHghtZU9QtaJE4qxgL10b1MZhR0AcDWcTTUl" 
# =========================================================

# --- 1. Inisialisasi Klien Tweepy ---
client = tweepy.Client(BEARER_TOKEN)

# --- 2. Parameter Pencarian Tanah Longsor ---
# Menggunakan query yang spesifik untuk Tanah Longsor di Indonesia
QUERY = '"tanah longsor" OR longsor OR tertimbun OR evakuasi lang:id -is:retweet' 
MAX_TWEETS_PER_REQUEST = 100 # Maksimal 100 per request pada akses dasar

# --- 3. Mengambil Data (search_recent_tweets) ---
tweets_data = []

print(f"Mulai mengambil tweet terbaru tentang Tanah Longsor...")

try:
    # Menggunakan search_recent_tweets (kompatibel dengan akses dasar)
    response = client.search_recent_tweets(
        query=QUERY,
        max_results=MAX_TWEETS_PER_REQUEST,
        tweet_fields=["created_at", "public_metrics"]
    )

    # Mengumpulkan data
    if response.data:
        for tweet in response.data:
            tweets_data.append([
                tweet.text,
                tweet.created_at,
                tweet.public_metrics['like_count'],
                tweet.public_metrics['retweet_count']
            ])
        print(f"Berhasil mengambil {len(tweets_data)} tweet terbaru.")
    else:
        print("Peringatan: Tidak ada tweet yang ditemukan dengan query ini.")

except tweepy.errors.TweepyException as e:
    print(f"ERROR API Tweepy: Terjadi masalah. Cek Bearer Token dan izin API.")
    print(e)
    exit()

# --- 4. Menyimpan ke CSV ---
df = pd.DataFrame(tweets_data, columns=['Text', 'Date', 'Likes', 'Retweets'])

# Simpan sebagai file baru
output_file = 'longsor_data_realtime.csv'
df.to_csv(output_file, index=False)

print("\n" + "="*50)
print(f"Selesai! Data tersimpan di: {output_file}")
print("==================================================")