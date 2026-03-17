import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =============================
# FILE DATA
# =============================

DATA_FILE = "data_instansi.csv"

# jika file belum ada
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Asal Instansi",
        "Permasalahan",
        "Permohonan",
        "Pertanyaan"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# fungsi load data
def load_data():
    return pd.read_csv(DATA_FILE)

# fungsi simpan data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# =============================
# MENU
# =============================

if "menu" not in st.session_state:
    st.session_state.menu = "beranda"

st.sidebar.title("📁 Navigasi")

if st.sidebar.button("🏠 Beranda"):
    st.session_state.menu = "beranda"

if st.sidebar.button("📝 Input Data Instansi"):
    st.session_state.menu = "input"

if st.sidebar.button("🤖 Cek Cluster Instansi"):
    st.session_state.menu = "cluster"

menu = st.session_state.menu


# ====================================================
# BERANDA
# ====================================================

if menu == "beranda":

    st.title("📊 Dashboard Clustering Instansi")

    st.markdown("""
Dashboard ini digunakan untuk **mengelompokkan instansi**
berdasarkan jumlah:

- Permasalahan
- Permohonan
- Pertanyaan

menggunakan metode **K-Means Clustering**.
""")

    df = load_data()

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Jumlah Data", len(df))
    col2.metric("Jumlah Instansi", df["Asal Instansi"].nunique())
    col3.metric("Jumlah Variabel", 3)

    st.divider()

    st.subheader("Cara Menggunakan Dashboard")

    st.write("""
1️⃣ Input data instansi  
2️⃣ Tambahkan beberapa instansi  
3️⃣ Jalankan clustering  
4️⃣ Lihat instansi masuk cluster mana
""")


# ====================================================
# INPUT DATA INSTANSI
# ====================================================

elif menu == "input":

    st.title("📝 Input Data Instansi")

    with st.form("form_input"):

        nama = st.text_input("Nama Instansi")

        permasalahan = st.number_input(
            "Jumlah Permasalahan",
            min_value=0
        )

        permohonan = st.number_input(
            "Jumlah Permohonan",
            min_value=0
        )

        pertanyaan = st.number_input(
            "Jumlah Pertanyaan",
            min_value=0
        )

        col1, col2 = st.columns(2)

        tambah = col1.form_submit_button("➕ Tambah Data")
        reset = col2.form_submit_button("🧹 Hapus Isian")
        if tambah:

            if nama == "":
                st.warning("Nama instansi harus diisi")

            else:

                df = load_data()

                data_baru = {
                    "Asal Instansi": nama,
                    "Permasalahan": permasalahan,
                    "Permohonan": permohonan,
                    "Pertanyaan": pertanyaan
                }

                df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)

                save_data(df)

                st.success("Data berhasil disimpan")

        if reset:
            st.rerun()

    st.divider()

    st.subheader("📋 Data Instansi")

    df = load_data()

    st.dataframe(df, use_container_width=True)

    # ============================
    # HAPUS DATA
    # ============================

    if len(df) > 0:

        st.subheader("🗑 Hapus Data Instansi")

        instansi_hapus = st.selectbox(
            "Pilih Instansi",
            df["Asal Instansi"]
        )

        if st.button("Hapus Data"):

            df = df[df["Asal Instansi"] != instansi_hapus]

            save_data(df)

            st.success("Data berhasil dihapus")

            st.rerun()


# ====================================================
# CLUSTERING
# ====================================================

elif menu == "cluster":

    st.title("🤖 Cek Cluster Instansi")

    df = load_data()

    if len(df) < 4:

        st.warning("Minimal 4 data instansi untuk melakukan clustering")

    else:

        X = df[['Permasalahan','Permohonan','Pertanyaan']]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)

        df["Cluster"] = kmeans.fit_predict(X_scaled)

        cluster_names = {
            0: "Dominan Permasalahan",
            1: "Dominan Permohonan",
            2: "Dominan Pertanyaan",
            3: "Campuran"
        }

        df["Kategori Cluster"] = df["Cluster"].map(cluster_names)

        st.subheader("📊 Hasil Clustering")

        st.dataframe(
            df[["Asal Instansi","Kategori Cluster"]],
            use_container_width=True
        )