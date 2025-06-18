import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests
from datetime import date
from shapely.geometry import Point

GEOJSON_URL = (
    "https://services5.arcgis.com/7nsPwEMP38bSkCjy/ArcGIS/rest/services/"
    "LAPD_Division/FeatureServer/0/query?where=1=1&outFields=*"
    "&outSR=4326&f=geojson"
)
FASTAPI_URL = "http://localhost:8000/predict"

LOW_THR = 300
MED_THR = 500

AREA_NAME_MAPPING = {
    "892878007.932": "Harbor",
    "699582609.226": "Mission",
    "1346816369.83": "Devonshire",
    "1297384550.74": "Foothill",
    "909032643.829": "Topanga",
    "936405735.233": "West Valley",
    "634601058.555": "North Hollywood",
    "489694990.173": "Van Nuys",
    "815602204.078": "Northeast",
    "371835298.23": "Hollywood",
    "1803658584.49": "West Los Angeles",
    "433032348.802": "Hollenbeck",
    "154395388.114": "Rampart",
    "327067076.835": "Wilshire",
    "174418477.13": "Olympic",
    "343325464.492": "Southwest",
    "272376013.411": "Newton",
    "717612851.136": "Pacific",
    "315958991.988": "77th Street",
    "261139061.954": "Southeast",
    "136747749.664": "Central",
}

st.set_page_config(page_title="LA Crime‑Risk Map", layout="wide")
st.title("📍 Los Angeles – interaktywna mapa ryzyka przestępczości")

@st.cache_data(show_spinner=False)
def load_divisions():
    try:
        gdf = gpd.read_file(GEOJSON_URL)
        gdf["AREA"] = gdf["AREA"].astype(str)
        gdf["NAME"] = gdf["AREA"].map(AREA_NAME_MAPPING).fillna("Nieznana dzielnica")
        return gdf[["AREA", "NAME", "geometry"]]
    except Exception as e:
        st.error(f"Błąd podczas ładowania danych: {e}")
        return None

divisions = load_divisions()
if divisions is None:
    st.stop()

if "selected_area" not in st.session_state:
    st.session_state.selected_area = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

picked_date = st.sidebar.date_input(
    "Wybierz datę do analizy ryzyka",
    value=date.today(),
    format="YYYY-MM-DD"
)

st.sidebar.markdown(
    "**Instrukcja:**\n"
    "1. Wybierz datę powyżej\n"
    "2. Kliknij na dzielnicę na mapie\n"
    "3. Kliknij przycisk 'Analizuj ryzyko'"
)

def bucket_to_colour(score: float) -> tuple[str, str]:
    if score <= LOW_THR:
        return "Niskie", "#24a148"
    elif score <= MED_THR:
        return "Średnie", "#ffbe2e"
    return "Wysokie", "#fa4d56"

def get_risk_description(risk_level: str) -> str:
    desc = {
        "Niskie": "Prawdopodobieństwo wystąpienia przestępstwa jest relatywnie małe.",
        "Średnie": "Umiarkowane prawdopodobieństwo wystąpienia przestępstwa.",
        "Wysokie": "Podwyższone ryzyko wystąpienia przestępstwa."
    }
    return desc.get(risk_level, "")

m = folium.Map(
    location=[34.05, -118.25],
    zoom_start=10,
    tiles="cartodbpositron",
    zoom_control=False,
    scrollWheelZoom=False,
    dragging=False,
    min_zoom=10,
    max_zoom=10
)

for _, row in divisions.iterrows():
    area_id = row["AREA"]
    name = row["NAME"]
    is_selected = st.session_state.selected_area == area_id
    style_fill = "#28a745" if is_selected else "#cccccc"
    style_op = 0.8 if is_selected else 0.4
    style_w = 3 if is_selected else 1

    feature = {
        "type": "Feature",
        "properties": {"AREA": area_id, "NAME": name},
        "geometry": row["geometry"].__geo_interface__
    }

    folium.GeoJson(
        feature,
        name=name,
        style_function=lambda feat, col=style_fill, op=style_op, w=style_w: {
            "color": "#333",
            "weight": w,
            "fillColor": col,
            "fillOpacity": op
        },
        highlight_function=lambda feat: {"weight": 4, "color": "#000", "fillOpacity": 0.9},
        tooltip=folium.Tooltip(f"<b>{name}</b>", sticky=True),
    ).add_to(m)

map_data = st_folium(
    m,
    width=950,
    height=600,
    returned_objects=["last_object_clicked", "last_clicked"],
    key="crime_map"
)

clicked_area = None
if map_data and map_data.get("last_object_clicked"):
    obj = map_data["last_object_clicked"]
    if isinstance(obj, dict) and "lat" in obj:
        pt = Point(obj["lng"], obj["lat"])
        for _, row in divisions.iterrows():
            if row["geometry"].contains(pt):
                clicked_area = row["AREA"]
                break
    elif isinstance(obj, dict) and "properties" in obj:
        clicked_area = obj["properties"].get("AREA")

if clicked_area and clicked_area != st.session_state.selected_area:
    st.session_state.selected_area = clicked_area
    st.session_state.analysis_results = None
    st.rerun()


col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("🔍 Analiza ryzyka")
    name_to_area = {v: k for k, v in AREA_NAME_MAPPING.items()}
    area_names = [""] + list(name_to_area.keys())
    current_name = AREA_NAME_MAPPING.get(st.session_state.selected_area, "") if st.session_state.selected_area else ""

    sel = st.selectbox("Lub wybierz dzielnicę:", options=area_names,
                       index=area_names.index(current_name) if current_name in area_names else 0)

    if sel and sel != current_name:
        st.session_state.selected_area = name_to_area[sel]
        st.session_state.analysis_results = None
        st.rerun()


    if st.session_state.selected_area:
        st.success(f"✅ Wybrana dzielnica: **{AREA_NAME_MAPPING.get(st.session_state.selected_area)}**")
        st.write(f"📅 Data: **{picked_date}**")
    else:
        st.info("👆 Wybierz dzielnicę")

    if st.button("🔍 Analizuj ryzyko", disabled=not st.session_state.selected_area):
        payload = {"area": st.session_state.selected_area, "date": picked_date.isoformat()}
        try:
            r = requests.post(FASTAPI_URL, json=payload, timeout=10)
            r.raise_for_status()
            res = r.json()
            score = res["predicted_crime_score"]
            lvl, col = bucket_to_colour(score)
            st.session_state.analysis_results = {"score": score, "level": lvl, "color": col}
            st.success("Analiza zakończona!")
        except Exception as e:
            st.error(f"Błąd: {e}")

with col2:
    st.subheader("Legenda")
    st.markdown(
        '<div style="display:flex;align-items:center;margin-bottom:10px">'
        '<div style="width:20px;height:20px;background:#28a745;margin-right:8px;border:1px solid #000;"></div>'
        '<span>Wybrana dzielnica</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;align-items:center;margin-bottom:10px">'
        '<div style="width:20px;height:20px;background:#cccccc;margin-right:8px;border:1px solid #000;"></div>'
        '<span>Inne dzielnice</span></div>', unsafe_allow_html=True)

if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.markdown("---")
    st.subheader("📊 Wyniki analizy ryzyka")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Dzielnica", AREA_NAME_MAPPING.get(st.session_state.selected_area))
    with c2: st.metric("Poziom ryzyka", res["level"])
    with c3: st.metric("Wynik", f"{res['score']:.1f}")
    st.markdown(
        f'<div style="background:{res["color"]};color:white;padding:15px;border-radius:5px;text-align:center;margin:20px 0">'
        f'<strong>Ryzyko: {res["level"]}</strong><br>{get_risk_description(res["level"])}</div>',
        unsafe_allow_html=True
    )

    with st.expander("ℹ️ Szczegóły"):
        st.write(f"**Wynik numeryczny:** {res['score']:.2f}")
        st.write(f"- Niskie: ≤ {LOW_THR}")
        st.write(f"- Średnie: {LOW_THR+1}-{MED_THR}")
        st.write(f"- Wysokie: > {MED_THR}")
