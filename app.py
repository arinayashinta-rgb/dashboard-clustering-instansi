import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="centered"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# SESSION NAVIGATION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def pindah(page):
    st.session_state.page = page

# =========================
# FUNGSI HITUNG
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=150)

    st.markdown(
        "<h2 style='text-align: center;'>Aplikasi Clustering Instansi</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Masuk", use_container_width=True):
        pindah("menu")

# =========================
# MENU DASHBOARD
# =========================
elif st.session_state.page == "menu":

    st.title("📊 Dashboard")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("ℹ️\nInformasi", use_container_width=True):
            pindah("info")

    with col2:
        if st.button("📝\nInput Data", use_container_width=True):
            pindah("input")

    with col3:
         if st.button("📊\nLihat Hasil", use_container_width=True):
            pindah("hasil")
        
       

# =========================
# INPUT DATA
# =========================
elif st.session_state.page == "input":

    st.title("📝 Input Data")

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")
        permasalahan = st.text_area("Permasalahan")
        permohonan = st.text_area("Permohonan")
        pertanyaan = st.text_area("Pertanyaan")

        submit = st.form_submit_button("Proses")

    if submit:
        hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

        st.session_state.hasil = {
            "nama": nama,
            "permasalahan": permasalahan,
            "permohonan": permohonan,
            "pertanyaan": pertanyaan,
            "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
            "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
        }

        if not hasil.empty:
            st.success("Data berhasil diproses")
        else:
            st.error("Instansi tidak ditemukan")

    if st.button("⬅️ Kembali"):
        pindah("menu")

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":

    st.title("📊 Hasil Clustering")

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        st.write(f"**Instansi:** {data['nama']}")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")

        st.divider()

        st.subheader("📊 Rincian")

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", hitung_jumlah(data["permasalahan"]))
        col2.metric("Permohonan", hitung_jumlah(data["permohonan"]))
        col3.metric("Pertanyaan", hitung_jumlah(data["pertanyaan"]))

    else:
        st.warning("Belum ada data")

    if st.button("⬅️ Kembali"):
        pindah("menu")

# =========================
# INFORMASI
# =========================
elif st.session_state.page == "info":

    st.title("ℹ️ Informasi")

    st.write("""
    Aplikasi ini digunakan untuk menampilkan hasil clustering instansi.

    Cara penggunaan:
    1. Masuk ke menu Input Data
    2. Masukkan nama instansi
    3. Klik proses
    4. Lihat hasil clustering
    """)

    if st.button("⬅️ Kembali"):
        pindah("menu")