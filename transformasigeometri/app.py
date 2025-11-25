import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Transformasi Geometri")
st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Interaktif untuk Rotasi, Dilatasi, Refleksi, dan Translasi.")

# --- Fungsi Dasar (Objek) ---
def create_polygon(vertices):
    """Membuat poligon dasar dari list koordinat (misal: segitiga)"""
    # Menutup poligon dengan mengulang titik pertama
    polygon = np.array(vertices + [vertices[0]])
    return polygon.T # Transpose agar formatnya (2, N)

# --- Objek Awal (Segitiga) ---
initial_vertices = [[1, 1], [3, 4], [5, 1]]
initial_polygon_T = create_polygon(initial_vertices)

# --- Fungsi Visualisasi ---
def plot_transformation(original_points, transformed_points, title):
    """Membuat plot untuk visualisasi transformasi"""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot Asli
    ax.plot(original_points[0], original_points[1], 'b-', marker='o', label='Asli')
    ax.fill(original_points[0], original_points[1], 'lightblue', alpha=0.5)

    # Plot Hasil Transformasi
    ax.plot(transformed_points[0], transformed_points[1], 'r--', marker='x', label='Transformasi')
    ax.fill(transformed_points[0], transformed_points[1], 'salmon', alpha=0.5)

    # Pengaturan Plot
    all_points = np.hstack((original_points, transformed_points))
    max_range = np.max(np.abs(all_points)) * 1.5
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(title)
    ax.legend()
    return fig

# --- Sidebar untuk Input ---
st.sidebar.header("Konfigurasi Objek")

# Membiarkan user mengubah titik awal jika mau
st.sidebar.markdown("**Titik Sudut Awal (x, y)**")
x1 = st.sidebar.number_input("x1", value=1, key="x1_in")
y1 = st.sidebar.number_input("y1", value=1, key="y1_in")
x2 = st.sidebar.number_input("x2", value=3, key="x2_in")
y2 = st.sidebar.number_input("y2", value=4, key="y2_in")
x3 = st.sidebar.number_input("x3", value=5, key="x3_in")
y3 = st.sidebar.number_input("y3", value=1, key="y3_in")

current_vertices = [[x1, y1], [x2, y2], [x3, y3]]
initial_polygon_T = create_polygon(current_vertices)
st.sidebar.markdown("---")

# --- Konten Utama (Tab) ---
tab1, tab2, tab3, tab4 = st.tabs(["➡️ Translasi", "🔄 Rotasi", "🔍 Dilatasi", "↔️ Refleksi"])

# --- TAB 1: TRANSLASI (Pergeseran) ---
with tab1:
    st.header("➡️ Translasi (Pergeseran)")
    col_vis, col_param = st.columns([2, 1])

    with col_param:
        st.subheader("Parameter Translasi")
        tx = st.slider("Komponen x (tx)", -5.0, 5.0, 2.0)
        ty = st.slider("Komponen y (ty)", -5.0, 5.0, 1.0)
        st.markdown(f"**Vektor Translasi T = ({tx}, {ty})**")
        

[Image of geometric translation vector]


    # Transformasi Translasi
    # Membuat matriks vektor translasi yang disesuaikan dengan dimensi poligon (2, N)
    translation_vector = np.array([[tx], [ty]])
    T = np.tile(translation_vector, (1, initial_polygon_T.shape[1]))

    transformed_T = initial_polygon_T + T

    with col_vis:
        st.subheader("Visualisasi")
        fig_t = plot_transformation(initial_polygon_T, transformed_T, "Hasil Translasi")
        st.pyplot(fig_t)
        st.latex(f"P'(x', y') = P(x, y) + T(t_x, t_y) \\Rightarrow P' = ({x1}+{tx}, {y1}+{ty}), \\dots")


# --- TAB 2: ROTASI (Perputaran) ---
with tab2:
    st.header("🔄 Rotasi (Perputaran)")
    col_vis, col_param = st.columns([2, 1])

    with col_param:
        st.subheader("Parameter Rotasi (Pusat di (0,0))")
        angle_deg = st.slider("Sudut Rotasi (derajat)", -180, 180, 45)
        st.markdown(f"**Sudut $\\theta$ = {angle_deg}° (Berlawanan Arah Jarum Jam)**")
        

[Image of geometric rotation about the origin]


    # Transformasi Rotasi
    angle_rad = np.deg2rad(angle_deg)
    # Matriks Rotasi R:
    # [cos(theta) -sin(theta)]
    # [sin(theta)  cos(theta)]
    R = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])

    transformed_R = R @ initial_polygon_T # Matriks perkalian

    with col_vis:
        st.subheader("Visualisasi")
        fig_r = plot_transformation(initial_polygon_T, transformed_R, f"Hasil Rotasi {angle_deg}°")
        st.pyplot(fig_r)
        st.latex(r"""
            \begin{pmatrix} x' \\ y' \end{pmatrix} =
            \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}
            \begin{pmatrix} x \\ y \end{pmatrix}
        """)

# --- TAB 3: DILATASI (Penskalaan) ---
with tab3:
    st.header("🔍 Dilatasi (Penskalaan)")
    col_vis, col_param = st.columns([2, 1])

    with col_param:
        st.subheader("Parameter Dilatasi (Pusat di (0,0))")
        k_factor = st.slider("Faktor Skala (k)", 0.1, 3.0, 1.5, 0.1)
        st.markdown(f"**Faktor Skala k = {k_factor}**")
        

[Image of geometric dilation on a coordinate plane]


    # Transformasi Dilatasi
    # Matriks Dilatasi D:
    # [k 0]
    # [0 k]
    D = np.array([
        [k_factor, 0],
        [0, k_factor]
    ])

    transformed_D = D @ initial_polygon_T

    with col_vis:
        st.subheader("Visualisasi")
        fig_d = plot_transformation(initial_polygon_T, transformed_D, f"Hasil Dilatasi dengan k={k_factor}")
        st.pyplot(fig_d)
        st.latex(r"""
            \begin{pmatrix} x' \\ y' \end{pmatrix} =
            \begin{pmatrix} k & 0 \\ 0 & k \end{pmatrix}
            \begin{pmatrix} x \\ y \end{pmatrix}
        """)

# --- TAB 4: REFLEKSI (Pencerminan) ---
with tab4:
    st.header("↔️ Refleksi (Pencerminan)")
    col_vis, col_param = st.columns([2, 1])

    with col_param:
        st.subheader("Pilih Sumbu Pencerminan")
        reflection_axis = st.radio("Sumbu Refleksi",
                                   ['Sumbu X (y=0)', 'Sumbu Y (x=0)', 'Garis y=x', 'Garis y=-x'])
        

[Image of geometric reflection across the x and y axes]


    # Transformasi Refleksi
    M = np.identity(2) # Matriks Identitas 2x2 sebagai default

    if reflection_axis == 'Sumbu X (y=0)':
        # Matriks Refleksi Sumbu X:
        # [1  0]
        # [0 -1]
        M = np.array([[1, 0], [0, -1]])
        matrix_latex = r"""\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}"""
    elif reflection_axis == 'Sumbu Y (x=0)':
        # Matriks Refleksi Sumbu Y:
        # [-1 0]
        # [ 0 1]
        M = np.array([[-1, 0], [0, 1]])
        matrix_latex = r"""\begin{pmatrix} -1 & 0 \\ 0 & 1 \end{pmatrix}"""
    elif reflection_axis == 'Garis y=x':
        # Matriks Refleksi Garis y=x:
        # [0 1]
        # [1 0]
        M = np.array([[0, 1], [1, 0]])
        matrix_latex = r"""\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}"""
    elif reflection_axis == 'Garis y=-x':
        # Matriks Refleksi Garis y=-x:
        # [ 0 -1]
        # [-1  0]
        M = np.array([[0, -1], [-1, 0]])
        matrix_latex = r"""\begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}"""

    transformed_F = M @ initial_polygon_T

    with col_vis:
        st.subheader("Visualisasi")
        fig_f = plot_transformation(initial_polygon_T, transformed_F, f"Hasil Refleksi terhadap {reflection_axis}")
        st.pyplot(fig_f)
        st.latex(r"""
            \begin{pmatrix} x' \\ y' \end{pmatrix} =
            """ + matrix_latex +
            r"""
            \begin{pmatrix} x \\ y \end{pmatrix}
        """)
