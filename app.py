import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# FUNGSI HITUNG (BENAR 🔥)
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    
    # 1 baris = 1 item
    lines = [line.strip() for line in teks.split("\n") if line.strip()]
    return len(lines)

# =========================
# NAVIGASI
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "Beranda",
    "Input Data",
    "Hasil Clustering"
])

# =========================
# SESSION STATE
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.write("### 📌 Tentang Aplikasi")
    st.write("""
    Aplikasi ini digunakan untuk menampilkan hasil clustering instansi 
    berdasarkan data yang telah diolah sebelumnya.
    """)

    st.write("### 🧭 Cara Menggunakan")
    st.markdown("""
    1. Pilih menu **Input Data**
    2. Masukkan nama instansi
    3. Isi data (1 baris = 1 item)
    4. Klik tombol **Proses**
    5. Lihat hasil di menu **Hasil Clustering**
    """)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":

    st.title("📝 Input Data Instansi")

    st.info("💡 Gunakan ENTER untuk memisahkan data (1 baris = 1 item)")

    with st.form("form_input"):
        nama = st.text_input("🏢 Nama Instansi")

        permasalahan = st.text_area("⚠️ Permasalahan")
        permohonan = st.text_area("📄 Permohonan")
        pertanyaan = st.text_area("❓ Pertanyaan")

        submit = st.form_submit_button("➕ Proses")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

            if not hasil.empty:
                st.session_state.hasil = {
                    "nama": nama,
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": hasil.iloc[0]["Cluster"],
                    "kategori": hasil.iloc[0]["Kategori Cluster"]
                }
                st.success("✅ Data berhasil diproses!")
            else:
                st.session_state.hasil = {
                    "nama": nama,
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": None,
                    "kategori": "Tidak ditemukan"
                }
                st.error("❌ Instansi tidak ditemukan")

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":

    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        # =========================
        # DATA INPUT
        # =========================
        st.write("### 📌 Data Input")
        st.write(f"**Nama Instansi:** {data['nama']}")
        st.write(f"**Permasalahan:** {data['permasalahan']}")
        st.write(f"**Permohonan:** {data['permohonan']}")
        st.write(f"**Pertanyaan:** {data['pertanyaan']}")

        # =========================
        # HITUNG JUMLAH (VALID)
        # =========================
        jml_permasalahan = hitung_jumlah(data.get("permasalahan", ""))
        jml_permohonan = hitung_jumlah(data.get("permohonan", ""))
        jml_pertanyaan = hitung_jumlah(data.get("pertanyaan", ""))

        # =========================
        # HASIL CLUSTERING
        # =========================
        st.write("### 🎯 Hasil Clustering")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Instansi tidak ditemukan dalam dataset")

      