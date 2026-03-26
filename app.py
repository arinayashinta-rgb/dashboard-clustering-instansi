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
# FUNGSI CLUSTERING (RULE BASED)
# =========================
def tentukan_cluster(permasalahan, permohonan, pertanyaan):
    teks = (permasalahan + " " + permohonan + " " + pertanyaan).lower()

    if "masalah" in teks or "kendala" in teks:
        return "Dominan Permasalahan"
    elif "mohon" in teks or "permintaan" in teks:
        return "Dominan Permohonan"
    elif "tanya" in teks or "bagaimana" in teks:
        return "Dominan Pertanyaan"
    else:
        return "Campuran"

# ====================================================
# BERANDA
# ====================================================

if menu == "beranda":

    st.title("📊 Clustering Instansi")

    st.markdown("""
Aplikasi ini digunakan untuk **mengelompokkan instansi**
berdasarkan jumlah:

- Permasalahan
- Permohonan
- Pertanyaan

menggunakan metode **K-Means Clustering**.
""")

    st.divider()

    st.subheader("Cara Menggunakan Aplikasi")

    st.write("""
1️⃣ Input data instansi  
2️⃣ Tambahkan beberapa instansi  
3️⃣ Jalankan clustering  
4️⃣ Lihat instansi masuk cluster mana
""")

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

    # =========================
    # PROSES SUBMIT
    # =========================
    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            kategori = tentukan_cluster(permasalahan, permohonan, pertanyaan)

            st.session_state.hasil = {
                "nama": nama,
                "kategori": kategori
            }

            st.success("✅ Data berhasil diproses!")

    # =========================
    # RESET FORM
    # =========================
    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        st.success("Berhasil menentukan cluster!")

        st.write("### Detail Instansi")
        st.write(f"**Nama Instansi:** {st.session_state.hasil['nama']}")

        st.write("### Hasil Clustering")
        st.write(f"**Kategori Cluster:** {st.session_state.hasil['kategori']}")

        # =========================
        # INTERPRETASI
        # =========================
        st.write("### Interpretasi")

        kategori = st.session_state.hasil['kategori']

        if kategori == "Dominan Permasalahan":
            st.info("Instansi ini lebih banyak menyampaikan permasalahan.")
        elif kategori == "Dominan Permohonan":
            st.info("Instansi ini lebih banyak mengajukan permohonan.")
        elif kategori == "Dominan Pertanyaan":
            st.info("Instansi ini cenderung berisi pertanyaan.")
        else:
            st.info("Instansi memiliki kombinasi berbagai jenis laporan.")

    else:
        st.warning("Belum ada data yang diproses. Silakan input data terlebih dahulu.")