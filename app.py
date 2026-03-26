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
# FUNGSI HITUNG (1 BARIS = 1 ITEM)
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# SESSION STATE
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# NAVIGASI
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "Beranda",
    "Input Data",
    "Hasil Clustering"
])

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.markdown("""
    Aplikasi ini digunakan untuk menampilkan hasil clustering instansi 
    berdasarkan dataset yang telah dianalisis sebelumnya.
    """)

    st.subheader("🎯 Tujuan")
    st.markdown("""
    - Mengelompokkan instansi berdasarkan cluster  
    - Mempermudah analisis data  
    - Menyajikan hasil secara cepat  
    """)

    st.subheader("🧭 Cara Menggunakan")
    st.markdown("""
    1. Pilih menu **Input Data**  
    2. Masukkan nama instansi  
    3. Isi data (1 baris = 1 item)  
    4. Klik tombol **Proses**  
    5. Buka menu **Hasil Clustering**  
    """)

# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":

    st.title("📝 Input Data Instansi")

    st.info("Gunakan ENTER untuk memisahkan data (1 baris = 1 item)")

    with st.form("form_input"):
        nama = st.text_input("🏢 Nama Instansi")

        permasalahan = st.text_area("⚠️ Permasalahan")
        permohonan = st.text_area("📄 Permohonan")
        pertanyaan = st.text_area("❓ Pertanyaan")

        submit = st.form_submit_button("➕ Proses Data")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi")
        else:
            hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

            st.session_state.hasil = {
                "nama": nama,
                "permasalahan": permasalahan,
                "permohonan": permohonan,
                "pertanyaan": pertanyaan,
                "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
                "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
            }

            if not hasil.empty:
                st.success("Data berhasil diproses")
            else:
                st.error("Instansi tidak ditemukan dalam dataset")

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":

    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        # =========================
        # INFORMASI INSTANSI
        # =========================
        st.subheader("📌 Informasi Instansi")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Nama Instansi**")
            st.write(data["nama"])

        with col2:
            if data["cluster"] is not None:
                st.success("Data ditemukan")
            else:
                st.error("Data tidak ditemukan")

        st.divider()

        # =========================
        # HASIL CLUSTERING
        # =========================
        st.subheader("🎯 Hasil Clustering")

        col1, col2 = st.columns(2)

        with col1:
            if data["cluster"] is not None:
                st.success(f"Cluster: {data['cluster']}")
            else:
                st.error("-")

        with col2:
            if data["cluster"] is not None:
                st.info(f"Kategori: {data['kategori']}")
            else:
                st.warning("-")

        st.divider()

        # =========================
        # DETAIL INPUT
        # =========================
        st.subheader("📝 Detail Input")

        st.write("**Permasalahan**")
        st.write(data["permasalahan"] or "-")

        st.write("**Permohonan**")
        st.write(data["permohonan"] or "-")

        st.write("**Pertanyaan**")
        st.write(data["pertanyaan"] or "-")

        st.divider()

        # =========================
        # RINCIAN
        # =========================
        st.subheader("📊 Rincian Input")

        jml_permasalahan = hitung_jumlah(data.get("permasalahan", ""))
        jml_permohonan = hitung_jumlah(data.get("permohonan", ""))
        jml_pertanyaan = hitung_jumlah(data.get("pertanyaan", ""))

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", jml_permasalahan)
        col2.metric("Permohonan", jml_permohonan)
        col3.metric("Pertanyaan", jml_pertanyaan)

        st.divider()

        # =========================
        # ANALISIS TAMBAHAN
        # =========================
        st.subheader("🧠 Analisis")

        kategori_dominan = max(
            {
                "Permasalahan": jml_permasalahan,
                "Permohonan": jml_permohonan,
                "Pertanyaan": jml_pertanyaan
            },
            key=lambda x: {
                "Permasalahan": jml_permasalahan,
                "Permohonan": jml_permohonan,
                "Pertanyaan": jml_pertanyaan
            }[x]
        )

        st.info(f"Jenis laporan yang paling dominan: **{kategori_dominan}**")

    else:
        st.warning("Silakan input data terlebih dahulu")