import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="centered"
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
# FUNGSI HITUNG (VALID)
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LANDING PAGE (FIX CENTER)
# =========================
if st.session_state.page == "landing":

    # Spacer atas (atur tinggi biar pas tengah)
    st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

    # CENTER GAMBAR
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        st.image("logo.png", width=200)

    # JUDUL
    st.markdown(
        "<h2 style='text-align:center;'>Aplikasi Clustering Instansi</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # BUTTON CENTER
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Masuk", use_container_width=True):
            pindah("menu")

# =========================
# MENU
# =========================
elif st.session_state.page == "menu":

    st.title("📊 Menu Utama")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("ℹ️ Tentang Aplikasi", use_container_width=True):
        pindah("tentang")

    if st.button("📝 Input Data", use_container_width=True):
        pindah("input")

    if st.button("📊 Hasil Clustering", use_container_width=True):
        pindah("hasil")

# =========================
# TENTANG
# =========================
elif st.session_state.page == "tentang":

    st.title("ℹ️ Tentang Aplikasi")

    st.write("""
    Aplikasi ini digunakan untuk menampilkan hasil clustering instansi 
    berdasarkan dataset yang telah dianalisis sebelumnya.

    ### Cara Penggunaan:
    1. Masuk ke menu Input Data
    2. Masukkan nama instansi
    3. Isi data pengaduan
    4. Klik proses
    5. Lihat hasil clustering
    """)

    if st.button("⬅️ Kembali"):
        pindah("menu")

# =========================
# INPUT DATA
# =========================
elif st.session_state.page == "input":

    st.title("📝 Input Data")

    st.info("Gunakan ENTER untuk memisahkan data (1 baris = 1 item)")

    with st.form("form_input"):
        nama = st.text_input("🏢 Nama Instansi")

        total_pengaduan = st.number_input("📊 Total Pengaduan", min_value=0, step=1)

        permasalahan = st.text_area("⚠️ Permasalahan")
        permohonan = st.text_area("📄 Permohonan")
        pertanyaan = st.text_area("❓ Pertanyaan")

        submit = st.form_submit_button("Proses")

    if submit:
        hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

        st.session_state.hasil = {
            "nama": nama,
            "total": total_pengaduan,
            "permasalahan": permasalahan,
            "permohonan": permohonan,
            "pertanyaan": pertanyaan,
            "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
            "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
        }

        if not hasil.empty:
            st.success("Data berhasil diproses")
        else:
            st.error("Instansi tidak ditemukan")

    if st.button("⬅️ Kembali"):
        pindah("menu")

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":

    st.title("📊 Hasil Clustering")

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        # =========================
        # INFORMASI
        # =========================
        st.subheader("📌 Informasi")

        st.write(f"**Nama Instansi:** {data['nama']}")
        st.write(f"**Total Pengaduan:** {data['total']}")

        st.divider()

        # =========================
        # HASIL
        # =========================
        st.subheader("🎯 Hasil")

        if data["cluster"] is not None:
            st.success(f"Cluster: {data['cluster']}")
            st.info(f"Kategori: {data['kategori']}")
        else:
            st.error("Data tidak ditemukan")

        st.divider()

        # =========================
        # RINCIAN (VALID 🔥)
        # =========================
        st.subheader("📊 Rincian Input")

        jml_permasalahan = hitung_jumlah(data["permasalahan"])
        jml_permohonan = hitung_jumlah(data["permohonan"])
        jml_pertanyaan = hitung_jumlah(data["pertanyaan"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", jml_permasalahan)
        col2.metric("Permohonan", jml_permohonan)
        col3.metric("Pertanyaan", jml_pertanyaan)

        st.divider()

        # =========================
        # VALIDASI (PENTING 🔥)
        # =========================
        total_input = jml_permasalahan + jml_permohonan + jml_pertanyaan

        st.write(f"Total hasil input: **{total_input}**")

        if total_input != data["total"]:
            st.warning("Jumlah rincian tidak sama dengan total pengaduan")
        else:
            st.success("Jumlah rincian sesuai dengan total pengaduan")

    else:
        st.warning("Belum ada data")

    if st.button("⬅️ Kembali"):
        pindah("menu")