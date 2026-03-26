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
# FUNGSI HITUNG ITEM (FIX 🔥)
# =========================
def hitung_jumlah(teks):
    if not teks.strip():
        return 0
    
    # pisahkan berdasarkan enter, titik, koma
    teks = teks.replace("\n", ".").replace(",", ".")
    items = [i.strip() for i in teks.split(".") if i.strip()]
    
    return len(items)

# =========================
# NAVIGASI
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "Beranda",
    "Input Data",
    "Hasil Clustering"
])

# =========================
# SESSION
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.write("### 📌 Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan hasil clustering 
    yang telah dilakukan sebelumnya.

    Sistem akan menampilkan kategori cluster dari instansi yang diinputkan.
    """)

    st.write("### 🎯 Tujuan")
    st.markdown("""
    - Mengidentifikasi kategori instansi
    - Mempermudah analisis data
    - Menyajikan hasil secara cepat
    """)

    st.write("### 🧭 Cara Menggunakan")
    st.markdown("""
    1. Pilih menu **Input Data**
    2. Masukkan nama instansi
    3. Isi:
       - Permasalahan
       - Permohonan
       - Pertanyaan
    4. Klik **Proses**
    5. Buka menu **Hasil Clustering**
    """)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":

    st.title("📝 Input Data Instansi")

    with st.form("form_input"):
        nama = st.text_input("🏢 Nama Instansi")

        st.write("### ✏️ Deskripsi (boleh lebih dari 1, pisahkan enter / titik)")

        permasalahan = st.text_area("⚠️ Permasalahan")
        permohonan = st.text_area("📄 Permohonan")
        pertanyaan = st.text_area("❓ Pertanyaan")

        submit = st.form_submit_button("➕ Proses")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

            # =========================
            # HITUNG ITEM (SUDAH BENAR)
            # =========================
            jml_permasalahan = hitung_jumlah(permasalahan)
            jml_permohonan = hitung_jumlah(permohonan)
            jml_pertanyaan = hitung_jumlah(pertanyaan)

            if not hasil.empty:
                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": hasil.iloc[0]["Cluster"],
                    "kategori": hasil.iloc[0]["Kategori Cluster"],
                    "jml_permasalahan": jml_permasalahan,
                    "jml_permohonan": jml_permohonan,
                    "jml_pertanyaan": jml_pertanyaan
                }
                st.success("✅ Data berhasil diproses!")
            else:
                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": None,
                    "kategori": "Tidak ditemukan",
                    "jml_permasalahan": jml_permasalahan,
                    "jml_permohonan": jml_permohonan,
                    "jml_pertanyaan": jml_pertanyaan
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
        # DETAIL
        # =========================
        st.write("### 📌 Detail Instansi")
        st.write(f"**Nama Instansi:** {data.get('nama')}")

        # =========================
        # HASIL
        # =========================
        st.write("### 🎯 Hasil Clustering")

        if data.get("cluster") is not None:
            st.success(f"Cluster: {data.get('cluster')}")
            st.info(f"Kategori: {data.get('kategori')}")
        else:
            st.error("Instansi tidak ditemukan dalam dataset")

        # =========================
        # RINCIAN (SUDAH FIX 🔥)
        # =========================
        st.write("### 📊 Rincian Input")

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", data.get("jml_permasalahan", 0))
        col2.metric("Permohonan", data.get("jml_permohonan", 0))
        col3.metric("Pertanyaan", data.get("jml_pertanyaan", 0))

        # =========================
        # ANALISIS TAMBAHAN
        # =========================
        st.write("### 🧠 Analisis")

        max_kategori = max({
            "Permasalahan": data.get("jml_permasalahan", 0),
            "Permohonan": data.get("jml_permohonan", 0),
            "Pertanyaan": data.get("jml_pertanyaan", 0)
        }, key=lambda x: {
            "Permasalahan": data.get("jml_permasalahan", 0),
            "Permohonan": data.get("jml_permohonan", 0),
            "Pertanyaan": data.get("jml_pertanyaan", 0)
        }[x])

        st.info(f"Jenis laporan yang paling dominan: **{max_kategori}**")

    else:
        st.warning("Silakan input data terlebih dahulu.")