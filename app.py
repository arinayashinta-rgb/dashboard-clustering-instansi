import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Instansi", layout="wide")

# =========================
# SESSION STATE
# =========================

if "menu" not in st.session_state:
    st.session_state.menu = "Input"

if "data_instansi" not in st.session_state:
    st.session_state.data_instansi = pd.DataFrame(columns=[
        "Asal Instansi",
        "Permasalahan",
        "Permohonan",
        "Pertanyaan"
    ])

# =========================
# SIDEBAR MENU
# =========================

st.sidebar.title("Menu Dashboard")

if st.sidebar.button("Input Data Instansi"):
    st.session_state.menu = "Input"

if st.sidebar.button("Cek Cluster Instansi"):
    st.session_state.menu = "Cluster"

menu = st.session_state.menu


# =====================================================
# HALAMAN 1 : INPUT DATA INSTANSI
# =====================================================

if menu == "Input":

    st.title("Input Data Instansi")

    st.subheader("Tambah / Edit Data")

    nama = st.text_input("Nama Instansi")

    permasalahan = st.number_input("Jumlah Permasalahan", min_value=0)

    permohonan = st.number_input("Jumlah Permohonan", min_value=0)

    pertanyaan = st.number_input("Jumlah Pertanyaan", min_value=0)

    col1, col2 = st.columns(2)

    # =========================
    # TAMBAH DATA
    # =========================

    if col1.button("Tambah Data"):

        data_baru = {
            "Asal Instansi": nama,
            "Permasalahan": permasalahan,
            "Permohonan": permohonan,
            "Pertanyaan": pertanyaan
        }

        st.session_state.data_instansi = pd.concat(
            [st.session_state.data_instansi, pd.DataFrame([data_baru])],
            ignore_index=True
        )

        st.success("Data berhasil ditambahkan")

    # =========================
    # RESET FORM
    # =========================

    if col2.button("Hapus Isian"):
        st.rerun()

    st.divider()

    # =========================
    # TABEL DATA
    # =========================

    st.subheader("Data Instansi")

    df = st.session_state.data_instansi

    st.dataframe(df, use_container_width=True)

    # =========================
    # HAPUS DATA
    # =========================

    if len(df) > 0:

        st.subheader("Hapus Data Instansi")

        instansi_hapus = st.selectbox(
            "Pilih Instansi",
            df["Asal Instansi"]
        )

        if st.button("Hapus Data"):

            st.session_state.data_instansi = df[
                df["Asal Instansi"] != instansi_hapus
            ]

            st.success("Data berhasil dihapus")

            st.rerun()

    # =========================
    # EDIT DATA
    # =========================

    if len(df) > 0:

        st.subheader("Edit Data Instansi")

        instansi_edit = st.selectbox(
            "Pilih Instansi untuk Edit",
            df["Asal Instansi"],
            key="edit_instansi"
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

            st.session_state.data_instansi.loc[idx,
                ["Permasalahan","Permohonan","Pertanyaan"]
            ] = [
                permasalahan_edit,
                permohonan_edit,
                pertanyaan_edit
            ]

            st.success("Data berhasil diperbarui")

            st.rerun()


# =====================================================
# HALAMAN 2 : CEK CLUSTER INSTANSI
# =====================================================

elif menu == "Cluster":

    st.title("Cek Cluster Instansi")

    df = st.session_state.data_instansi

    if len(df) < 4:

        st.warning("Minimal 4 data instansi untuk melakukan clustering")

    else:

        X = df[['Permasalahan','Permohonan','Pertanyaan']]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)

        df['Cluster'] = kmeans.fit_predict(X_scaled)

        cluster_names = {
            0: "Dominan Permasalahan",
            1: "Dominan Permohonan",
            2: "Dominan Pertanyaan",
            3: "Campuran"
        }

        df['Kategori Cluster'] = df['Cluster'].map(cluster_names)

        st.subheader("Hasil Clustering")

        st.dataframe(df[['Asal Instansi','Kategori Cluster']],
                     use_container_width=True)