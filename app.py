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
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def pindah(page):
    st.session_state.page = page

# =========================
# STYLE (AMAN)
# =========================
st.markdown("""
<style>

/* padding ringan */
.block-container {
    padding: 2rem 3rem;
}

/* tombol */
.stButton>button {
    background: linear-gradient(90deg,#1abc9c,#16a085);
    color: white;
    border-radius: 8px;
    height: 45px;
    font-size: 15px;
}

.stButton>button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LANDING
# =========================
if st.session_state.page == "landing":

    col1, col2 = st.columns([3,2], gap="large")

    # LEFT (GAMBAR NORMAL)
    with col1:
        st.image("clustering.jpg", use_container_width=True)

    # RIGHT (RAPI TANPA FLEX TINGGI)
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

        st.markdown("## **Clustering Instansi**")

        st.markdown("""
        <p style='color:#555'>
        Aplikasi untuk analisis dan pengelompokan data instansi secara otomatis.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Mulai", use_container_width=True):
            pindah("beranda")

# =========================
# MAIN APP
# =========================
else:

    col_menu, col_content = st.columns([1,4])

    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

    with col_content:

        if st.session_state.page == "beranda":

            st.title("📊 Dashboard Clustering Instansi")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Data", len(df))
            col2.metric("Cluster", df["Cluster"].nunique())
            col3.metric("Status", "Aktif")

        elif st.session_state.page == "input":

            st.title("📝 Input Data")

            with st.form("form_input"):
                nama = st.text_input("Nama Instansi")
                total = st.number_input("Total Pengaduan", min_value=0)

                permasalahan = st.text_area("Permasalahan")
                permohonan = st.text_area("Permohonan")
                pertanyaan = st.text_area("Pertanyaan")

                submit = st.form_submit_button("Proses")

            if submit:
                hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

                st.session_state.hasil = {
                    "nama": nama,
                    "total": total,
                    "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
                    "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
                }

                st.success("Data berhasil diproses")

        elif st.session_state.page == "hasil":

            st.title("📊 Hasil Clustering")

            if "hasil" in st.session_state:
                data = st.session_state.hasil

                st.write(f"Nama: {data['nama']}")
                st.write(f"Total: {data['total']}")

                if data["cluster"] is not None:
                    st.success(f"Cluster: {data['cluster']}")
                    st.info(f"Kategori: {data['kategori']}")
                else:
                    st.error("Data tidak ditemukan")
            else:
                st.warning("Belum ada data")