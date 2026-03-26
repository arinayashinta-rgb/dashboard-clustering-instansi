# =========================
# HASIL CLUSTERING
# =========================
elif menu == "Hasil Clustering":

    st.title("📊 Hasil Clustering")

    if st.session_state.hasil:
        data = st.session_state.hasil

        # =========================
        # SECTION 1: DATA INSTANSI
        # =========================
        st.subheader("📌 Informasi Instansi")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Nama Instansi**")
            st.write(data['nama'])

        with col2:
            st.write("**Status Data**")
            if data["cluster"] is not None:
                st.success("Ditemukan")
            else:
                st.error("Tidak ditemukan")

        st.divider()

        # =========================
        # SECTION 2: ISI INPUT
        # =========================
        st.subheader("📝 Detail Input")

        with st.container():
            st.write("**Permasalahan**")
            st.write(data["permasalahan"] or "-")

            st.write("**Permohonan**")
            st.write(data["permohonan"] or "-")

            st.write("**Pertanyaan**")
            st.write(data["pertanyaan"] or "-")

        st.divider()

        # =========================
        # SECTION 3: HASIL
        # =========================
        st.subheader("🎯 Hasil Clustering")

        col1, col2 = st.columns(2)

        with col1:
            if data["cluster"] is not None:
                st.success(f"Cluster: {data['cluster']}")
            else:
                st.error("Cluster tidak tersedia")

        with col2:
            if data["cluster"] is not None:
                st.info(f"Kategori: {data['kategori']}")
            else:
                st.warning("-")

        st.divider()

        # =========================
        # SECTION 4: RINCIAN
        # =========================
        st.subheader("📊 Rincian Input")

        def hitung_jumlah(teks):
            if not teks:
                return 0
            return len([line for line in teks.split("\n") if line.strip()])

        jml_permasalahan = hitung_jumlah(data.get("permasalahan", ""))
        jml_permohonan = hitung_jumlah(data.get("permohonan", ""))
        jml_pertanyaan = hitung_jumlah(data.get("pertanyaan", ""))

        col1, col2, col3 = st.columns(3)

        col1.metric("Permasalahan", jml_permasalahan)
        col2.metric("Permohonan", jml_permohonan)
        col3.metric("Pertanyaan", jml_pertanyaan)

    else:
        st.warning("Silakan input data terlebih dahulu.")