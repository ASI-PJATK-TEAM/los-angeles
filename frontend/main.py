import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests
from datetime import date

GEOJSON_URL = (
    "https://services5.arcgis.com/7nsPwEMP38bSkCjy/ArcGIS/rest/services/"
    "LAPD_Division/FeatureServer/0/query?where=1=1&outFields=*"
    "&outSR=4326&f=geojson"
)
FASTAPI_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="LA Crime-Risk Map", layout="wide")
st.title("📍 Los Angeles – interactive crime-risk map")


@st.cache_data(show_spinner=False)
def load_divisions():
    gdf = gpd.read_file(GEOJSON_URL)
    gdf = gdf[["AREA", "geometry"]]
    return gdf

divisions = load_divisions()

if "risk_colors" not in st.session_state:
    st.session_state.risk_colors = {}

picked_date: date = st.sidebar.date_input(
    "Choose date for risk estimation", value=date.today(), format="YYYY-MM-DD"
)

st.sidebar.markdown(
    "Click on any division polygon to fetch its risk score "
    "and see the colour update."
)

# TODO: update to check from returned value
def bucket_to_colour(score: float) -> tuple[str, str]:
    if score <= LOW_THR:
        return "Low", "#24a148"
    elif score <= MED_THR:
        return "Medium", "#ffbe2e"
    return "High", "#fa4d56"



m = folium.Map(location=[34.05, -118.25], zoom_start=10,
               tiles="cartodbpositron")

for _, row in divisions.iterrows():
    division = row["AREA"]
    fill_col = st.session_state.risk_colors.get(division, "#88888820")  # default transparent

    folium.GeoJson(
        row["geometry"],
        name=division,
        style_function=lambda _, col=fill_col: dict(
            color="#444444", weight=1.2,
            fillColor=col, fillOpacity=0.5
        ),
        highlight_function=lambda _: dict(weight=3, color="#000000"),
        tooltip=division
    ).add_to(m)

click_data = st_folium(m, width=950, height=600, returned_objects=[])


if click_data and click_data.get("last_active_drawing"):
    props = click_data["last_active_drawing"]["properties"]
    clicked_division = props.get("name") or props.get("DIVISION")

    if clicked_division:
        payload = {"area": clicked_division, "date": picked_date.isoformat()}
        try:
            r = requests.post(FASTAPI_URL, json=payload, timeout=10)
            r.raise_for_status()
            score = r.json()["predicted_crime_score"]
            bucket, colour = bucket_to_colour(score)


            st.session_state.risk_colors[clicked_division] = colour
            st.toast(f"{clicked_division}: {bucket} risk ({score:.1f})", icon="✅")
            st.experimental_rerun()

        except Exception as exc:
            st.error(f"API call failed: {exc}")

with st.sidebar:
    st.subheader("Legend (current map)")
    for div, col in st.session_state.risk_colors.items():
        st.markdown(
            f'<div style="display:flex;align-items:center">'
            f'<div style="width:18px;height:18px;background:{col};'
            f'margin-right:6px;border:1px solid #000;"></div>{div}'
            f'</div>',
            unsafe_allow_html=True
        )