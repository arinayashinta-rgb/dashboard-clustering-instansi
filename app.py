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
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

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
    yang telah dilakukan sebelumnya menggunakan metode analisis data.

    Sistem akan menampilkan kategori cluster dari instansi yang diinputkan oleh pengguna.
    """)

    st.write("### 🎯 Tujuan")
    st.markdown("""
    - Mengidentifikasi kategori instansi
    - Mempermudah analisis data instansi
    - Menyajikan hasil clustering secara cepat
    """)

    st.write("### 🧭 Cara Menggunakan Aplikasi")
    st.markdown("""
    1. Pilih menu **Input Data**
    2. Masukkan **nama instansi**
    3. Isi kolom:
       - Permasalahan
       - Permohonan
       - Pertanyaan
    4. Klik tombol **Proses**
    5. Buka menu **Hasil Clustering**
    """)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":

    st.title("📝 Input Data Instansi")

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

            # hitung jumlah kata (aman walau kosong)
            jml_permasalahan = len(permasalahan.split()) if permasalahan else 0
            jml_permohonan = len(permohonan.split()) if permohonan else 0
            jml_pertanyaan = len(pertanyaan.split()) if pertanyaan else 0

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
# HASIL
# =========================
elif menu == "Hasil Clustering":

    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        st.write("### 📌 Detail")
        st.write(f"**Nama Instansi:** {data.get('nama', '-')}")

        st.write("### 🎯 Hasil Clustering")

        if data.get("cluster") is not None:
            st.success(f"Cluster: {data.get('cluster')}")
            st.info(f"Kategori: {data.get('kategori')}")
        else:
            st.error("Data tidak ditemukan dalam dataset")

        # =========================
        # RINCIAN INPUT (ANTI ERROR)
        # =========================
        st.write("### 📊 Rincian Input")

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", data.get("jml_permasalahan", 0))
        col2.metric("Permohonan", data.get("jml_permohonan", 0))
        col3.metric("Pertanyaan", data.get("jml_pertanyaan", 0))

    else:
        st.warning("Silakan input data terlebih dahulu.")