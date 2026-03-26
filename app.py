import streamlit as st

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Menu", [
    "Beranda",
    "Input Data",
    "Hasil Clustering"
])

# =========================
# SESSION STATE
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# FUNGSI CLUSTERING (VERSI IMPROVED)
# =========================
def tentukan_cluster(permasalahan, permohonan, pertanyaan):

    skor = {
        "Dominan Permasalahan": 0,
        "Dominan Permohonan": 0,
        "Dominan Pertanyaan": 0
    }

    teks_permasalahan = permasalahan.lower()
    teks_permohonan = permohonan.lower()
    teks_pertanyaan = pertanyaan.lower()

    # =========================
    # KEYWORD DETECTION
    # =========================
    kata_masalah = ["masalah", "kendala", "error", "gangguan", "tidak bisa"]
    kata_permohonan = ["mohon", "permintaan", "harap", "tolong", "ajukan"]
    kata_pertanyaan = ["bagaimana", "apakah", "kenapa", "kapan", "?"]

    # cek permasalahan
    for kata in kata_masalah:
        if kata in teks_permasalahan:
            skor["Dominan Permasalahan"] += 2

    # cek permohonan
    for kata in kata_permohonan:
        if kata in teks_permohonan:
            skor["Dominan Permohonan"] += 2

    # cek pertanyaan
    for kata in kata_pertanyaan:
        if kata in teks_pertanyaan:
            skor["Dominan Pertanyaan"] += 2

    # =========================
    # LOGIKA TAMBAHAN (PANJANG TEKS)
    # =========================
    if len(teks_permasalahan) > len(teks_permohonan) and len(teks_permasalahan) > len(teks_pertanyaan):
        skor["Dominan Permasalahan"] += 1

    if len(teks_permohonan) > len(teks_permasalahan) and len(teks_permohonan) > len(teks_pertanyaan):
        skor["Dominan Permohonan"] += 1

    if len(teks_pertanyaan) > len(teks_permasalahan) and len(teks_pertanyaan) > len(teks_permohonan):
        skor["Dominan Pertanyaan"] += 1

    # =========================
    # HASIL AKHIR
    # =========================
    if all(v == 0 for v in skor.values()):
        return "Campuran", skor

    hasil = max(skor, key=skor.get)
    return hasil, skor

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.write("""
    Aplikasi ini digunakan untuk:
    - Mengelompokkan instansi berdasarkan isi laporan
    - Menentukan kategori cluster secara otomatis
    """)

    st.info("Masuk ke menu **Input Data** untuk mulai.")

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":
    st.title("📝 Input Data Instansi")

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")
        permasalahan = st.text_area("Permasalahan")
        permohonan = st.text_area("Permohonan")
        pertanyaan = st.text_area("Pertanyaan")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("➕ Tambah Data")
        reset = col2.form_submit_button("🗑️ Hapus Isian")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            kategori, skor = tentukan_cluster(permasalahan, permohonan, pertanyaan)

            st.session_state.hasil = {
                "nama": nama,
                "kategori": kategori,
                "skor": skor
            }

            st.success("✅ Data berhasil diproses!")

    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        st.success("Berhasil menentukan cluster!")

        st.write("### Detail Instansi")
        st.write(f"**Nama Instansi:** {data['nama']}")

        st.write("### Hasil Clustering")
        st.write(f"**Kategori Cluster:** {data['kategori']}")

        # =========================
        # INTERPRETASI
        # =========================
        st.write("### Interpretasi")

        if data["kategori"] == "Dominan Permasalahan":
            st.info("Instansi ini lebih banyak menyampaikan permasalahan.")
        elif data["kategori"] == "Dominan Permohonan":
            st.info("Instansi ini lebih banyak mengajukan permohonan.")
        elif data["kategori"] == "Dominan Pertanyaan":
            st.info("Instansi ini berisi pertanyaan atau inquiry.")
        else:
            st.info("Instansi memiliki kombinasi berbagai jenis laporan.")

        # =========================
        # DEBUG (OPSIONAL - BAGUS UNTUK SKRIPSI)
        # =========================
        with st.expander("🔍 Lihat Skor Penilaian"):
            st.write(data["skor"])

    else:
        st.warning("Belum ada data yang diproses. Silakan input data terlebih dahulu.")