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

            # =========================
            # HITUNG JUMLAH KATA
            # =========================
            jumlah_permasalahan = len(permasalahan.split())
            jumlah_permohonan = len(permohonan.split())
            jumlah_pertanyaan = len(pertanyaan.split())

            if not hasil.empty:
                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": hasil.iloc[0]["Cluster"],
                    "kategori": hasil.iloc[0]["Kategori Cluster"],
                    "jml_permasalahan": jumlah_permasalahan,
                    "jml_permohonan": jumlah_permohonan,
                    "jml_pertanyaan": jumlah_pertanyaan
                }
                st.success("✅ Data berhasil diproses!")
            else:
                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": None,
                    "kategori": "Tidak ditemukan",
                    "jml_permasalahan": jumlah_permasalahan,
                    "jml_permohonan": jumlah_permohonan,
                    "jml_pertanyaan": jumlah_pertanyaan
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
        st.write(f"**Nama Instansi:** {data['nama']}")

        st.write("### 🎯 Hasil Clustering")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan dalam dataset")

        # =========================
        # RINCIAN INPUT
        # =========================
        st.write("### 📊 Rincian Input")

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", data["jml_permasalahan"])
        col2.metric("Permohonan", data["jml_permohonan"])
        col3.metric("Pertanyaan", data["jml_pertanyaan"])

    else:
        st.warning("Silakan input data terlebih dahulu.")