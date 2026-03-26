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
# FUNGSI HITUNG
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LANDING
# =========================
if st.session_state.page == "landing":

    st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.8,3,1])
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
            pindah("beranda")

# =========================
# MAIN LAYOUT (KIRI + KANAN)
# =========================
elif st.session_state.page != "landing":

    col_menu, col_content = st.columns([1,4])

    # =========================
    # MENU KIRI (BUTTON)
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
    # KONTEN KANAN
    # =========================
    with col_content:

        # =========================
        # BERANDA (SESUAI GAMBAR)
        # =========================
        if st.session_state.page == "beranda":

            st.title("📊 Aplikasi Clustering Instansi")

            st.subheader("📌 Tentang Aplikasi")
            st.write("""
            Aplikasi ini digunakan untuk menampilkan hasil clustering instansi 
            berdasarkan data yang telah diolah sebelumnya.
            """)

            st.subheader("🧭 Cara Menggunakan")
            st.markdown("""
            1. Pilih menu Input Data  
            2. Masukkan nama instansi  
            3. Isi data (1 baris = 1 item)  
            4. Klik tombol Proses  
            5. Lihat hasil di menu Hasil Clustering  
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