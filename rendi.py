import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# ==========================
# Fungsi Analisis Sentimen
# ==========================
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positif"
    elif polarity < 0:
        return "Negatif"
    else:
        return "Netral"


# ==========================
# Daftar File
# ==========================
files = {
    "Banjir": "banjir_data_realtime.csv",
    "Gempa Bumi": "gempa_data_realtime.csv",
    "Tanah Longsor": "longsor_data_realtime.csv"
}

summary = {}  # untuk visualisasi dan laporan
all_results = []  # untuk disimpan ke CSV

# ==========================
# Pemrosesan Setiap File
# ==========================
for kategori, file_path in files.items():
    print(f"\n=== Memproses: {kategori} ===")
    
    try:
        df = pd.read_csv(file_path)
    except:
        print(f"File {file_path} tidak ditemukan!")
        continue

    if "Text" not in df.columns:
        print(f"Kolom 'Text' tidak ada dalam file {file_path}")
        continue

    # Analisis sentimen
    df["Sentimen"] = df["Text"].apply(analyze_sentiment)

    # Simpan hasil
    df["Kategori"] = kategori
    all_results.append(df)

    # Ringkasan untuk visualisasi
    summary[kategori] = df["Sentimen"].value_counts()


# ==========================
# Gabungkan Semua Hasil
# ==========================
if all_results:
    final_df = pd.concat(all_results)
    final_df.to_csv("hasil_sentimen.csv", index=False)
    print("\nHasil analisis disimpan ke hasil_sentimen.csv")


# ==========================
# Visualisasi
# ==========================
summary_df = pd.DataFrame(summary).fillna(0)

if not summary_df.empty:
    summary_df.plot(kind="bar", figsize=(10, 6))
    plt.title("Distribusi Sentimen per Kategori Bencana")
    plt.xlabel("Jenis Sentimen")
    plt.ylabel("Jumlah Tweet")
    plt.legend(title="Kategori")
    plt.tight_layout()
    plt.show()
else:
    print("Tidak ada data yang bisa divisualisasikan.")
