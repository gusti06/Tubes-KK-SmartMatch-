"""
SmartMatch Application Orchestrator & UI (Python Streamlit Version)
"""

import os
import csv
import math
import time
# pyrefly: ignore [missing-import]
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set Streamlit page configuration for a premium look
st.set_page_config(
    page_title="SmartMatch - Laptop Recommendation System",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load backend logic
from fuzzy import preprocess_laptop, evaluate_laptop_suitability
from pso import PSOManager

# Exchange rates
RATES = {
    'EUR_TO_IDR': 20521.0,
    'USD_TO_IDR': 17701.0,
    'EUR_TO_USD': 1.16
}

# --- Core Helper Functions ---

def get_budget_in_euro(value, from_currency):
    if from_currency == 'EUR':
        return value
    if from_currency == 'IDR':
        return value / RATES['EUR_TO_IDR']
    if from_currency == 'USD':
        return value / RATES['EUR_TO_USD']
    return value

def format_price(price_in_eur, target_currency):
    if target_currency == 'EUR':
        return f"€ {price_in_eur:,.2f}"
    if target_currency == 'USD':
        price_in_usd = price_in_eur * RATES['EUR_TO_USD']
        return f"$ {price_in_usd:,.2f}"
    if target_currency == 'IDR':
        price_in_idr = price_in_eur * RATES['EUR_TO_IDR']
        return f"Rp {price_in_idr:,.0f}".replace(",", ".")
    return f"{price_in_eur:.2f}"

@st.cache_data
def load_dataset(csv_path):
    laptops = []
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                laptop = {
                    'company': row['Company'],
                    'product': row['Product'],
                    'typeName': row['TypeName'],
                    'inches': float(row['Inches']),
                    'screenResolution': row['ScreenResolution'],
                    'cpuCompany': row['CPU_Company'],
                    'cpuType': row['CPU_Type'],
                    'cpuFreq': float(row['CPU_Frequency (GHz)']),
                    'ram': float(row['RAM (GB)']),
                    'memory': row['Memory'],
                    'gpuCompany': row['GPU_Company'],
                    'gpuType': row['GPU_Type'],
                    'opsys': row['OpSys'],
                    'weight': float(row['Weight (kg)']),
                    'price': float(row['Price (Euro)'])
                }
                laptops.append(laptop)
            except Exception:
                continue
    return laptops

def calculate_distance_to_optimal(laptop, optimal_specs):
    # optimal_specs = [Price, RAM, Weight, Performance]
    opt_price, opt_ram, opt_weight, opt_perf = optimal_specs

    # Normalized diffs
    diff_price = (laptop['price'] - opt_price) / (4000.0 - 150.0)
    diff_ram = (laptop['ram'] - opt_ram) / (32.0 - 2.0)
    diff_weight = (laptop['weight'] - opt_weight) / (4.5 - 0.6)
    diff_perf = (laptop['perfScore'] - opt_perf) / (100.0 - 10.0)

    # Weighted Euclidean distance
    dist = math.sqrt(
        0.35 * (diff_price ** 2) +
        0.25 * (diff_ram ** 2) +
        0.15 * (diff_weight ** 2) +
        0.25 * (diff_perf ** 2)
    )
    return dist

def get_recommendations(laptops, prefs, optimal_specs):
    results = []
    for laptop in laptops:
        l = preprocess_laptop(laptop)
        fuzzy_eval = evaluate_laptop_suitability(l, prefs)

        # Hybrid Matching: combining fuzzy score (70%) and proximity to optimal specs (30%)
        distance = calculate_distance_to_optimal(l, optimal_specs)
        proximity_score = max(0.0, (1.0 - distance) * 100.0)

        # Overall recommendation score
        final_score = round(fuzzy_eval['score'] * 0.7 + proximity_score * 0.3)

        category = "Tidak Direkomendasikan"
        css_class = "not-rec"
        if final_score >= 80:
            category = "Sangat Direkomendasikan"
            css_class = "highly-rec"
        elif final_score >= 60:
            category = "Direkomendasikan"
            css_class = "rec"
        elif final_score >= 40:
            category = "Cukup Cocok"
            css_class = "fairly-rec"

        results.append({
            'laptop': l,
            'score': final_score,
            'category': category,
            'cssClass': css_class,
            'reasons': fuzzy_eval['reasons'],
            'perfScore': fuzzy_eval['perfScore'],
            'batteryScore': fuzzy_eval['batteryScore']
        })

    # Sort results descending by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# --- CSS Styling for Glassmorphism Look ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00f2fe;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        text-align: center;
        color: #8e9aaf;
        margin-bottom: 2rem;
        font-size: 1rem;
    }
    .card {
        background-color: #1e2230;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 5px solid #00f2fe;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .highly-rec-card { border-left-color: #00e676; }
    .rec-card { border-left-color: #00f2fe; }
    .fairly-rec-card { border-left-color: #ff9100; }
    .not-rec-card { border-left-color: #ff5252; }
    
    .card-title {
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.3rem;
        color: #ffffff;
    }
    .card-meta {
        font-size: 0.85rem;
        color: #8e9aaf;
        margin-bottom: 0.6rem;
    }
    .score-badge {
        float: right;
        background-color: #2e354f;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .highly-rec-badge { color: #00e676; }
    .rec-badge { color: #00f2fe; }
    .fairly-rec-badge { color: #ff9100; }
    
    .price-tag {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
    }
    .reason-bullet {
        font-size: 0.85rem;
        color: #b0c4de;
        margin-left: 0.5rem;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App Layout ---

st.markdown('<div class="main-header">💻 SmartMatch Laptop</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistem Rekomendasi Laptop berbasis Computational Intelligence (Fuzzy Logic + PSO)</div>', unsafe_allow_html=True)

# Path dataset
csv_path = "laptop_price - dataset.csv"
laptops = load_dataset(csv_path)

if not laptops:
    st.error("File dataset `laptop_price - dataset.csv` tidak ditemukan di direktori project. Silakan unggah file tersebut.")
    st.stop()

# --- SIDEBAR INPUTS ---
st.sidebar.header("🎯 Preferensi Anda")

# Currency Select
currency = st.sidebar.selectbox("Pilih Mata Uang", options=["IDR", "USD", "EUR"], index=0)

# Budget Input
if currency == 'IDR':
    budget_input = st.sidebar.number_input("Budget Maksimum (Rupiah)", value=15000000, step=500000, min_value=1)
elif currency == 'USD':
    budget_input = st.sidebar.number_input("Budget Maksimum (USD)", value=900, step=50, min_value=1)
else:
    budget_input = st.sidebar.number_input("Budget Maksimum (Euro)", value=800, step=50, min_value=1)

# Convert helper text
budget_eur = get_budget_in_euro(budget_input, currency)
if currency == 'IDR':
    usd_val = budget_input / RATES['USD_TO_IDR']
    st.sidebar.markdown(f"<small style='color:#8e9aaf;'>Setara dengan: **€ {budget_eur:,.2f}** / **$ {usd_val:,.2f}**</small>", unsafe_allow_html=True)
elif currency == 'USD':
    idr_val = budget_input * RATES['USD_TO_IDR']
    st.sidebar.markdown(f"<small style='color:#8e9aaf;'>Setara dengan: **€ {budget_eur:,.2f}** / **Rp {idr_val:,.0f}**</small>", unsafe_allow_html=True)
else:
    idr_val = budget_input * RATES['EUR_TO_IDR']
    usd_val = budget_input * RATES['EUR_TO_USD']
    st.sidebar.markdown(f"<small style='color:#8e9aaf;'>Setara dengan: **Rp {idr_val:,.0f}** / **$ {usd_val:,.2f}**</small>", unsafe_allow_html=True)

# Selectbox parameters
ram_input = st.sidebar.selectbox("RAM Minimum", options=[2, 4, 8, 12, 16, 32], index=2) # default 8GB
storage_select = st.sidebar.selectbox("Penyimpanan", options=[("SSD (Direkomendasikan)", "ssd"), ("HDD / SSD (Bebas)", "any")], format_func=lambda x: x[0], index=0)[1]
weight_select = st.sidebar.selectbox("Portabilitas (Berat Laptop)", options=[("Bebas", "bebas"), ("Sedang (Maks 2.3 kg)", "sedang"), ("Sangat Ringan (Maks 1.6 kg)", "ringan")], format_func=lambda x: x[0], index=0)[1]
perf_select = st.sidebar.selectbox("Prioritas Performa Utama", options=[("Bebas", "bebas"), ("Cukup & Responsif (Menengah)", "sedang"), ("Performa Tinggi (Editing/Gaming)", "tinggi")], format_func=lambda x: x[0], index=0)[1]
battery_select = st.sidebar.selectbox("Prioritas Baterai", options=[("Bebas", "bebas"), ("Cukup (Baterai Sedang)", "sedang"), ("Sangat Awet (Prioritas Mobilitas)", "lama")], format_func=lambda x: x[0], index=0)[1]

# Primary Needs Checkboxes
st.sidebar.subheader("Kebutuhan Penggunaan")
needs = []
if st.sidebar.checkbox("Kuliah / Kerja", value=True):
    needs.append("kuliah")
if st.sidebar.checkbox("Programming", value=True):
    needs.append("programming")
if st.sidebar.checkbox("Video/Photo Edit", value=False):
    needs.append("editing")
if st.sidebar.checkbox("Gaming", value=False):
    needs.append("gaming")
if st.sidebar.checkbox("Desain Grafis", value=False):
    needs.append("desain")

prefs = {
    'budgetEur': budget_eur,
    'minRam': ram_input,
    'storagePref': storage_select,
    'weightPref': weight_select,
    'perfPref': perf_select,
    'batteryPref': battery_select,
    'needs': needs
}

# --- SEARCH BUTTON TRIGGER ---
search_clicked = st.sidebar.button("🔍 Cari Laptop Terbaik (PSO)", use_container_width=True)

# Initialize Session State to keep recommendations and PSO results
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "optimal_specs" not in st.session_state:
    st.session_state.optimal_specs = None
if "pso_history" not in st.session_state:
    st.session_state.pso_history = None

# --- WORKFLOW EXECUTION ---

# Create columns for Visualizer and Recommendations
col_left, col_right = st.columns([5, 6])

with col_left:
    st.subheader("🤖 Visualisasi Algoritma PSO")
    
    # Visualizer placeholder
    plot_placeholder = st.empty()
    stats_placeholder = st.empty()

    # Pre-render faint background dataset constellation points
    laptops_preprocessed = [preprocess_laptop(l) for l in laptops]
    bg_prices = [float(l['price']) for l in laptops_preprocessed]
    bg_perfs = [float(l['perfScore']) for l in laptops_preprocessed]

    # Helper function to plot
    def render_plot(particles=None, gbest=None, iteration=0, status="Idle"):
        # Setup dark theme style for matplotlib
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4.2))
        
        # Faint constellation points
        ax.scatter(bg_prices, bg_perfs, color='#00f2fe', alpha=0.04, s=5, label='Titik Dataset Laptop')
        
        # Plot particles
        if particles:
            p_prices = [p.position[0] for p in particles]
            p_perfs = [p.position[3] for p in particles]
            ax.scatter(p_prices, p_perfs, color='#00f2fe', alpha=0.8, s=15, label='Partikel Swarm (PSO)', edgecolors='none')
            
        # Plot GBest Solution
        if gbest:
            ax.scatter(gbest[0], gbest[3], color='#9d4edd', s=80, marker='+', linewidths=2.5, label='Global Best (GBest)')
            # Pulsating circle helper
            ax.scatter(gbest[0], gbest[3], color='#9d4edd', s=180, facecolors='none', edgecolors='#9d4edd', alpha=0.5, linewidths=1)

        # Style plot
        ax.set_xlim(150, 3000)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Harga Laptop (Euro)", fontsize=9, color="#8e9aaf")
        ax.set_ylabel("Performa Laptop (0 - 100)", fontsize=9, color="#8e9aaf")
        ax.grid(True, color=(1.0, 1.0, 1.0, 0.05), linestyle=':', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color((1.0, 1.0, 1.0, 0.25))
        ax.spines['bottom'].set_color((1.0, 1.0, 1.0, 0.25))
        ax.tick_params(axis='both', colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
        
        # Legend outside/below
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
        fig.tight_layout()
        
        plot_placeholder.pyplot(fig)
        plt.close(fig)

        # Update stats
        if gbest:
            stats_placeholder.markdown(
                f"**Iterasi**: {iteration}/80 | **Kecocokan Terbaik**: {gbest[3]:.1f}% | **Status**: `{status}`"
            )
        else:
            stats_placeholder.markdown(
                f"**Iterasi**: - | **Kecocokan Terbaik**: - | **Status**: `{status}`"
            )

    # Initial empty plot render
    if st.session_state.optimal_specs is None:
        render_plot(status="Idle")
    else:
        render_plot(gbest=st.session_state.optimal_specs, iteration=80, status="Selesai (Converged)")

# Trigger Search
if search_clicked:
    # 1. Reset state
    st.session_state.recommendations = None
    st.session_state.optimal_specs = None
    
    # 2. Run PSO Optimization
    pso = PSOManager(prefs, swarm_size=40)
    
    # Render starting plot
    render_plot(particles=pso.particles, gbest=pso.global_best_position, iteration=0, status="Swarming...")

    # Iterate through step updates with rendering (simulate requestAnimationFrame loop)
    while not pso.is_converged:
        pso.step()
        # Render every 2 iterations to speed up Python execution but keep animation
        if pso.iteration % 2 == 0 or pso.is_converged:
            render_plot(particles=pso.particles, gbest=pso.global_best_position, iteration=pso.iteration, status="Swarming...")
            time.sleep(0.02) # frame delay for smooth feel

    # Optimization finished
    st.session_state.optimal_specs = pso.global_best_position
    render_plot(gbest=pso.global_best_position, iteration=80, status="Selesai (Converged)")

    # 3. Match database items to optimal specs
    recs = get_recommendations(laptops, prefs, pso.global_best_position)
    st.session_state.recommendations = recs

# Display results inside Right column
with col_right:
    st.subheader("Hasil Rekomendasi Laptop")
    
    if st.session_state.recommendations is None:
        st.info("Masukkan preferensi Anda di sidebar dan tekan tombol **'Cari Laptop Terbaik (PSO)'** untuk memulai simulasi swarm.")
    else:
        recs = st.session_state.recommendations
        
        # Display up to top 12 highly recommended items
        top_recs = [r for r in recs if r['category'] in ["Sangat Direkomendasikan", "Direkomendasikan", "Cukup Cocok"]][:12]
        
        if not top_recs:
            st.warning("Tidak ada laptop yang cocok dengan kriteria RAM/Storage minimum Anda. Silakan naikkan budget atau turunkan preferensi minimum RAM di sidebar.")
        else:
            # Multi-select comparison bar in Streamlit
            st.markdown("##### 🔍 Perbandingan Spesifikasi")
            selected_for_compare = []
            
            # Show list of laptops inside grid/columns or clean scrollable cards
            for idx, item in enumerate(top_recs):
                l = item['laptop']
                
                # Setup custom cards using HTML + Streamlit checkbox
                badge_color_class = item['cssClass'] + "-badge"
                card_border_class = item['cssClass'] + "-card"
                formatted_price_str = format_price(l['price'], currency)
                
                card_html = f"""
                <div class="card {card_border_class}">
                    <span class="score-badge {badge_color_class}">{item['score']}% Match</span>
                    <div class="card-title">{l['company']} {l['product']}</div>
                    <div class="card-meta">{l['typeName']} | {l['opsys']}</div>
                    <div style="font-size:0.9rem; color:#f0f2f6; margin-bottom: 0.5rem;">
                        <b>Spesifikasi:</b> RAM {int(l['ram'])}GB | CPU {l['cpuCompany']} {l['cpuType']} ({l['cpuFreq']}GHz) | GPU {l['gpuType']} | Layar {l['inches']}" ({l['screenResolution'].split(' ')[-1]}) | Berat {l['weight']}kg | Storage {l['memory']}
                    </div>
                    <div style="margin-top: 0.3rem;">
                        <span class="price-tag">{formatted_price_str}</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Checkbox to let user add to comparison
                compare_check = st.checkbox(f"Pilih {l['company']} {l['product']} untuk perbandingan", key=f"comp_{idx}")
                if compare_check:
                    selected_for_compare.append(item)
                
                st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.15;' />", unsafe_allow_html=True)

            # Draw Comparison Table if items are selected
            if len(selected_for_compare) > 0:
                if len(selected_for_compare) > 3:
                    st.sidebar.error("Maksimal hanya dapat membandingkan 3 laptop secara bersamaan.")
                else:
                    st.markdown("---")
                    st.subheader("⚖️ Perbandingan Laptop Terpilih")
                    
                    # Create comparison matrix
                    headers = ["Spesifikasi"] + [f"{item['laptop']['company']} {item['laptop']['product']} ({item['score']}% Match)" for item in selected_for_compare]
                    
                    specs_rows = [
                        ("Harga", lambda l: format_price(l['price'], currency)),
                        ("Kategori", lambda l: l['typeName']),
                        ("Sistem Operasi", lambda l: l['opsys']),
                        ("Prosesor (CPU)", lambda l: f"{l['cpuCompany']} {l['cpuType']} ({l['cpuFreq']} GHz)"),
                        ("RAM", lambda l: f"{int(l['ram'])} GB"),
                        ("Kartu Grafis (GPU)", lambda l: f"{l['gpuCompany']} {l['gpuType']}"),
                        ("Penyimpanan", lambda l: l['memory']),
                        ("Layar", lambda l: f"{l['inches']}\" ({l['screenResolution']})"),
                        ("Berat", lambda l: f"{l['weight']} kg"),
                        ("Skor Performa Fuzzy", lambda l: f"{round(l['perfScore'])} / 100"),
                        ("Skor Baterai Fuzzy", lambda l: f"{round(l['batteryScore'])} / 100")
                    ]
                    
                    comp_data = []
                    for label, extractor in specs_rows:
                        row = [label]
                        for item in selected_for_compare:
                            row.append(extractor(item['laptop']))
                        comp_data.append(row)
                    
                    # Display Table
                    st.table(np.array(comp_data))
