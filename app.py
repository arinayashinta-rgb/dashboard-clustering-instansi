import streamlit as st
import pandas as pd

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Menu", [
    "Beranda",
    "Input Data",
    "Hasil Clustering"
])

# =========================
# SESSION
# =========================
if "hasil" not in st.session_state:
    st.session_state.hasil = None

# =========================
# BERANDA
# =========================
if menu == "Beranda":
    st.title("📊 Aplikasi Clustering Instansi")

    st.write("### Data Instansi")
    st.dataframe(df)

# =========================
# INPUT
# =========================
elif menu == "Input Data":
    st.title("📝 Input Data Instansi")

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("➕ Tambah Data")
        reset = col2.form_submit_button("🗑️ Hapus Isian")

    if submit:
        if nama.strip() == "":
            st.warning("Nama instansi wajib diisi!")
        else:
            # =========================
            # CARI DI DATASET
            # =========================
            hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

            if not hasil.empty:
                cluster = hasil.iloc[0]["Cluster"]
                kategori = hasil.iloc[0]["Kategori Cluster"]

                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": cluster,
                    "kategori": kategori
                }

                st.success("✅ Data ditemukan di dataset!")

            else:
                st.session_state.hasil = {
                    "nama": nama,
                    "cluster": None,
                    "kategori": "Tidak ditemukan di dataset"
                }

                st.warning("Instansi tidak ditemukan dalam dataset!")

    if reset:
        st.session_state.hasil = None
        st.rerun()

# =========================
# HASIL
# =========================
elif menu == "Hasil Clustering":
    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        st.write("### Detail Instansi")
        st.write(f"**Nama Instansi:** {data['nama']}")

        if data["cluster"] is not None:
            st.write("### Hasil Clustering")
            st.write(f"**Cluster:** {data['cluster']}")
            st.write(f"**Kategori:** {data['kategori']}")
        else:
            st.error("Data tidak ditemukan dalam dataset")

    else:
        st.warning("Silakan input data terlebih dahulu.")