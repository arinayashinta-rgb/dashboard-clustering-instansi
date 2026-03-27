import streamlit as st
import pandas as pd
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        return pd.read_excel("dataset.xlsx")
    except:
        return pd.DataFrame({
            "Asal Instansi": ["A", "B"],
            "Cluster": [0, 1],
            "Kategori Cluster": ["Permasalahan", "Permohonan"]
        })

df = load_data()

# =========================
# BACKGROUND
# =========================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("BG.jpg")

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page

# =========================
# STYLE
# =========================
st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
}}

.glass {{
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 40px;
    margin: 30px auto;
    max-width: 1100px;
}}

.hero {{
    text-align: center;
    padding: 100px 20px;
}}

.hero h1 {{
    font-size: 60px;
}}

.hero h3 {{
    font-size: 28px;
}}

.hero p {{
    font-size: 18px;
}}

.stButton>button {{
    background: linear-gradient(90deg, #1e90ff, #0066ff);
    color: white;
    border-radius: 25px;
    height: 45px;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
def navbar():
    col1, col2 = st.columns([2,3])

    with col1:
        st.image("Unsia.png", width=120)

    with col2:
        c1, c2, c3 = st.columns(3)
        if c1.button("BERANDA"):
            go("home")
        if c2.button("INPUT"):
            go("input")
        if c3.button("HASIL"):
            go("hasil")

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("""
    <div class="hero">
        <h1>Selamat Datang</h1>
        <h3>di Aplikasi Clustering</h3>
        <p>
        Aplikasi clustering instansi untuk membantu analisis data pengaduan 
        secara otomatis, cepat, dan akurat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
elif st.session_state.page == "input":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.title("📝 Input Data")

    with st.form("form_input"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Nama Instansi**")
            nama = st.text_input("nama_instansi", label_visibility="collapsed")

            st.markdown("**Permasalahan**")
            permasalahan = st.text_area("permasalahan", height=80, label_visibility="collapsed")

        with col2:
            st.markdown("**Permohonan**")
            permohonan = st.text_area("permohonan", height=80, label_visibility="collapsed")

            st.markdown("**Pertanyaan**")
            pertanyaan = st.text_area("pertanyaan", height=80, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**Total Pengaduan**")
        col_small, _ = st.columns([1, 3])
        with col_small:
            total = st.text_input("total_pengaduan", label_visibility="collapsed")

        submit = st.form_submit_button("Proses")

    if submit:
        hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

        st.session_state.hasil = {
            "nama": nama,
            "permasalahan": permasalahan,
            "permohonan": permohonan,
            "pertanyaan": pertanyaan,
            "total": total,
            "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
            "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
        }

        st.success("Berhasil diproses")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.title("📊 Hasil Clustering")

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        # ===== TABEL =====
        tabel = pd.DataFrame({
            "Nama Instansi": [data["nama"]],
            "Total Pengaduan": [data["total"]],
            "Permasalahan": [data["permasalahan"]],
            "Permohonan": [data["permohonan"]],
            "Pertanyaan": [data["pertanyaan"]],
            "Cluster": [data["cluster"]],
            "Kategori": [data["kategori"]]
        })

        st.markdown("### 📋 Data Hasil Clustering")
        st.dataframe(tabel, use_container_width=True)

        # ===== ANALISIS =====
        if data["cluster"] is not None:
            cluster = data["cluster"]

            st.markdown("### 📊 Analisis Clustering")

            if cluster == 0:
                st.warning("""
**Cluster 0 – Dominan Permasalahan**

Instansi ini lebih banyak menyampaikan laporan berupa permasalahan dibandingkan dengan permohonan maupun pertanyaan. 

Hal ini menunjukkan bahwa instansi ini sering menemukan hambatan operasional, gangguan layanan, atau kondisi tertentu yang memerlukan penanganan lebih lanjut dari pihak penyedia layanan.
                """)

            elif cluster == 1:
                st.info("""
**Cluster 1 – Dominan Permohonan**

Instansi ini lebih sering menyampaikan permohonan dibandingkan dengan jenis laporan lainnya. 

Permohonan yang dimaksud dapat berupa permintaan bantuan atau permintaan dukungan dalam pelaksanaan kegiatan atau layanan. Instansi ini memiliki kebutuhan koordinasi atau dukungan administratif yang cukup tinggi.
                """)

            elif cluster == 2:
                st.success("""
**Cluster 2 – Dominan Pertanyaan**

Instansi ini lebih sering mengajukan pertanyaan dan cenderung menggunakan sistem pelaporan untuk memperoleh informasi atau klarifikasi terkait kebijakan, prosedur, maupun mekanisme layanan tertentu. 

Tingginya jumlah pertanyaan mengindikasikan bahwa instansi ini masih membutuhkan informasi tambahan atau pemahaman yang lebih jelas.
                """)

            elif cluster == 3:
                st.markdown("""
**Cluster 3 – Campuran**

Instansi ini memiliki komposisi laporan yang relatif seimbang antara permasalahan, permohonan, dan pertanyaan. 

Instansi ini memanfaatkan sistem pelaporan secara lebih komprehensif.
                """)

        else:
            st.error("Data tidak ditemukan")

    else:
        st.warning("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)