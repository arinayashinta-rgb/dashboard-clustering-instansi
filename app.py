import streamlit as st
import pandas as pd
import base64

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
# UTIL
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LOAD IMAGE BASE64
# =========================
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("clustering.jpg")

# =========================
# STYLE
# =========================
st.markdown(f"""
<style>
.block-container {{
    padding: 0;
}}

/* LEFT FULL IMAGE */
.left-box {{
    height: 100vh;
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
}}

/* RIGHT */
.right-box {{
    height: 100vh;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.content-box {{
    text-align: center;
    width: 320px;
}}

/* BUTTON */
.stButton>button {{
    background: #1abc9c;
    color: white;
    border-radius: 6px;
    height: 45px;
}}

.stButton>button:hover {{
    background: #16a085;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    col_left, col_right = st.columns([3,2])

    # LEFT (IMAGE)
    with col_left:
        st.markdown('<div class="left-box"></div>', unsafe_allow_html=True)

    # RIGHT (TEXT + BUTTON)
    with col_right:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.markdown('<div class="content-box">', unsafe_allow_html=True)

        st.markdown("## **Clustering Instansi**")
        st.markdown("""
        <p style='color:gray'>
        Aplikasi untuk analisis dan pengelompokan data instansi secara otomatis.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Mulai", use_container_width=True):
            pindah("beranda")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
                    "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
                }

                st.success("Data berhasil diproses")

        elif st.session_state.page == "hasil":

            st.title("📊 Hasil Clustering")

            if "hasil" in st.session_state:
                data = st.session_state.hasil

                st.write(f"**Nama Instansi:** {data['nama']}")
                st.write(f"**Total Pengaduan:** {data['total']}")

                st.divider()

                if data["cluster"] is not None:
                    st.success(f"Cluster: {data['cluster']}")
                    st.info(f"Kategori: {data['kategori']}")
                else:
                    st.error("Data tidak ditemukan")

            else:
                st.warning("Belum ada data")