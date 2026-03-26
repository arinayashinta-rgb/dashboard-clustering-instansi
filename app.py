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
# SESSION NAVIGATION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def pindah(page):
    st.session_state.page = page

# =========================
# FUNGSI HITUNG
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo.png", width=500)

    st.markdown(
        "<h1 style='text-align:center;'>Aplikasi Clustering Instansi</h1>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Masuk", use_container_width=True):
            pindah("home")

# =========================
# HOME (MENU UTAMA)
# =========================
elif st.session_state.page == "home":

    st.title("📊 Aplikasi Clustering Instansi")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("ℹ️ Tentang Aplikasi", use_container_width=True):
            pindah("tentang")

    with col2:
        if st.button("📝 Input Data", use_container_width=True):
            pindah("input")

    with col3:
        if st.button("📊 Hasil Clustering", use_container_width=True):
            pindah("hasil")

    st.markdown("<br>")

    if st.button("⬅️ Kembali ke Landing Page"):
        pindah("landing")

# =========================
# TENTANG
# =========================
elif st.session_state.page == "tentang":

    st.title("📌 Tentang Aplikasi")

    st.write("""
    Aplikasi ini digunakan untuk menampilkan hasil clustering instansi 
    berdasarkan data yang telah diolah sebelumnya.
    """)

    st.subheader("🧭 Cara Menggunakan")
    st.markdown("""
    1. Pilih menu Input Data  
    2. Masukkan nama instansi  
    3. Isi data (1 baris = 1 item)  
    4. Klik tombol proses  
    5. Lihat hasil clustering  
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Kembali ke Menu"):
            pindah("home")

    with col2:
        if st.button("🏠 Landing Page"):
            pindah("landing")

# =========================
# INPUT DATA
# =========================
elif st.session_state.page == "input":

    st.title("📝 Input Data")

    st.info("Gunakan ENTER untuk memisahkan data (1 baris = 1 item)")

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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Kembali ke Menu"):
            pindah("home")

    with col2:
        if st.button("🏠 Landing Page"):
            pindah("landing")

# =========================
# HASIL CLUSTERING
# =========================
elif st.session_state.page == "hasil":

    st.title("📊 Hasil Clustering")

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        # INFORMASI
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

        # HASIL
        st.subheader("🎯 Hasil")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")

        st.divider()

        # RINCIAN
        st.subheader("📊 Rincian")

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", hitung_jumlah(data["permasalahan"]))
        col2.metric("Permohonan", hitung_jumlah(data["permohonan"]))
        col3.metric("Pertanyaan", hitung_jumlah(data["pertanyaan"]))

    else:
        st.warning("Belum ada data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Kembali ke Menu"):
            pindah("home")

    with col2:
        if st.button("🏠 Landing Page"):
            pindah("landing")