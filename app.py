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

/* Background */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
}}

/* Container */
.glass {{
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 50px;
    margin: 30px auto;
    max-width: 1200px;
}}

/* Hero */
.hero {{
    text-align: center;
    padding: 120px 20px;
}}

.hero h1 {{
    font-size: 70px;
    font-weight: 800;
}}

.hero h3 {{
    font-size: 34px;
    font-weight: 700;
}}

.hero p {{
    font-size: 22px;
}}

/* Global text */
html, body {{
    font-size: 18px;
}}

/* Label */
label {{
    font-size: 20px !important;
    font-weight: 600 !important;
}}

/* Input */
input {{
    font-size: 18px !important;
    padding: 10px !important;
}}

/* Button */
.stButton>button {{
    height: 55px;
    font-size: 18px;
    font-weight: 700;
    border-radius: 30px;
    background: linear-gradient(90deg, #1e90ff, #0066ff);
    color: white;
}}

/* Hide menu */
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

        st.dataframe(tabel, use_container_width=True)

        if data["cluster"] is not None:
            cluster = data["cluster"]

            if cluster == 0:
                st.warning("Cluster 0 – Dominan Permasalahan")
            elif cluster == 1:
                st.info("Cluster 1 – Dominan Permohonan")
            elif cluster == 2:
                st.success("Cluster 2 – Dominan Pertanyaan")
            elif cluster == 3:
                st.markdown("Cluster 3 – Campuran")

        else:
            st.error("Data tidak ditemukan")

    else:
        st.warning("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)