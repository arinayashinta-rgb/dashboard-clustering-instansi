import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

st.set_page_config(
    page_title="Clustering Instansi",
    layout="wide"
)

# ======================
# SESSION STATE
# ======================

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

# ======================
# SIDEBAR MENU
# ======================

st.sidebar.title("Menu Dashboard")

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
    Aplikasi ini digunakan untuk melakukan **clustering instansi**
    berdasarkan:

    - Permasalahan
    - Permohonan
    - Pertanyaan

    Menggunakan metode **K-Means Clustering**.
    """)

    st.info("Silakan mulai dari menu **Import Data**")


# ======================
# IMPORT DATA
# ======================

elif menu == "Import":

    st.title("Import Data Instansi")

    file = st.file_uploader("Upload file Excel", type=["xlsx"])

    if file is not None:

        df = pd.read_excel(file)

        st.session_state["data"] = df

        st.success("Data berhasil diupload")

        st.write("Preview Data")

        st.dataframe(df)


# ======================
# PREPROCESSING
# ======================

elif menu == "Preprocessing":

    st.title("Preprocessing Data")

    if "data" not in st.session_state:

        st.warning("Upload data terlebih dahulu")

    else:

        df = st.session_state["data"]

        st.subheader("Cek Missing Value")

        st.write(df.isnull().sum())

        # hapus missing
        df = df.dropna()

        # hapus duplikasi
        df = df.drop_duplicates()

        st.success("Missing value dan duplikasi telah dibersihkan")

        X = df[['Permasalahan','Permohonan','Pertanyaan']]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        st.session_state["df_clean"] = df
        st.session_state["X_scaled"] = X_scaled
        st.session_state["scaler"] = scaler

        st.write("Data setelah preprocessing")

        st.dataframe(df)


# ======================
# CLUSTERING
# ======================

elif menu == "Clustering":

    st.title("Clustering Instansi")

    if "X_scaled" not in st.session_state:

        st.warning("Lakukan preprocessing terlebih dahulu")

    else:

        df = st.session_state["df_clean"].copy()
        X_scaled = st.session_state["X_scaled"]

        st.subheader("Menentukan Jumlah Cluster")

        k = st.slider("Pilih jumlah cluster", 2, 6, 4)

        # silhouette
        labels = KMeans(n_clusters=k, random_state=42).fit_predict(X_scaled)

        score = silhouette_score(X_scaled, labels)

        st.metric("Silhouette Score", round(score,3))

        # elbow method
        wcss = []

        for i in range(1,10):

            kmeans = KMeans(n_clusters=i, random_state=42)

            kmeans.fit(X_scaled)

            wcss.append(kmeans.inertia_)

        fig, ax = plt.subplots()

        ax.plot(range(1,10), wcss, marker='o')

        ax.set_xlabel("Jumlah Cluster")
        ax.set_ylabel("WCSS")

        ax.set_title("Elbow Method")

        st.pyplot(fig)

        # ======================
        # MODEL CLUSTER
        # ======================

        kmeans = KMeans(n_clusters=k, random_state=42)

        labels = kmeans.fit_predict(X_scaled)

        df['Cluster'] = labels

        cluster_summary = df.groupby('Cluster')[[
            'Permasalahan',
            'Permohonan',
            'Pertanyaan'
        ]].mean()

        st.subheader("Rata-rata tiap cluster")

        st.dataframe(cluster_summary)

        cluster_names = {
            0: "Dominan Permasalahan",
            1: "Dominan Permohonan",
            2: "Dominan Pertanyaan",
            3: "Campuran"
        }

        df['Kategori Cluster'] = df['Cluster'].map(cluster_names)

        st.subheader("Hasil Clustering")

        hasil = df[['Asal Instansi','Cluster','Kategori Cluster']]

        st.dataframe(hasil)

        st.subheader("Instansi masuk cluster mana")

        instansi = st.selectbox(
            "Pilih Instansi",
            df['Asal Instansi']
        )

        hasil_instansi = hasil[hasil['Asal Instansi'] == instansi]

        st.success(
            f"Instansi {instansi} masuk ke {hasil_instansi['Kategori Cluster'].values[0]}"
        )