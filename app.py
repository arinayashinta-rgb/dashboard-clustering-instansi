import streamlit as st
import pandas as pd

# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Menu", [
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

    st.write("""
    Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan hasil clustering yang telah dilakukan sebelumnya.

    ### 🎯 Tujuan
    - Mengetahui kategori cluster dari suatu instansi
    - Mempermudah analisis data instansi

    ### 🧭 Cara Menggunakan
    1. Masuk ke menu **Input Data**
    2. Masukkan nama instansi
    3. Isi permasalahan, permohonan, atau pertanyaan (opsional)
    4. Klik tombol **Tambah Data**
    5. Lihat hasil pada menu **Hasil Clustering**
    """)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":
    st.title("📝 Input Data Instansi")

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")

        permasalahan = st.text_area("Permasalahan")
        permohonan = st.text_area("Permohonan")
        pertanyaan = st.text_area("Pertanyaan")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("➕ Tambah Data")
        reset = col2.form_submit_button("🗑️ Hapus Isian")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            # =========================
            # CARI DATA BERDASARKAN INSTANSI
            # =========================
            hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

            if not hasil.empty:
                cluster = hasil.iloc[0]["Cluster"]
                kategori = hasil.iloc[0]["Kategori Cluster"]

                st.session_state.hasil = {
                    "nama": nama,
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": cluster,
                    "kategori": kategori
                }

                st.success("✅ Data berhasil diproses!")

            else:
                st.session_state.hasil = {
                    "nama": nama,
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": None,
                    "kategori": "Tidak ditemukan di dataset"
                }

                st.warning("Instansi tidak ditemukan dalam dataset!")

    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        st.write("### 📌 Data Input")
        st.write(f"**Nama Instansi:** {data['nama']}")
        st.write(f"**Permasalahan:** {data['permasalahan']}")
        st.write(f"**Permohonan:** {data['permohonan']}")
        st.write(f"**Pertanyaan:** {data['pertanyaan']}")

        st.write("### 🎯 Hasil Clustering")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Instansi tidak ditemukan dalam dataset")

    else:
        st.warning("Silakan input data terlebih dahulu.")