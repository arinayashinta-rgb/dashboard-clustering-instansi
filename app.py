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
# UTIL
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# GLOBAL STYLE
# =========================
st.markdown("""
<style>
.block-container {
    padding: 0;
}

/* LEFT PANEL */
.left-box {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: black;
}

/* IMAGE FULL */
.left-box img {
    width: 100%;
    height: 100vh;
    object-fit: cover;
}

/* RIGHT PANEL */
.right-box {
    background: #f5f5f5;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CONTENT */
.content-box {
    text-align: center;
    width: 320px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LANDING PAGE
# =========================
# =========================
# GLOBAL STYLE (UPDATE)
# =========================
st.markdown("""
<style>
.block-container {
    padding: 0;
}

/* LEFT FULL BACKGROUND */
.left-box {
    height: 100vh;
    background-image: url('clustering.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* RIGHT PANEL */
.right-box {
    background: #f5f5f5;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CONTENT */
.content-box {
    text-align: center;
    width: 320px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LANDING PAGE (FIXED)
# =========================
if st.session_state.page == "landing":

    col_left, col_right = st.columns([3,2])

    # LEFT (BACKGROUND IMAGE)
    with col_left:
        st.markdown('<div class="left-box"></div>', unsafe_allow_html=True)

    # RIGHT
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

        # BERANDA
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

            st.subheader("🧭 Cara Menggunakan")
            st.markdown("""
            1. Masuk ke menu Input Data  
            2. Isi nama instansi  
            3. Masukkan data  
            4. Klik proses  
            5. Lihat hasil clustering  
            """)

        # INPUT
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

        # HASIL
        elif st.session_state.page == "hasil":

            st.title("📊 Hasil Clustering")

            if "hasil" in st.session_state:
                data = st.session_state.hasil

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

            else:
                st.warning("Belum ada data")