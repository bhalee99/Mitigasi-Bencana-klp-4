import tweepy
import pandas as pd
import time

# =========================================================
# ⚠ BEARER TOKEN ANDA ⚠
# Token ini sudah diisi dari input Anda. Pastikan token ini valid dan rahasia!
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMLheAAAAAAA0%2BuSeid%2BULvsea4JtiGRiSDSJSI%3DEUifiRBkKG5E2XzMDjRfl76ZC9Ub0wnz4XsNiRVBChTYbJcE3F" 
# =========================================================

# --- 1. Inisialisasi Klien Tweepy ---
# Menggunakan API V2 yang direkomendasikan X
client = tweepy.Client(BEARER_TOKEN)

# --- 2. Parameter Pencarian GEMPA BUMI ---
# Query disesuaikan untuk Gempa Bumi di Indonesia
# Mencari: Gempa, Guncangan, Korban, Kerusakan, Aman
QUERY = 'gempa OR "gempa bumi" OR guncangan OR kerusakan OR aman lang:id -is:retweet' 
MAX_TWEETS = 1500 # Jumlah maksimum tweet yang ingin Anda ambil

# Tanggal setelah 1 Januari 2024
START_TIME = "2024-01-01T00:00:00Z" 

# --- 3. Mengambil Data ---
tweets_data = []

print(f"Mulai mengambil {MAX_TWEETS} tweet tentang Gempa Bumi...")

try:
    # PERINGATAN: search_all_tweets membutuhkan akses berbayar. Jika gagal, gunakan search_recent_tweets.
    response = client.search_all_tweets(
        query=QUERY,
        start_time=START_TIME,
        max_results=500, # Max per request
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
        print(f"Berhasil mengambil {len(tweets_data)} tweet.")
    else:
        print("Tidak ada data ditemukan dengan query tersebut.")

except tweepy.errors.TweepyException as e:
    print(f"ERROR API Tweepy: Terjadi masalah dengan permintaan Anda. Cek token dan izin API.")
    print(e)
    exit()

# --- 4. Menyimpan ke CSV ---
df = pd.DataFrame(tweets_data, columns=['Text', 'Date', 'Likes', 'Retweets'])

# Nama file disesuaikan
output_file = 'gempa_data_realtime.csv' 
df.to_csv(output_file, index=False)

print("\n" + "="*50)
print(f"Selesai! Data tersimpan di: {output_file}")
print("==================================================")