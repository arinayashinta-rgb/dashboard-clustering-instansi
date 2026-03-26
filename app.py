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
# CUSTOM CSS (SUPER UI 🔥)
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}

/* CARD BUTTON */
.menu-card {
    background-color: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
    transition: 0.3s;
}
.menu-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 22px rgba(0,0,0,0.2);
}

/* TITLE */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1f3c88;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

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
    st.session_state.page = "home"

# =========================
# NAVIGATION FUNCTION
# =========================
def go_to(page):
    st.session_state.page = page

# =========================
# HOME (LANDING PAGE)
# =========================
if st.session_state.page == "home":

    st.markdown('<div class="title">👋 Selamat Datang di Aplikasi Clustering Instansi</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sistem untuk mengelompokkan instansi berdasarkan hasil clustering</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # MENU 1
    with col1:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("📝 Input Data")
        st.write("Masukkan data instansi untuk dianalisis")
        if st.button("Masuk", key="btn1"):
            go_to("input")
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 2
    with col2:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("📊 Hasil Clustering")
        st.write("Lihat hasil pengelompokan instansi")
        if st.button("Lihat", key="btn2"):
            go_to("hasil")
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 3
    with col3:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.subheader("ℹ️ Tentang")
        st.write("Informasi aplikasi dan cara penggunaan")
        if st.button("Info", key="btn3"):
            go_to("tentang")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HALAMAN TENTANG
# =========================
elif st.session_state.page == "tentang":
    st.title("ℹ️ Tentang Aplikasi")

    st.write("""
    Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan hasil clustering.

    ### Cara Penggunaan:
    1. Masuk ke menu Input Data
    2. Masukkan nama instansi
    3. Klik tombol proses
    4. Lihat hasil clustering
    """)

    if st.button("⬅️ Kembali"):
        go_to("home")

# =========================
# INPUT DATA
# =========================
elif st.session_state.page == "input":
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
            st.error("Instansi tidak ditemukan")

    if st.button("⬅️ Kembali"):
        go_to("home")

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":
    st.title("📊 Hasil Clustering")

    if st.session_state.get("hasil"):
        data = st.session_state.hasil

        st.write(f"**Instansi:** {data['nama']}")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")

    else:
        st.warning("Belum ada data diproses")

    if st.button("⬅️ Kembali"):
        go_to("home")