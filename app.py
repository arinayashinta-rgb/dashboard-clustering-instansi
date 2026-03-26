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
# CUSTOM CSS (UI MODERN)
# =========================
st.markdown("""
<style>
.block-container {
    padding: 0;
}

/* NAVBAR */
.navbar {
    background-color: #0a58ca;
    padding: 15px 40px;
    color: white;
    display: flex;
    justify-content: space-between;
    font-weight: bold;
}

/* HERO */
.hero {
    display: flex;
    height: 500px;
}

/* KIRI */
.hero-left {
    width: 30%;
    background-color: #ffe04d;
    display: flex;
    align-items: center;
    padding: 50px;
}

.hero-left h1 {
    color: #0a58ca;
    font-size: 38px;
}

/* KANAN */
.hero-right {
    width: 70%;
    background: linear-gradient(135deg, #1bb1dc, #4b6cb7);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

/* CARD */
.hero-card {
    display: flex;
    gap: 40px;
    text-align: center;
}

.hero-card img {
    width: 120px;
    border-radius: 50%;
}

/* BUTTON */
.stButton>button {
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
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
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    # NAVBAR
    st.markdown("""
    <div class="navbar">
        <div>Clustering Instansi</div>
        <div>Dashboard Data</div>
    </div>
    """, unsafe_allow_html=True)

    # HERO
    st.markdown("""
    <div class="hero">

        <div class="hero-left">
            <h1>Selamat Datang di<br>Aplikasi Clustering Instansi</h1>
        </div>

        <div class="hero-right">
            <div class="hero-card">
                <div>
                    <img src="https://i.pravatar.cc/120?img=5">
                    <p>Analisis Data</p>
                </div>
                <div>
                    <img src="https://i.pravatar.cc/120?img=8">
                    <p>Clustering</p>
                </div>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BUTTON MASUK
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Masuk ke Aplikasi", use_container_width=True):
            pindah("beranda")

# =========================
# MAIN APP
# =========================
else:

    col_menu, col_content = st.columns([1,4])

    # =========================
    # MENU
    # =========================
    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

    # =========================
    # CONTENT
    # =========================
    with col_content:

        # =========================
        # BERANDA
        # =========================
        if st.session_state.page == "beranda":

            st.title("📊 Dashboard Clustering Instansi")

            st.subheader("📌 Tentang Aplikasi")
            st.write("""
            Aplikasi ini digunakan untuk mengelompokkan instansi 
            berdasarkan data pengaduan yang masuk.
            """)

            st.subheader("🧭 Cara Menggunakan")
            st.markdown("""
            1. Masuk ke menu Input Data  
            2. Isi nama instansi  
            3. Masukkan data  
            4. Klik proses  
            5. Lihat hasil clustering  
            """)

        # =========================
        # INPUT
        # =========================
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

        # =========================
        # HASIL
        # =========================
        elif st.session_state.page == "hasil":

            st.title("📊 Hasil Clustering")

            if "hasil" in st.session_state:
                data = st.session_state.hasil

                st.subheader("📌 Informasi")
                st.write(f"**Nama Instansi:** {data['nama']}")
                st.write(f"**Total Pengaduan:** {data['total']}")

                st.write("**Permasalahan:**")
                st.write(data["permasalahan"] or "-")

                st.write("**Permohonan:**")
                st.write(data["permohonan"] or "-")

                st.write("**Pertanyaan:**")
                st.write(data["pertanyaan"] or "-")

                st.divider()

                st.subheader("🎯 Hasil")

                if data["cluster"] is not None:
                    st.success(f"Cluster: {data['cluster']}")
                    st.info(f"Kategori: {data['kategori']}")
                else:
                    st.error("Data tidak ditemukan")

                st.divider()

                st.subheader("📊 Rincian")

                col1, col2, col3 = st.columns(3)

                col1.metric("Permasalahan", hitung_jumlah(data["permasalahan"]))
                col2.metric("Permohonan", hitung_jumlah(data["permohonan"]))
                col3.metric("Pertanyaan", hitung_jumlah(data["pertanyaan"]))

            else:
                st.warning("Belum ada data")