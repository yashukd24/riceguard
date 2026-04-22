from utils.config import SEVERITY_MILD, SEVERITY_MODERATE


def estimate_severity(affected_area: float) -> str:
    if affected_area < SEVERITY_MILD:
        return "Mild"
    if affected_area < SEVERITY_MODERATE:
        return "Moderate"
    return "Severe"


ADVISORY_DB = {
    "Bacterial_Blight": {
        "description": "Caused by Xanthomonas oryzae pv. oryzae. Water-soaked lesions on leaf edges turn yellowish-white. One of the most destructive rice diseases worldwide.",
        "Mild": {
            "action": "Monitor closely. Remove infected leaves. Ensure proper field drainage.",
            "chemicals": ["Copper oxychloride 50% WP @ 2.5 g/L", "Copper-based bactericide (preventive)"],
            "cultural": ["Avoid over-irrigation", "Use disease-free certified seeds", "Maintain proper plant spacing"],
        },
        "Moderate": {
            "action": "Apply bactericide immediately. Drain flooded fields. Reduce nitrogen fertilizer.",
            "chemicals": ["Streptomycin sulphate + Tetracycline (100 ppm)", "Copper hydroxide 53.8% DF @ 2 g/L"],
            "cultural": ["Avoid clipping seedling tips", "Use resistant varieties (IR-64, Swarna Sub1)", "Reduce nitrogen application"],
        },
        "Severe": {
            "action": "Immediate intervention. Isolate infected areas. Apply bactericide twice at 10-day intervals.",
            "chemicals": ["Streptomycin sulphate + Tetracycline (200 ppm)", "Bismerthiazol 20% WP @ 1 g/L", "Kasugamycin 3% SL @ 2 mL/L"],
            "cultural": ["Remove and burn heavily infected plants", "Do not reuse irrigation water from infected fields", "Apply balanced potassium fertilizer"],
        },
    },
    "Blast": {
        "description": "Caused by Magnaporthe oryzae (fungal). Diamond-shaped grey lesions with brown borders on leaves. Can cause 100% crop loss in severe outbreaks.",
        "Mild": {
            "action": "Apply preventive fungicide. Avoid excessive nitrogen. Monitor weather - blast spreads in cool, humid conditions.",
            "chemicals": ["Tricyclazole 75% WP @ 0.6 g/L", "Carbendazim 50% WP @ 1 g/L"],
            "cultural": ["Use blast-resistant varieties (Pusa Basmati 1121)", "Avoid waterlogging", "Apply silicon fertilizer"],
        },
        "Moderate": {
            "action": "Apply systemic fungicide immediately. Repeat after 7 days if conditions remain humid.",
            "chemicals": ["Tricyclazole 75% WP @ 0.6 g/L", "Isoprothiolane 40% EC @ 1.5 mL/L", "Propiconazole 25% EC @ 1 mL/L"],
            "cultural": ["Split nitrogen doses", "Alternate wetting and drying", "Avoid late sowing"],
        },
        "Severe": {
            "action": "Emergency fungicide at 5-7 day intervals. Increase potassium and silica. Evaluate field abandonment if neck blast detected.",
            "chemicals": ["Tricyclazole 75% WP @ 0.6 g/L (twice)", "Azoxystrobin 23% SC @ 1 mL/L", "Tebuconazole 25.9% EC @ 1 mL/L"],
            "cultural": ["Remove and burn infected panicles", "Avoid overhead irrigation", "Apply potassium silicate"],
        },
    },
    "Brown_Spot": {
        "description": "Caused by Bipolaris oryzae (fungal). Oval brown lesions with yellow halo. Often linked to nutrient deficiency (K, Si).",
        "Mild": {
            "action": "Correct soil nutrient deficiencies. Apply potassium. Use protective fungicide if spreading.",
            "chemicals": ["Mancozeb 75% WP @ 2.5 g/L", "Iprodione 50% WP @ 1 g/L"],
            "cultural": ["Apply K2O @ 40 kg/ha", "Improve soil fertility with organic manure", "Use disease-free seeds"],
        },
        "Moderate": {
            "action": "Apply systemic fungicide. Address soil nutrition. Inspect for concurrent stress.",
            "chemicals": ["Propiconazole 25% EC @ 1 mL/L", "Thiophanate-methyl 70% WP @ 1.5 g/L"],
            "cultural": ["Seed treatment with Thiram @ 2 g/kg", "Balanced NPK application", "Improve drainage"],
        },
        "Severe": {
            "action": "Apply systemic fungicide twice at 10-day intervals. Conduct soil testing urgently.",
            "chemicals": ["Propiconazole 25% EC @ 1 mL/L (twice)", "Carbendazim + Mancozeb @ 2 g/L", "Hexaconazole 5% EC @ 1 mL/L"],
            "cultural": ["Foliar potassium spray (0.5% KCl)", "Use certified biofungicide-treated seeds", "Consult agronomist for soil amendment"],
        },
    },
    "Tungro": {
        "description": "Caused by two viruses (RTBV + RTSV) transmitted by green leafhopper (Nephotettix virescens). Yellow-orange discoloration, stunted growth. No chemical cure - vector control is key.",
        "Mild": {
            "action": "Control leafhopper vectors immediately. Remove infected plants to prevent virus spread.",
            "chemicals": ["Imidacloprid 17.8% SL @ 0.3 mL/L", "Thiamethoxam 25% WG @ 0.3 g/L"],
            "cultural": ["Use tungro-resistant varieties", "Synchronize planting with neighbors", "Avoid planting near infected fields"],
        },
        "Moderate": {
            "action": "Intensify leafhopper control. Uproot and destroy infected plants.",
            "chemicals": ["Imidacloprid 17.8% SL @ 0.5 mL/L", "Buprofezin 25% WP @ 1 g/L"],
            "cultural": ["Maintain field hygiene", "Flood fields briefly to reduce leafhopper population", "Consult agricultural department"],
        },
        "Severe": {
            "action": "Declare field under disease alert. Uproot and burn all infected plants. Apply leafhopper sprays every 5 days.",
            "chemicals": ["Imidacloprid 17.8% SL @ 0.5 mL/L (every 5 days)", "Deltamethrin 2.8% EC @ 1 mL/L"],
            "cultural": ["Flood field to 5 cm for 3-4 days", "Burn all crop debris after harvest", "Contact district agricultural officer", "Plan resistant varieties for next season"],
        },
    },
}


def get_advisory(disease: str, severity: str) -> dict:
    if disease not in ADVISORY_DB or severity not in ["Mild", "Moderate", "Severe"]:
        return {"error": "Invalid disease or severity"}

    db = ADVISORY_DB[disease]
    severity_data = db[severity]
    return {
        "disease": disease.replace("_", " "),
        "severity": severity,
        "description": db["description"],
        "action": severity_data["action"],
        "chemicals": severity_data["chemicals"],
        "cultural": severity_data["cultural"],
    }
