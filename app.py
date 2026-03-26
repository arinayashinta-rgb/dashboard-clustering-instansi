import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# GLOBAL CSS
# =========================
st.markdown("""
<style>
.block-container {
    padding: 1rem 2rem;
}

/* SIDEBAR */
.menu-box {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

/* BUTTON */
.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 45px;
    font-size: 15px;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

/* TITLE */
.title {
    font-size: 26px;
    font-weight: bold;
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
# LANDING PAGE (FIXED & FULL)
# =========================
if st.session_state.page == "landing":

    components.html("""
    <div style="font-family:Arial;">

        <!-- NAVBAR -->
        <div style="background:#0a58ca;color:white;padding:15px 40px;
                    display:flex;justify-content:space-between;">
            <div><b>Clustering Instansi</b></div>
            <div>Dashboard Data</div>
        </div>

        <!-- HERO -->
        <div style="display:flex;min-height:85vh;">

            <!-- LEFT -->
            <div style="width:30%;background:#ffe04d;
                        display:flex;align-items:center;padding:60px;">
                <h1 style="color:#0a58ca;font-size:40px;">
                    Selamat Datang di<br>
                    Aplikasi Clustering Instansi
                </h1>
            </div>

            <!-- RIGHT -->
            <div style="width:70%;
                        background:linear-gradient(135deg,#1bb1dc,#4b6cb7);
                        display:flex;align-items:center;justify-content:center;
                        color:white;">

                <div style="display:flex;gap:60px;text-align:center;">

                    <div>
                        <img src="https://i.pravatar.cc/120?img=5"
                             style="border-radius:50%;width:130px;">
                        <p>Analisis Data</p>
                    </div>

                    <div>
                        <img src="https://i.pravatar.cc/120?img=8"
                             style="border-radius:50%;width:130px;">
                        <p>Clustering</p>
                    </div>

                </div>

            </div>

        </div>
    </div>
    """, height=750, scrolling=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
    # MENU (SIDEBAR STYLE)
    # =========================
    with col_menu:
        st.markdown('<div class="menu-box">', unsafe_allow_html=True)

        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # CONTENT
    # =========================
    with col_content:

        # =========================
        # BERANDA (DASHBOARD)
        # =========================
        if st.session_state.page == "beranda":

            st.markdown('<div class="title">📊 Dashboard Clustering Instansi</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # CARDS
            col1, col2, col3 = st.columns(3)

            col1.markdown("""
            <div class="card" style="text-align:center;">
                <h4>Total Data</h4>
                <h2>100+</h2>
            </div>
            """, unsafe_allow_html=True)

            col2.markdown("""
            <div class="card" style="text-align:center;">
                <h4>Cluster</h4>
                <h2>3</h2>
            </div>
            """, unsafe_allow_html=True)

            col3.markdown("""
            <div class="card" style="text-align:center;">
                <h4>Status</h4>
                <h2>Aktif</h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # INFO
            st.markdown("""
            <div class="card">
                <h3>📌 Tentang Aplikasi</h3>
                <p>
                Aplikasi ini digunakan untuk mengelompokkan instansi berdasarkan data pengaduan.
                </p>

                <h3>🧭 Cara Menggunakan</h3>
                <ol>
                <li>Masuk ke menu Input Data</li>
                <li>Isi nama instansi</li>
                <li>Masukkan data</li>
                <li>Klik proses</li>
                <li>Lihat hasil clustering</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # INPUT
        # =========================
        elif st.session_state.page == "input":

            st.markdown('<div class="title">📝 Input Data</div>', unsafe_allow_html=True)

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

            st.markdown('<div class="title">📊 Hasil Clustering</div>', unsafe_allow_html=True)

            if "hasil" in st.session_state:
                data = st.session_state.hasil

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.write(f"**Nama Instansi:** {data['nama']}")
                st.write(f"**Total Pengaduan:** {data['total']}")

                st.write("**Permasalahan:**")
                st.write(data["permasalahan"] or "-")

                st.write("**Permohonan:**")
                st.write(data["permohonan"] or "-")

                st.write("**Pertanyaan:**")
                st.write(data["pertanyaan"] or "-")

                st.divider()

                if data["cluster"] is not None:
                    st.success(f"Cluster: {data['cluster']}")
                    st.info(f"Kategori: {data['kategori']}")
                else:
                    st.error("Data tidak ditemukan")

                st.divider()

                col1, col2, col3 = st.columns(3)

                col1.metric("Permasalahan", hitung_jumlah(data["permasalahan"]))
                col2.metric("Permohonan", hitung_jumlah(data["permohonan"]))
                col3.metric("Pertanyaan", hitung_jumlah(data["pertanyaan"]))

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.warning("Belum ada data")