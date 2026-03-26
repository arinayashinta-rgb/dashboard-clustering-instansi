import streamlit as st
import pandas as pd

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# CUSTOM CSS (BIAR CANTIK 🔥)
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #1f3c88;
}

.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #e8f4ff;
    border-left: 6px solid #1f77b4;
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
# SIDEBAR
# =========================
st.sidebar.title("📌 Navigasi")
menu = st.sidebar.radio("", [
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

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("""
    ### 🎯 Tentang Aplikasi
    Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan hasil clustering yang telah dilakukan sebelumnya.

    ### ⚙️ Cara Menggunakan
    1. Masuk ke menu **Input Data**
    2. Masukkan nama instansi
    3. Isi deskripsi (opsional)
    4. Klik **Tambah Data**
    5. Lihat hasil di menu **Hasil Clustering**
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":
    st.title("📝 Input Data Instansi")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    with st.form("form_input"):
        nama = st.text_input("🏢 Nama Instansi")

        col1, col2, col3 = st.columns(3)
        with col1:
            permasalahan = st.text_area("⚠️ Permasalahan")
        with col2:
            permohonan = st.text_area("📄 Permohonan")
        with col3:
            pertanyaan = st.text_area("❓ Pertanyaan")

        colA, colB = st.columns(2)
        submit = colA.form_submit_button("➕ Tambah Data")
        reset = colB.form_submit_button("🗑️ Reset")

    st.markdown('</div>', unsafe_allow_html=True)

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
                st.error("❌ Instansi tidak ditemukan!")

    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        col1, col2 = st.columns(2)

        # =========================
        # DATA INPUT
        # =========================
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📌 Data Input")

            st.write(f"**Instansi:** {data['nama']}")
            st.write(f"**Permasalahan:** {data['permasalahan']}")
            st.write(f"**Permohonan:** {data['permohonan']}")
            st.write(f"**Pertanyaan:** {data['pertanyaan']}")

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================
        # HASIL
        # =========================
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("🎯 Hasil")

            if data["cluster"] is not None:
                st.success(f"Cluster: {data['cluster']}")
                st.write(f"Kategori: {data['kategori']}")
            else:
                st.error("Data tidak ditemukan")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Silakan input data terlebih dahulu.")