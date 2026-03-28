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
# STYLE (FINAL UPGRADE)
# =========================
st.markdown(f"""
<style>

/* Background */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
}}

/* Container */
.glass {{
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 50px;
    max-width: 1200px;
    margin: auto;
}}

/* TEXT GLOBAL */
html, body {{
    font-size: 18px;
}}

/* LABEL */
label {{
    font-size: 20px !important;
    font-weight: 700 !important;
}}

/* INPUT */
input {{
    font-size: 18px !important;
    padding: 10px !important;
}}

/* BUTTON */
.stButton>button {{
    height: 55px;
    font-size: 18px;
    font-weight: 700;
    border-radius: 30px;
    background: linear-gradient(90deg, #1e90ff, #0066ff);
    color: white;
}}

/* ===== TABEL SUPER BESAR ===== */
[data-testid="stDataFrame"] table {{
    font-size: 22px !important;
}}

[data-testid="stDataFrame"] th {{
    font-size: 24px !important;
    font-weight: 900 !important;
    text-align: center !important;
}}

[data-testid="stDataFrame"] td {{
    font-size: 22px !important;
    font-weight: 700 !important;
}}

/* ===== ANALISIS ===== */
.stAlert {{
    font-size: 20px !important;
    font-weight: 600 !important;
    line-height: 1.8;
}}

.stAlert strong {{
    font-size: 24px !important;
    font-weight: 900 !important;
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
        st.image("Unsia.png", width=140)

    with col2:
        c1, c2, c3 = st.columns(3)
        if c1.button("🏠 BERANDA"):
            go("home")
        if c2.button("📝 INPUT"):
            go("input")
        if c3.button("📊 HASIL"):
            go("hasil")

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("""
    <div style="text-align:center; padding:100px;">
        <h1 style="font-size:70px; font-weight:800;">Selamat Datang</h1>
        <h3 style="font-size:34px;">di Aplikasi Clustering</h3>
        <p style="font-size:22px;">
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

    st.markdown("<h1 style='font-size:40px;'>📝 Input Data</h1>", unsafe_allow_html=True)

    with st.form("form_input"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Nama Instansi**")
            nama = st.text_input("nama_instansi", label_visibility="collapsed")

            st.markdown("**Permasalahan**")
            permasalahan = st.text_input("permasalahan", label_visibility="collapsed")

        with col2:
            st.markdown("**Permohonan**")
            permohonan = st.text_input("permohonan", label_visibility="collapsed")

            st.markdown("**Pertanyaan**")
            pertanyaan = st.text_input("pertanyaan", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**Total Pengaduan**")
        total = st.text_input("total_pengaduan", label_visibility="collapsed")

        submit = st.form_submit_button("🚀 Proses")

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

        st.success("✅ Berhasil diproses")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("<h1 style='font-size:40px;'>📊 Hasil Clustering</h1>", unsafe_allow_html=True)

    if "hasil" in st.session_state:
        data = st.session_state.hasil

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

            st.markdown("<h2 style='font-size:32px; font-weight:800;'>📊 Analisis Clustering</h2>", unsafe_allow_html=True)

            if cluster == 0:
                st.warning("""
<strong>Cluster 0 – Dominan Permasalahan</strong><br><br>

Instansi ini lebih banyak menyampaikan laporan berupa permasalahan dibandingkan dengan permohonan maupun pertanyaan.<br><br>

Hal ini menunjukkan bahwa instansi ini sering menemukan hambatan operasional, gangguan layanan, atau kondisi tertentu yang memerlukan penanganan lebih lanjut.
""", unsafe_allow_html=True)

            elif cluster == 1:
                st.info("""
<strong>Cluster 1 – Dominan Permohonan</strong><br><br>

Instansi ini lebih sering menyampaikan permohonan dibandingkan dengan jenis laporan lainnya.<br><br>

Permohonan berupa permintaan bantuan atau dukungan administratif.
""", unsafe_allow_html=True)

            elif cluster == 2:
                st.success("""
<strong>Cluster 2 – Dominan Pertanyaan</strong><br><br>

Instansi ini lebih sering mengajukan pertanyaan untuk memperoleh informasi atau klarifikasi.<br><br>

Menunjukkan kebutuhan pemahaman lebih lanjut.
""", unsafe_allow_html=True)

            elif cluster == 3:
                st.markdown("""
<div style='font-size:20px; font-weight:600; line-height:1.8;'>

<strong style='font-size:24px;'>Cluster 3 – Campuran</strong><br><br>

Instansi ini memiliki komposisi laporan yang relatif seimbang antara permasalahan, permohonan, dan pertanyaan.

</div>
""", unsafe_allow_html=True)

        else:
            st.error("Data tidak ditemukan")

    else:
        st.warning("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)