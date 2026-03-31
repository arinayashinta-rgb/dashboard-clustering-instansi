import streamlit as st
import pandas as pd
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        return pd.read_excel("dataset.xlsx")
    except:
        return pd.DataFrame({
            "Asal Instansi": ["A", "B"],
            "Cluster": [0, 1],
            "Kategori Cluster": ["Permasalahan", "Permohonan"]
        })

df = load_data()
df.columns = df.columns.str.strip()
df = df.fillna(0)

# =========================
# BACKGROUND
# =========================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("BG.jpg")

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page

# =========================
# STYLE
# =========================
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
}}

.glass {{
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 50px;
    max-width: 1200px;
    margin: auto;
}}

#MainMenu, footer {{
    visibility: hidden;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
def navbar():
    col1, col2 = st.columns([2,3])
    with col1:
        st.image("Unsia.png", width=200)
    with col2:
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("🏠 BERANDA"): go("home")
        if c2.button("📝 INPUT"): go("input")
        if c3.button("📊 HASIL"): go("hasil")
        if c4.button("👥 CLUSTER"): go("anggota")
        if c5.button("📂 DATASET"): go("dataset")

# =========================
# HOME
# =========================
if st.session_state.page == "home":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()
    st.markdown("<h1 style='font-size:70px;'>Selamat Datang</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
elif st.session_state.page == "input":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    with st.form("form_input"):
        nama = st.text_input("Nama Instansi")
        permasalahan = st.text_input("Permasalahan")
        permohonan = st.text_input("Permohonan")
        pertanyaan = st.text_input("Pertanyaan")
        total = st.text_input("Total")

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
            "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "-"
        }

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        html_table = "<table style='width:100%; border-collapse:collapse;'>"
        html_table += "<tr style='background:#0066ff;color:white;'>"
        html_table += "<th>Instansi</th><th>Total</th><th>Cluster</th><th>Kategori</th></tr>"

        html_table += "<tr>"
        html_table += f"<td>{data['nama']}</td>"
        html_table += f"<td>{data['total']}</td>"
        html_table += f"<td>{data['cluster']}</td>"
        html_table += f"<td>{data['kategori']}</td>"
        html_table += "</tr></table>"

        st.markdown(html_table, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ANGGOTA
# =========================
elif st.session_state.page == "anggota":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    cluster = st.selectbox("Cluster", df["Cluster"].unique())
    data_cluster = df[df["Cluster"] == cluster]

    html = "<table style='width:100%; border-collapse:collapse;'>"
    html += "<tr style='background:#0066ff;color:white;'>"
    html += "<th>Instansi</th><th>Cluster</th></tr>"

    for _, row in data_cluster.iterrows():
        html += f"<tr><td>{row['Asal Instansi']}</td><td>{row['Cluster']}</td></tr>"

    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DATASET
# =========================
elif st.session_state.page == "dataset":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    html = "<table style='width:100%; border-collapse:collapse;'>"
    html += "<tr style='background:#0066ff;color:white;'>"
    html += "<th>Instansi</th></tr>"

    for _, row in df.iterrows():
        html += f"<tr><td>{row['Asal Instansi']}</td></tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
```
