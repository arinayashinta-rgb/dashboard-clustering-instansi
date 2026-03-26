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
# LOAD DATA (RINGAN)
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# SIDEBAR NAVIGATION (LEBIH CEPAT 🔥)
# =========================
menu = st.sidebar.radio("Navigasi", [
    "🏠 Beranda",
    "📝 Input Data",
    "📊 Hasil Clustering"
])

# =========================
# SESSION
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# BERANDA
# =========================
if menu == "🏠 Beranda":

    st.markdown("""
    # 👋 Selamat Datang di Aplikasi Clustering Instansi
    """)

    st.info("""
    Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan hasil clustering yang telah dilakukan sebelumnya.
    """)

    col1, col2, col3 = st.columns(3)

    col1.success("📝 Input Data\n\nMasukkan data instansi")
    col2.info("📊 Hasil\n\nLihat hasil clustering")
    col3.warning("ℹ️ Info\n\nPanduan penggunaan")

# =========================
# INPUT DATA
# =========================
elif menu == "📝 Input Data":

    st.title("📝 Input Data Instansi")

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")
        permasalahan = st.text_area("Permasalahan")
        permohonan = st.text_area("Permohonan")
        pertanyaan = st.text_area("Pertanyaan")

        submit = st.form_submit_button("➕ Proses")

    if submit:
        hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

        if not hasil.empty:
            st.session_state.hasil = {
                "nama": nama,
                "cluster": hasil.iloc[0]["Cluster"],
                "kategori": hasil.iloc[0]["Kategori Cluster"]
            }
            st.success("✅ Berhasil diproses!")
        else:
            st.session_state.hasil = {
                "nama": nama,
                "cluster": None,
                "kategori": "Tidak ditemukan"
            }
            st.error("❌ Instansi tidak ditemukan")

# =========================
# HASIL
# =========================
elif menu == "📊 Hasil Clustering":

    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        st.write(f"**Instansi:** {data['nama']}")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")
    else:
        st.warning("Belum ada data diproses")