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
# STYLE FINAL (SUDAH FIX)
# =========================
st.markdown(f"""
<style>

/* ===== BACKGROUND FIX ===== */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* ===== GLASS ===== */
.glass {{
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 30px;
    margin: 30px auto;
    max-width: 1100px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* ===== HERO ===== */
.hero {{
    text-align: center;
    padding: 80px 20px;
}}

.hero h1 {{
    font-size: 48px;
}}

.hero h3 {{
    color: #555;
}}

.hero p {{
    color: #666;
    max-width: 500px;
    margin: auto;
}}

/* ===== BUTTON ===== */
.stButton>button {{
    background: #2c2c2c;
    color: white;
    border-radius: 25px;
    height: 45px;
    padding: 0 25px;
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
        st.image("Unsia.png", width=120)  # logo UNSIA

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
# DASHBOARD
# =========================
elif st.session_state.page == "dashboard":

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    navbar()

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data", len(df))
    col2.metric("Cluster", df["Cluster"].nunique())
    col3.metric("Status", "Aktif")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
elif st.session_state.page == "input":

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    navbar()

    st.title("📝 Input Data")

    with st.form("form"):
        nama = st.text_input("Nama Instansi")

        permasalahan = st.text_area("Permasalahan")
        permohonan = st.text_area("Permohonan")
        pertanyaan = st.text_area("Pertanyaan")

        total = st.number_input("Total Pengaduan", min_value=0)

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