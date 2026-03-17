import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Instansi", layout="wide")

# ======================
# SESSION STATE
# ======================

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

# ======================
# SIDEBAR
# ======================

st.sidebar.title("Menu")

if st.sidebar.button("Beranda"):
    st.session_state.menu = "Beranda"

if st.sidebar.button("Import Data"):
    st.session_state.menu = "Import"

if st.sidebar.button("Preprocessing"):
    st.session_state.menu = "Preprocessing"

if st.sidebar.button("Clustering"):
    st.session_state.menu = "Clustering"

menu = st.session_state.menu


# ======================
# BERANDA
# ======================

if menu == "Beranda":

    st.title("Dashboard Clustering Instansi")

    st.write("""
    Sistem ini digunakan untuk melakukan **clustering instansi**
    berdasarkan jumlah:

    - Permasalahan
    - Permohonan
    - Pertanyaan

    Setelah model dibuat, Anda bisa **menginput instansi baru**
    untuk mengetahui instansi tersebut **masuk cluster mana**.
    """)


# ======================
# IMPORT DATA
# ======================

elif menu == "Import":

    st.title("Import Dataset")

    file = st.file_uploader("Upload dataset Excel", type=["xlsx"])

    if file is not None:

        df = pd.read_excel(file)

        st.session_state["data"] = df

        st.success("Dataset berhasil diupload")

        st.dataframe(df)


# ======================
# PREPROCESSING
# ======================

elif menu == "Preprocessing":

    st.title("Preprocessing Data")

    if "data" not in st.session_state:

        st.warning("Upload dataset terlebih dahulu")

    else:

        df = st.session_state["data"]

        # hapus missing
        df = df.dropna()

        # hapus duplikat
        df = df.drop_duplicates()

        X = df[['Permasalahan','Permohonan','Pertanyaan']]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        st.session_state["df_clean"] = df
        st.session_state["X_scaled"] = X_scaled
        st.session_state["scaler"] = scaler

        st.success("Preprocessing selesai")

        st.dataframe(df)


# ======================
# CLUSTERING + PREDIKSI
# ======================

elif menu == "Clustering":

    st.title("Clustering Instansi")

    if "X_scaled" not in st.session_state:

        st.warning("Lakukan preprocessing terlebih dahulu")

    else:

        df = st.session_state["df_clean"].copy()
        X_scaled = st.session_state["X_scaled"]
        scaler = st.session_state["scaler"]

        # model clustering
        kmeans = KMeans(n_clusters=4, random_state=42)

        df['Cluster'] = kmeans.fit_predict(X_scaled)

        st.session_state["kmeans"] = kmeans

        cluster_names = {
            0: "Dominan Permasalahan",
            1: "Dominan Permohonan",
            2: "Dominan Pertanyaan",
            3: "Campuran"
        }

        df['Kategori Cluster'] = df['Cluster'].map(cluster_names)

        st.subheader("Hasil Clustering Dataset")

        st.dataframe(df[['Asal Instansi','Cluster','Kategori Cluster']])

        st.divider()

        # ======================
        # INPUT INSTANSI BARU
        # ======================

        st.subheader("Coba Cluster Instansi Baru")

        nama = st.text_input("Nama Instansi")

        permasalahan = st.number_input("Jumlah Permasalahan", min_value=0)

        permohonan = st.number_input("Jumlah Permohonan", min_value=0)

        pertanyaan = st.number_input("Jumlah Pertanyaan", min_value=0)

        if st.button("Proses Clustering"):

            data_baru = np.array([[permasalahan, permohonan, pertanyaan]])

            data_scaled = scaler.transform(data_baru)

            cluster = kmeans.predict(data_scaled)[0]

            kategori = cluster_names.get(cluster, "Cluster Tidak Diketahui")

            st.success(
                f"Instansi **{nama}** masuk ke cluster: **{kategori}**"
            )