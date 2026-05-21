"""
SmartMatch Fuzzy Logic Engine (Python Version)
"""

def trimf(x, a, b, c):
    """Triangular Membership Function"""
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a)
    if b < x < c:
        return (c - x) / (c - b)
    return 0.0

def trapmf(x, a, b, c, d):
    """Trapezoidal Membership Function"""
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if a < x < b:
        return (x - a) / (b - a)
    if c < x < d:
        return (d - x) / (d - c)
    return 0.0

def estimate_performance_score(laptop):
    """Estimates the performance score of a laptop (0 to 100) based on specs."""
    # 1. RAM component (max 100)
    ram = float(laptop.get('ram', 0))
    if ram <= 2:
        ram_score = 10
    elif ram <= 4:
        ram_score = 30
    elif ram <= 6:
        ram_score = 45
    elif ram <= 8:
        ram_score = 65
    elif ram <= 12:
        ram_score = 80
    elif ram <= 16:
        ram_score = 90
    elif ram <= 24:
        ram_score = 95
    else:
        ram_score = 100

    # 2. CPU component (max 100)
    cpu_score = 30.0
    cpu_company = str(laptop.get('cpuCompany', '')).lower()
    cpu_type = str(laptop.get('cpuType', '')).lower()
    cpu_freq = float(laptop.get('cpuFreq', 0.0))

    if "intel" in cpu_company:
        if "core i7" in cpu_type or "xeon" in cpu_type:
            cpu_score = 90.0
        elif "core i5" in cpu_type:
            cpu_score = 70.0
        elif "core i3" in cpu_type:
            cpu_score = 50.0
        elif any(x in cpu_type for x in ["pentium", "celeron", "atom", "core m"]):
            cpu_score = 30.0
    elif "amd" in cpu_company:
        if any(x in cpu_type for x in ["ryzen 7", "fx", "ryzen 1700"]):
            cpu_score = 90.0
        elif any(x in cpu_type for x in ["ryzen 5", "a12", "a10"]):
            cpu_score = 70.0
        elif any(x in cpu_type for x in ["ryzen 3", "a9", "a8", "a6"]):
            cpu_score = 50.0
        elif any(x in cpu_type for x in ["e-series", "e2", "athlon"]):
            cpu_score = 35.0

    if cpu_freq > 0:
        cpu_score = cpu_score * (cpu_freq / 2.5)
    cpu_score = min(100.0, max(10.0, cpu_score))

    # 3. GPU component (max 100)
    gpu_score = 25.0
    gpu_type = str(laptop.get('gpuType', '')).lower()
    gpu_company = str(laptop.get('gpuCompany', '')).lower()

    if "nvidia" in gpu_company:
        if any(x in gpu_type for x in ["gtx 1080", "gtx 1070", "gtx 1060", "quadro m"]):
            gpu_score = 100.0
        elif any(x in gpu_type for x in ["gtx 1050", "mx150", "gtx 9"]):
            gpu_score = 80.0
        elif any(x in gpu_type for x in ["940mx", "930mx", "920mx", "geforce 9"]):
            gpu_score = 50.0
        else:
            gpu_score = 40.0
    elif "amd" in gpu_company:
        if any(x in gpu_type for x in ["rx 580", "rx 570", "firepro"]):
            gpu_score = 95.0
        elif any(x in gpu_type for x in ["rx 560", "rx 550", "radeon 530"]):
            gpu_score = 75.0
        elif any(x in gpu_type for x in ["r7", "r5", "r4", "r2"]):
            gpu_score = 45.0
        else:
            gpu_score = 35.0
    else: # Intel Integrated
        if "iris" in gpu_type:
            gpu_score = 40.0
        else:
            gpu_score = 25.0

    return 0.3 * ram_score + 0.4 * cpu_score + 0.3 * gpu_score

def estimate_battery_score(laptop):
    """Estimates battery life score (0 to 100) based on form factor, weight, and screen size."""
    score = 65.0
    type_name = str(laptop.get('typeName', '')).lower()
    weight = float(laptop.get('weight', 0.0))
    inches = float(laptop.get('inches', 0.0))

    if "ultrabook" in type_name or "netbook" in type_name:
        score = 90.0
    elif "2 in 1 convertible" in type_name:
        score = 80.0
    elif "gaming" in type_name or "workstation" in type_name:
        score = 35.0

    if weight <= 1.2:
        score += 10.0
    elif weight >= 2.8:
        score -= 15.0
    elif weight >= 2.0:
        score -= 5.0

    if inches <= 12.5:
        score += 5.0
    elif inches >= 17.0:
        score -= 10.0

    return min(100.0, max(10.0, score))

def preprocess_laptop(laptop):
    """Preprocesses a laptop item, enriching it with synthesized fuzzy variables."""
    if laptop.get('_preprocessed'):
        return laptop

    enriched = dict(laptop)
    enriched['perfScore'] = estimate_performance_score(laptop)
    enriched['batteryScore'] = estimate_battery_score(laptop)
    enriched['_preprocessed'] = True
    return enriched

def get_fuzzy_memberships(laptop):
    """Evaluates fuzzy membership values for a preprocessed laptop."""
    price = float(laptop.get('price', 0.0))
    weight = float(laptop.get('weight', 0.0))
    perf = float(laptop.get('perfScore', 0.0))
    battery = float(laptop.get('batteryScore', 0.0))

    return {
        'price': {
            'murah': trapmf(price, 0, 0, 400, 750),
            'sedang': trimf(price, 500, 1000, 1500),
            'mahal': trapmf(price, 1250, 1800, 100000, 100000)
        },
        'weight': {
            'ringan': trapmf(weight, 0, 0, 1.2, 1.6),
            'sedang': trimf(weight, 1.4, 2.0, 2.6),
            'berat': trapmf(weight, 2.3, 3.0, 100, 100)
        },
        'performance': {
            'rendah': trapmf(perf, 0, 0, 25, 45),
            'sedang': trimf(perf, 35, 55, 75),
            'tinggi': trapmf(perf, 65, 80, 100, 100)
        },
        'battery': {
            'singkat': trapmf(battery, 0, 0, 30, 50),
            'sedang': trimf(battery, 40, 65, 80),
            'lama': trapmf(battery, 70, 85, 100, 100)
        }
    }

def evaluate_laptop_suitability(laptop, prefs):
    """Evaluates the suitability score (0-100) and explanations of a laptop based on user preferences."""
    l = preprocess_laptop(laptop)
    m = get_fuzzy_memberships(l)

    # 1. Budget Suitability
    budget_eur = prefs['budgetEur']
    price = float(l['price'])
    if price <= budget_eur:
        budget_match = 1.0
    else:
        over_percent = (price - budget_eur) / budget_eur
        budget_match = max(0.0, 1.0 - (over_percent / 0.3)) # 30% tolerance margin

    # 2. RAM Suitability
    min_ram = prefs['minRam']
    ram = float(l['ram'])
    if ram >= min_ram:
        ram_match = 1.0
    else:
        ram_match = ram / min_ram

    # 3. Storage Match (SSD / HDD preference)
    storage_pref = prefs['storagePref']
    memory_lower = str(l.get('memory', '')).lower()
    if storage_pref == 'ssd' and 'ssd' not in memory_lower and 'flash' not in memory_lower:
        storage_match = 0.5
    else:
        storage_match = 1.0

    # 4. Weight Match
    weight_pref = prefs['weightPref']
    if weight_pref == 'ringan':
        weight_match = m['weight']['ringan'] + 0.5 * m['weight']['sedang']
    elif weight_pref == 'sedang':
        weight_match = m['weight']['ringan'] + m['weight']['sedang']
    else:
        weight_match = 1.0
    weight_match = min(1.0, weight_match)

    # 5. Performance Match
    perf_pref = prefs['perfPref']
    if perf_pref == 'tinggi':
        perf_match = m['performance']['tinggi']
    elif perf_pref == 'sedang':
        perf_match = m['performance']['sedang'] + m['performance']['tinggi']
    else:
        perf_match = 1.0
    perf_match = min(1.0, perf_match)

    # 6. Battery Match
    battery_pref = prefs['batteryPref']
    if battery_pref == 'lama':
        battery_match = m['battery']['lama']
    elif battery_pref == 'sedang':
        battery_match = m['battery']['sedang'] + m['battery']['lama']
    else:
        battery_match = 1.0
    battery_match = min(1.0, battery_match)

    # 7. Needs-based rule matching (Fuzzy logic rules)
    needs_score = 0.0
    active_needs_count = 0
    needs_explanations = []

    if 'kuliah' in prefs['needs']:
        rule_val = min(
            max(m['price']['murah'], m['price']['sedang']),
            max(m['weight']['ringan'], m['weight']['sedang']),
            max(m['battery']['sedang'], m['battery']['lama'])
        )
        needs_score += rule_val
        active_needs_count += 1
        if rule_val > 0.6:
            needs_explanations.append("Sangat cocok untuk Kuliah (ringan, baterai baik, harga terjangkau).")

    if 'programming' in prefs['needs']:
        ram_ok = 1.0 if ram >= 8 else (0.5 if ram >= 4 else 0.0)
        rule_val = min(
            max(m['performance']['sedang'], m['performance']['tinggi']),
            ram_ok,
            max(m['price']['sedang'], m['price']['mahal'])
        )
        needs_score += rule_val
        active_needs_count += 1
        if rule_val > 0.6:
            needs_explanations.append("Sangat menunjang Programming (performa & kapasitas RAM mumpuni).")

    if 'editing' in prefs['needs']:
        screen_res_lower = str(l.get('screenResolution', '')).lower()
        is_ips_or_4k = 1.0 if 'ips' in screen_res_lower or '4k' in screen_res_lower or 'ips' in memory_lower or '4k' in memory_lower else 0.6
        rule_val = min(
            m['performance']['tinggi'],
            1.0 if ram >= 16 else (0.7 if ram >= 8 else 0.3),
            is_ips_or_4k
        )
        needs_score += rule_val
        active_needs_count += 1
        if rule_val > 0.6:
            needs_explanations.append("Cocok untuk Video/Photo Editing (performa tinggi & layar berkualitas).")

    if 'gaming' in prefs['needs']:
        gpu_company_lower = str(l.get('gpuCompany', '')).lower()
        gpu_type_lower = str(l.get('gpuType', '')).lower()
        is_dedicated_gpu = "nvidia" in gpu_company_lower or ("amd" in gpu_company_lower and "r2" not in gpu_type_lower and "r4" not in gpu_type_lower)
        rule_val = min(
            m['performance']['tinggi'],
            1.0 if is_dedicated_gpu else 0.2,
            1.0 if ram >= 8 else 0.4
        )
        needs_score += rule_val
        active_needs_count += 1
        if rule_val > 0.6:
            needs_explanations.append("Performa Gaming tinggi dengan kartu grafis dedicated.")

    if 'desain' in prefs['needs']:
        screen_res_lower = str(l.get('screenResolution', '')).lower()
        is_high_res = any(x in screen_res_lower for x in ['1920x', '2560x', '3840x', 'ips'])
        rule_val = min(
            max(m['performance']['sedang'], m['performance']['tinggi']),
            1.0 if ram >= 8 else 0.5,
            1.0 if is_high_res else 0.5
        )
        needs_score += rule_val
        active_needs_count += 1
        if rule_val > 0.6:
            needs_explanations.append("Cocok untuk Desain Grafis (layar tajam & reproduksi warna baik).")

    need_match = needs_score / active_needs_count if active_needs_count > 0 else 1.0

    # Defuzzification
    raw_match_val = (
        budget_match * 0.25 +
        ram_match * 0.15 +
        storage_match * 0.10 +
        weight_match * 0.15 +
        perf_match * 0.15 +
        battery_match * 0.10 +
        need_match * 0.10
    )
    score = round(raw_match_val * 100)

    # Explanations
    reasons = []
    if budget_match == 1.0:
        reasons.append("Harga sepenuhnya masuk budget.")
    elif budget_match > 0.5:
        reasons.append("Sedikit di atas budget Anda, namun masih masuk batas toleransi.")
    else:
        reasons.append("Melebihi budget cukup signifikan.")

    if ram >= min_ram:
        reasons.append(f"Kapasitas RAM {int(ram)}GB memenuhi kebutuhan.")
    else:
        reasons.append(f"RAM {int(ram)}GB berada di bawah preferensi Anda.")

    if weight_pref == 'ringan' and m['weight']['ringan'] > 0.7:
        reasons.append("Sangat ringan dan mudah dibawa bepergian.")
    if battery_pref == 'lama' and m['battery']['lama'] > 0.7:
        reasons.append("Ketahanan baterai sangat awet.")

    reasons.extend(needs_explanations)

    category = "Tidak Direkomendasikan"
    css_class = "not-rec"
    if score >= 80:
        category = "Sangat Direkomendasikan"
        css_class = "highly-rec"
    elif score >= 60:
        category = "Direkomendasikan"
        css_class = "rec"
    elif score >= 40:
        category = "Cukup Cocok"
        css_class = "fairly-rec"

    return {
        'score': score,
        'category': category,
        'cssClass': css_class,
        'reasons': reasons[:3],
        'perfScore': round(l['perfScore']),
        'batteryScore': round(l['batteryScore'])
    }
