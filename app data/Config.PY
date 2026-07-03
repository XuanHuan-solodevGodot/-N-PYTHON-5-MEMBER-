# =====================================
# THEME / COLORS
# =====================================

COLOR_BG = "#F7F1E8"          # cream background
COLOR_HEADER = "#5C1A2B"      # deep wine red
COLOR_HEADER_TEXT = "#F7F1E8"
COLOR_ACCENT = "#8C2F45"      # wine red accent
COLOR_GOLD = "#C9A227"        # gold accent
COLOR_CARD = "#FFFFFF"
COLOR_TEXT = "#3B2A2F"
COLOR_MUTED = "#7A6A6E"
COLOR_SUCCESS = "#3E7A4E"
COLOR_ROW_ALT = "#F1E6DC"

CLASS_COLORS = {
    1: "#8C2F45",
    2: "#C9A227",
    3: "#4B3A6B",
}

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_SECTION = ("Segoe UI", 15, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_LABEL_BOLD = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_RESULT = ("Segoe UI", 14, "bold")
FONT_STAT_NUM = ("Segoe UI", 22, "bold")
FONT_STAT_LABEL = ("Segoe UI", 10)

# =====================================
# DATA
# =====================================

FEATURE_COLUMNS = [
    "alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
    "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue", "od280_od315", "proline",
]

# (label shown in the form, placeholder/example text)
FIELDS = [
    ("Alcohol", "vd: 13.2"),
    ("Malic Acid", "vd: 1.78"),
    ("Ash", "vd: 2.14"),
    ("Alcalinity of Ash", "vd: 11.2"),
    ("Magnesium", "vd: 100"),
    ("Total Phenols", "vd: 2.65"),
    ("Flavanoids", "vd: 2.76"),
    ("Nonflavanoid Phenols", "vd: 0.26"),
    ("Proanthocyanins", "vd: 1.28"),
    ("Color Intensity", "vd: 4.38"),
    ("Hue", "vd: 1.05"),
    ("OD280/OD315", "vd: 3.40"),
    ("Proline", "vd: 1050"),
]