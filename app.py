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
# STYLE (PROFESIONAL)
# =========================
st.markdown("""
<style>

/* HILANGKAN PADDING */
.block-container {
    padding: 0rem 2rem;
}

/* FONT */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#1abc9c,#16a085);
    color: white;
    border-radius: 8px;
    height: 45px;
    font-size: 16px;
    font-weight: 500;
}

/* HOVER */
.stButton>button:hover {
    transform: scale(1.03);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    col1, col2 = st.columns([3,2])

    # =========================
    # LEFT (GAMBAR)
    # =========================
    with col1:
        st.image("clustering.jpg", use_container_width=True)

    # =========================
    # RIGHT (TEXT + BUTTON)
    # =========================
    with col2:

        st.markdown("""
        <div style="
            display:flex;
            flex-direction:column;
            justify-content:center;
            height:80vh;
            padding-left:40px;
        ">
        """, unsafe_allow_html=True)

        st.markdown("## **Clustering Instansi**")

        st.markdown("""
        <p style='color:#555;font-size:14px'>
        Aplikasi untuk analisis dan pengelompokan data instansi secara otomatis.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BUTTON LEBIH PROPORSIONAL
        col_btn = st.columns([1,2,1])[1]
        with col_btn:
            if st.button("🚀 Mulai"):
                pindah("beranda")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
else:

    col_menu, col_content = st.columns([1,4])

    # MENU
    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

    # CONTENT
    with col_content:

        if st.session_state.page == "beranda":

            st.title("📊 Dashboard Clustering Instansi")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Data", len(df))
            col2.metric("Cluster", df["Cluster"].nunique())
            col3.metric("Status", "Aktif")

            st.markdown("---")

            st.subheader("📌 Tentang Aplikasi")
            st.write("""
            Aplikasi ini digunakan untuk mengelompokkan instansi 
            berdasarkan data pengaduan.
            """)

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