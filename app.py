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
# STYLE MODERN UI
# =========================
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(135deg, #dbe6f6, #c5796d);
}

/* Glass Container */
.glass {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 30px;
    margin: 30px auto;
    max-width: 1100px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
}

.nav-links a {
    margin: 0 15px;
    text-decoration: none;
    color: #333;
    font-size: 14px;
}

/* Hero */
.hero {
    text-align: center;
    padding: 80px 20px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 10px;
}

.hero h3 {
    color: #555;
    margin-bottom: 15px;
}

.hero p {
    color: #666;
    max-width: 500px;
    margin: auto;
    margin-bottom: 25px;
}

/* Button */
.stButton>button {
    background: #2c2c2c;
    color: white;
    border-radius: 25px;
    height: 45px;
    font-size: 14px;
    padding: 0 25px;
}

/* Sidebar Button Style */
.sidebar-btn button {
    width: 100%;
    margin-bottom: 10px;
}

/* Metrics */
.metric-box {
    background: rgba(255,255,255,0.7);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    st.markdown("""
    <div class="glass">

        <div class="navbar">
            <div><b>LOGO HERE</b></div>
            <div class="nav-links">
                <a href="#">HOME</a>
                <a href="#">SERVICES</a>
                <a href="#">ABOUT</a>
                <a href="#">CONTACT</a>
            </div>
        </div>

        <div class="hero">
            <h1>Welcome</h1>
            <h3>To Our Company</h3>
            <p>
            Aplikasi clustering instansi untuk membantu analisis data pengaduan 
            secara otomatis, cepat, dan akurat.
            </p>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)

    if st.button("🚀 LEARN MORE"):
        pindah("beranda")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
else:

    col_menu, col_content = st.columns([1,4])

    # ===== SIDEBAR MENU =====
    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

    # ===== CONTENT =====
    with col_content:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        # ================= BERANDA =================
        if st.session_state.page == "beranda":

            st.title("📊 Dashboard Clustering Instansi")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Data", len(df))

            with col2:
                st.metric("Cluster", df["Cluster"].nunique())

            with col3:
                st.metric("Status", "Aktif")

        # ================= INPUT =================
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

        # ================= HASIL =================
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

        st.markdown('</div>', unsafe_allow_html=True)