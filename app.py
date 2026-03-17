import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Dashboard Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =============================
# SESSION STATE
# =============================

if "menu" not in st.session_state:
    st.session_state.menu = "beranda"

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Asal Instansi",
        "Permasalahan",
        "Permohonan",
        "Pertanyaan"
    ])

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "permasalahan" not in st.session_state:
    st.session_state.permasalahan = 0

if "permohonan" not in st.session_state:
    st.session_state.permohonan = 0

if "pertanyaan" not in st.session_state:
    st.session_state.pertanyaan = 0

# =============================
# SIDEBAR MENU
# =============================

st.sidebar.title("📁 Navigasi")

if st.sidebar.button("🏠 Beranda"):
    st.session_state.menu = "beranda"

if st.sidebar.button("📝 Input Data Instansi"):
    st.session_state.menu = "input"

if st.sidebar.button("🤖 Cek Cluster Instansi"):
    st.session_state.menu = "cluster"

menu = st.session_state.menu


# =====================================================
# HALAMAN BERANDA
# =====================================================

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

    st.divider()

    col1, col2, col3 = st.columns(3)

    total_data = len(st.session_state.data)
    total_instansi = st.session_state.data["Asal Instansi"].nunique()

    col1.metric("Jumlah Data", total_data)
    col2.metric("Jumlah Instansi", total_instansi)
    col3.metric("Jumlah Variabel", 3)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🧠 Tentang Clustering")

        st.markdown("""
        **Clustering** adalah metode dalam data mining
        yang digunakan untuk mengelompokkan data berdasarkan
        karakteristik yang mirip.

        Dalam dashboard ini digunakan algoritma:

        **K-Means Clustering**
        """)

    with col2:

        st.subheader("📊 Alur Penggunaan Dashboard")

        st.markdown("""
        1️⃣ Input data instansi  
        2️⃣ Tambahkan beberapa instansi  
        3️⃣ Jalankan clustering  
        4️⃣ Lihat instansi masuk cluster mana  
        """)


# =====================================================
# HALAMAN INPUT DATA INSTANSI
# =====================================================

elif menu == "input":

    st.title("📝 Input Data Instansi")

    st.subheader("Form Input")

    nama = st.text_input(
        "Nama Instansi",
        key="nama"
    )

    permasalahan = st.number_input(
        "Jumlah Permasalahan",
        min_value=0,
        key="permasalahan"
    )

    permohonan = st.number_input(
        "Jumlah Permohonan",
        min_value=0,
        key="permohonan"
    )

    pertanyaan = st.number_input(
        "Jumlah Pertanyaan",
        min_value=0,
        key="pertanyaan"
    )

    col1, col2 = st.columns(2)

    if col1.button("➕ Tambah Data"):

        if nama == "":
            st.warning("Nama instansi harus diisi")
        else:

            data_baru = {
                "Asal Instansi": nama,
                "Permasalahan": permasalahan,
                "Permohonan": permohonan,
                "Pertanyaan": pertanyaan
            }

            st.session_state.data = pd.concat(
                [st.session_state.data, pd.DataFrame([data_baru])],
                ignore_index=True
            )

            st.success("Data berhasil ditambahkan")

            st.session_state.nama = ""
            st.session_state.permasalahan = 0
            st.session_state.permohonan = 0
            st.session_state.pertanyaan = 0

            st.rerun()

    if col2.button("🧹 Hapus Isian"):

        st.session_state.nama = ""
        st.session_state.permasalahan = 0
        st.session_state.permohonan = 0
        st.session_state.pertanyaan = 0

        st.rerun()

    st.divider()

    st.subheader("📋 Data Instansi")

    df = st.session_state.data

    st.dataframe(df, use_container_width=True)

    if len(df) > 0:

        st.subheader("🗑 Hapus Data Instansi")

        instansi_hapus = st.selectbox(
            "Pilih Instansi",
            df["Asal Instansi"]
        )

        if st.button("Hapus Data"):

            st.session_state.data = df[
                df["Asal Instansi"] != instansi_hapus
            ]

            st.success("Data berhasil dihapus")

            st.rerun()

    if len(df) > 0:

        st.subheader("✏ Edit Data Instansi")

        instansi_edit = st.selectbox(
            "Pilih Instansi untuk Edit",
            df["Asal Instansi"],
            key="edit"
        )

        data_edit = df[df["Asal Instansi"] == instansi_edit].iloc[0]

        permasalahan_edit = st.number_input(
            "Permasalahan Baru",
            value=int(data_edit["Permasalahan"])
        )

        permohonan_edit = st.number_input(
            "Permohonan Baru",
            value=int(data_edit["Permohonan"])
        )

        pertanyaan_edit = st.number_input(
            "Pertanyaan Baru",
            value=int(data_edit["Pertanyaan"])
        )

        if st.button("Update Data"):

            idx = df[df["Asal Instansi"] == instansi_edit].index[0]

            st.session_state.data.loc[idx,
                ["Permasalahan","Permohonan","Pertanyaan"]
            ] = [
                permasalahan_edit,
                permohonan_edit,
                pertanyaan_edit
            ]

            st.success("Data berhasil diperbarui")

            st.rerun()


# =====================================================
# HALAMAN CLUSTERING
# =====================================================

elif menu == "cluster":

    st.title("🤖 Cek Cluster Instansi")

    df = st.session_state.data.copy()

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