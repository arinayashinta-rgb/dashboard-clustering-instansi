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
            "Cluster": [1, 2],
            "Kategori Cluster": ["Tinggi", "Rendah"]
        })

df = load_data()

# =========================
# BACKGROUND IMAGE
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
# STYLE FINAL (UPDATED)
# =========================
st.markdown(f"""
<style>

/* ===== BACKGROUND ===== */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* ===== GLASS ===== */
.glass {{
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 40px;
    margin: 30px auto;
    max-width: 1100px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* ===== HERO TEXT (LEBIH BESAR) ===== */
.hero {{
    text-align: center;
    padding: 100px 20px;
}}

.hero h1 {{
    font-size: 60px;
    font-weight: bold;
    color: #222;
}}

.hero h3 {{
    font-size: 28px;
    color: #444;
    margin-bottom: 15px;
}}

.hero p {{
    font-size: 18px;
    color: #555;
    max-width: 600px;
    margin: auto;
    line-height: 1.6;
}}

/* ===== BUTTON BIRU ===== */
.stButton>button {{
    background: linear-gradient(90deg, #1e90ff, #0066ff);
    color: white;
    border-radius: 25px;
    height: 45px;
    padding: 0 25px;
    border: none;
    font-weight: 500;
}}

.stButton>button:hover {{
    transform: scale(1.03);
    transition: 0.2s;
}}

/* ===== HIDE MENU ===== */
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
        with c1:
            if st.button("BERANDA"):
                go("home")
        with c2:
            if st.button("INPUT"):
                go("input")
        with c3:
            if st.button("HASIL"):
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
        Aplikasi clustering instansi untuk membantu analisis data 
        pengaduan secara otomatis, cepat, dan akurat.
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

    with st.form("form"):

        col1, col2 = st.columns(2)

        # ===== KOLOM KIRI =====
        with col1:
            nama = st.text_input("Nama Instansi")
            total = st.number_input("Total Pengaduan", min_value=0)

            permasalahan = st.text_area("Permasalahan", height=120)

        # ===== KOLOM KANAN =====
        with col2:
            permohonan = st.text_area("Permohonan", height=120)
            pertanyaan = st.text_area("Pertanyaan", height=120)

        st.markdown("<br>", unsafe_allow_html=True)

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

        st.write("Nama:", data["nama"])
        st.write("Total:", data["total"])

        st.write("Permasalahan:", data["permasalahan"])
        st.write("Permohonan:", data["permohonan"])
        st.write("Pertanyaan:", data["pertanyaan"])

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")
    else:
        st.warning("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)