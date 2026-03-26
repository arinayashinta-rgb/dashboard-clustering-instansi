import streamlit as st
import pandas as pd

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("dataset.xlsx")
    return df

df = load_data()

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
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.write("### Ringkasan Data")
    st.write(f"Jumlah Instansi: {len(df)}")
    st.write(f"Jumlah Cluster: {df['Kategori Cluster'].nunique()}")

    st.write("### Data Contoh")
    st.dataframe(df.head())

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
        # =========================
        # LOGIKA SEDERHANA (RULE BASED)
        # =========================
        teks = (permasalahan + " " + permohonan + " " + pertanyaan).lower()

        if "masalah" in teks or "kendala" in teks:
            kategori = "Dominan Permasalahan"
        elif "mohon" in teks or "permintaan" in teks:
            kategori = "Dominan Permohonan"
        elif "tanya" in teks or "bagaimana" in teks:
            kategori = "Dominan Pertanyaan"
        else:
            kategori = "Campuran"

        st.session_state.hasil = {
            "nama": nama,
            "kategori": kategori
        }

        st.success("Data berhasil diproses!")

    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        st.write("### Hasil Analisis")

        st.write(f"**Nama Instansi:** {st.session_state.hasil['nama']}")
        st.write(f"**Kategori Cluster:** {st.session_state.hasil['kategori']}")

        # tampilkan contoh instansi serupa
        contoh = df[df["Kategori Cluster"] == st.session_state.hasil["kategori"]]

        st.write("### Contoh Instansi dalam Cluster yang Sama")
        st.dataframe(contoh)

    else:
        st.info("Silakan input data terlebih dahulu.")