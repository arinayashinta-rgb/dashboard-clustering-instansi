import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

st.set_page_config(
    page_title="Dashboard Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# HEADER
# =========================

# =========================
# SESSION MENU
# =========================

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

# =========================
# SIDEBAR MENU
# =========================

st.sidebar.title("📁 Navigasi Dashboard")

if st.sidebar.button("🏠 Beranda"):
    st.session_state.menu = "Beranda"

if st.sidebar.button("📂 Upload Dataset"):
    st.session_state.menu = "Upload"

if st.sidebar.button("⚙️ Preprocessing Data"):
    st.session_state.menu = "Preprocessing"

if st.sidebar.button("📉 Elbow Method"):
    st.session_state.menu = "Elbow"

if st.sidebar.button("📊 Silhouette Score"):
    st.session_state.menu = "Silhouette"

if st.sidebar.button("🤖 Clustering"):
    st.session_state.menu = "Clustering"

if st.sidebar.button("📈 Visualisasi Cluster"):
    st.session_state.menu = "Visualisasi"

if st.sidebar.button("📋 Tabel Instansi Cluster"):
    st.session_state.menu = "Tabel"

menu = st.session_state.menu

# =========================
# BERANDA
# =========================

if menu == "Beranda":

    st.title("📊 Dashboard Analisis Clustering Instansi")

    st.markdown("""
    Dashboard ini digunakan untuk **melakukan clustering instansi pelapor**
    menggunakan metode **K-Means Clustering**.
    """)

    st.divider()

    if "data" in st.session_state:

        df = st.session_state["data"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Data", len(df))
        col2.metric("Jumlah Instansi", df["Asal Instansi"].nunique())
        col3.metric("Jumlah Variabel", len(df.columns))

    else:

        st.info("Upload dataset untuk melihat statistik dashboard.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🧠 Metode K-Means Clustering")

        st.markdown("""
        **K-Means** digunakan untuk mengelompokkan instansi berdasarkan:

        - Jumlah **Permasalahan**
        - Jumlah **Permohonan**
        - Jumlah **Pertanyaan**

        Hasil clustering menghasilkan dua kelompok utama:

        - Volume Pengaduan Tinggi
        - Volume Pengaduan Rendah
        """)

    with col2:

        st.subheader("📊 Alur Analisis")

        st.markdown("""
        1️⃣ Upload dataset  
        2️⃣ Preprocessing data  
        3️⃣ Elbow Method  
        4️⃣ Silhouette Score  
        5️⃣ Clustering  
        6️⃣ Visualisasi cluster  
        """)

# =========================
# UPLOAD DATASET
# =========================

elif menu == "Upload":

    st.subheader("Upload Dataset")

    file = st.file_uploader("Upload dataset Excel", type=["xlsx"])

    if file is not None:

        df = pd.read_excel(file)

        st.session_state["data"] = df

        col1, col2, col3 = st.columns(3)

        col1.metric("Jumlah Data", len(df))
        col2.metric("Jumlah Kolom", len(df.columns))
        col3.metric("Jumlah Instansi", df["Asal Instansi"].nunique())

        st.dataframe(df, use_container_width=True)

# =========================
# PREPROCESSING
# =========================

elif menu == "Preprocessing":

    st.subheader("Preprocessing Data")

    if "data" not in st.session_state:

        st.warning("Silakan upload dataset terlebih dahulu")

    else:

        df = st.session_state["data"]

        df.columns = df.columns.str.strip()
        df = df.drop_duplicates()

        cols = ['Permasalahan','Permohonan','Pertanyaan']

        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df[cols] = df[cols].fillna(0)

        df_instansi = df.groupby('Asal Instansi')[cols].sum().reset_index()

        df_instansi[cols] = np.log1p(df_instansi[cols])

        X = df_instansi[cols]

        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)

        IQR = Q3 - Q1

        X = X[~((X < (Q1 - 1.5 * IQR)) | (X > (Q3 + 1.5 * IQR))).any(axis=1)]

        df_instansi = df_instansi.loc[X.index].reset_index(drop=True)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        st.session_state["df_instansi"] = df_instansi
        st.session_state["X_scaled"] = X_scaled
        st.session_state["X_pca"] = X_pca

        st.success("Preprocessing berhasil")

        st.dataframe(df_instansi, use_container_width=True)

# =========================
# ELBOW METHOD
# =========================

elif menu == "Elbow":

    st.subheader("Elbow Method")

    if "X_scaled" not in st.session_state:

        st.warning("Lakukan preprocessing terlebih dahulu")

    else:

        X_scaled = st.session_state["X_scaled"]

        wcss = []

        for k in range(1,10):

            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_scaled)

            wcss.append(kmeans.inertia_)

        fig, ax = plt.subplots(figsize=(5,4))  # ukuran lebih kecil

        ax.plot(range(1,10), wcss, marker='o')

        ax.set_title("Elbow Method", fontsize=11)
        ax.set_xlabel("Jumlah Cluster", fontsize=9)
        ax.set_ylabel("WCSS", fontsize=9)

        plt.tight_layout()

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            st.pyplot(fig)

# =========================
# SILHOUETTE SCORE
# =========================

elif menu == "Silhouette":

    st.subheader("Silhouette Score")

    if "X_pca" not in st.session_state:

        st.warning("Lakukan preprocessing terlebih dahulu")

    else:

        X_pca = st.session_state["X_pca"]

        scores = []
        range_k = range(2,10)

        for k in range_k:

            model = KMeans(n_clusters=k, random_state=42, n_init=50)

            labels = model.fit_predict(X_pca)

            score = silhouette_score(X_pca, labels)

            scores.append(score)

        fig, ax = plt.subplots(figsize=(5,4))  # ukuran kecil

        ax.plot(range_k, scores, marker='o')

        ax.set_title("Silhouette Score", fontsize=11)
        ax.set_xlabel("Jumlah Cluster", fontsize=9)
        ax.set_ylabel("Score", fontsize=9)

        plt.tight_layout()

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            st.pyplot(fig)

        st.metric("Silhouette Score Tertinggi", round(max(scores),3))
# =========================
# CLUSTERING
# =========================

elif menu == "Clustering":

    st.subheader("K-Means Clustering")

    if "X_pca" not in st.session_state:

        st.warning("Lakukan preprocessing terlebih dahulu")

    else:

        df_instansi = st.session_state["df_instansi"].copy()
        X_pca = st.session_state["X_pca"]

        st.markdown("### Pilih Jumlah Cluster (K)")

        k = st.selectbox(
            "Jumlah Cluster",
            options=[2,3,4,5],
            index=0
        )

        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=50
        )

        df_instansi['Cluster'] = kmeans.fit_predict(X_pca)

        cols = ['Permasalahan','Permohonan','Pertanyaan']

        centroids = df_instansi.groupby('Cluster')[cols].mean()

        centroids['total'] = centroids.mean(axis=1)

        cluster_high = centroids['total'].idxmax()
        cluster_low = centroids['total'].idxmin()

        cluster_names = {
            cluster_high: 'Volume Pengaduan Tinggi',
            cluster_low: 'Volume Pengaduan Rendah'
        }

        df_instansi['Nama_Cluster'] = df_instansi['Cluster'].map(cluster_names)

        st.session_state["cluster_data"] = df_instansi

        # =========================
        # METRIC
        # =========================

        score = silhouette_score(X_pca, df_instansi['Cluster'])

        col1, col2 = st.columns(2)

        col1.metric("Jumlah Cluster", k)
        col2.metric("Silhouette Score", round(score,3))

        st.divider()

        st.subheader("Hasil Clustering")

        st.dataframe(df_instansi, use_container_width=True)
# =========================
# VISUALISASI CLUSTER
# =========================

elif menu == "Visualisasi":

    st.subheader("Visualisasi Cluster 3D")

    if "cluster_data" not in st.session_state:

        st.warning("Lakukan proses clustering terlebih dahulu")

    else:

        df_instansi = st.session_state["cluster_data"]

        sns.set_theme(style="ticks")

        # ukuran figure lebih kecil
        fig = plt.figure(figsize=(6,5))
        ax = fig.add_subplot(111, projection='3d')

        clusters = sorted(df_instansi['Cluster'].unique())

        colors = sns.color_palette("bright", len(clusters))

        # plot titik cluster
        for i, cluster in enumerate(clusters):

            data_cluster = df_instansi[df_instansi['Cluster'] == cluster]

            ax.scatter(
                data_cluster['Permasalahan'],
                data_cluster['Permohonan'],
                data_cluster['Pertanyaan'],

                s=40,                 # ukuran titik lebih kecil
                color=colors[i],
                edgecolor='black',
                linewidth=0.5,
                alpha=0.9,

                label=f'Cluster {cluster}'
            )

        # centroid cluster
        centroids = df_instansi.groupby('Cluster')[[
            'Permasalahan',
            'Permohonan',
            'Pertanyaan'
        ]].mean()

        ax.scatter(
            centroids['Permasalahan'],
            centroids['Permohonan'],
            centroids['Pertanyaan'],

            c='red',
            s=150,                 # centroid lebih kecil
            marker='X',
            edgecolor='black',
            linewidth=2,
            label='Centroid'
        )

        # label sumbu
        ax.set_xlabel("Permasalahan", fontsize=9)
        ax.set_ylabel("Permohonan", fontsize=9)
        ax.set_zlabel("Pertanyaan", fontsize=9)

        # judul
        ax.set_title(
            "Visualisasi Cluster Instansi",
            fontsize=11
        )

        # sudut kamera
        ax.view_init(elev=30, azim=120)

        # legend
        ax.legend(fontsize=8)

        # proporsi grafik
        ax.set_box_aspect((1,1,1))

        plt.tight_layout()

        # menampilkan grafik di tengah halaman
        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            st.pyplot(fig)
# =========================
# TABEL CLUSTER
# =========================

elif menu == "Tabel":

    st.subheader("Tabel Instansi Cluster")

    if "cluster_data" not in st.session_state:

        st.warning("Lakukan clustering terlebih dahulu")

    else:

        df_instansi = st.session_state["cluster_data"]

        tabel_instansi_cluster = df_instansi[[
            'Asal Instansi',            
            'Cluster',
            'Nama_Cluster'
        ]]

        cluster_filter = st.selectbox(
            "Filter Cluster",
            ["Semua"] + list(tabel_instansi_cluster["Nama_Cluster"].unique())
        )

        if cluster_filter != "Semua":

            tabel_instansi_cluster = tabel_instansi_cluster[
                tabel_instansi_cluster["Nama_Cluster"] == cluster_filter
            ]

        st.dataframe(tabel_instansi_cluster, use_container_width=True)


st.set_page_config(
    page_title="Dashboard Clustering Instansi",
    page_icon="📊",
    layout="wide"
)