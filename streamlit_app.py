import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
#st.set_page_config(layout="wide")
st.markdown('<i style="color:red;">Toto je pracovní verze.</i>', unsafe_allow_html=True)
st.markdown('<i style="color:red;">Data s vyjímkou budoucího růstu pochází z oec.world.</i>', unsafe_allow_html=True)
st.markdown('<i style="color:red;">Projekce 2025-30 berte s velikou rezervou.</i>', unsafe_allow_html=True)
st.title("Mapa Příležitostí")

# Sidebar for selecting variables
st.sidebar.header("Nastavení Grafu")

USD_to_czk = st.sidebar.number_input("Kurz USD vůči CZK",value=22.5)
color_discrete_map = {
    'A02. Doprava': '#d6568c',
    'A03. Budovy': '#274001',
    'A04. Výroba nízkoemisní elektřiny a paliv': '#f29f05',
    'A05. Ukládání energie': '#f25c05',
    'A06. Energetické sítě': '#828a00',
    'E01. Měřící a diagnostické přístroje; Monitoring': '#4d8584',
    'A01. Výroba, nízkoemisní výrobní postupy': '#a62f03',
    'B02. Cirkularita a odpady': '#400d01',

    'A02c. Cyklistika a jednostopá': '#808080',
    'A03a. Snižování energetické náročnosti budov': '#94FFB5',
    'A04f. Jádro': '#8F7C00',
    'A05b. Vodik a čpavek': '#9DCC00',
    'A06a. Distribuce a přenos elektřiny': '#C20088',
    'A04a. Větrná': '#003380',
    'E0f. Měření v energetice a síťových odvětvích (HS9028 - 9030, 903210)': '#FFA405',
    'E01c. Měření okolního prostředí (HS9025)': '#FFA8BB',
    'E01i. Ostatní': '#426600',
    'A02a. Železniční (osobní i nákladní)': '#FF0010',
    'E01h. Surveying / Zeměměřičství (HS 9015)': '#5EF1F2',
    'A01a. Nízkoemisní výroba': '#00998F',
    'A04g. Efektivní využití plynu a vodíku': '#E0FF66',
    'E01e. Chemická analýza (HS9027)': '#740AFF',
    'A04b. Solární': '#990000',
    'A03b. Elektrifikace tepelného hospodářství': '#FFFF80',
    'A05a. Baterie': '#FFE100',
    'E01d. Měření vlastností plynů a tekutnin (HS9026)': '#FF5005',
    'E01a. Optická měření (HS 9000 - 9013, HS 903140)': '#F0A0FF',
    'B02b. Cirkularita, využití odpadu': '#0075DC',
    'A05c. Ostatní ukládání': '#993F00',
    'A01c. Elektrifikace výrobních postupů': '#4C005C',
    'A03b. Elektrifikace domácností': '#191919',

    'Díly a vybavení': '#005C31',
    'Zateplení, izolace': '#2BCE48',
    'Komponenty pro jadernou energetiku': '#FFCC99',
    'Vodík (elektrolyzéry)': '#808080',
    'Transformační stanice a další síťové komponenty': '#94FFB5',
    'Komponenty pro větrnou energetiku': '#8F7C00',
    'Termostaty': '#9DCC00',
    'Termometry': '#C20088',
    'Ostatní': '#003380',
    'Nové lokomotivy a vozy': '#FFA405',
    'Surveying / Zeměměřičství': '#FFA8BB',
    'Nízkoemisní výroby ostatní': '#426600',
    'Komponenty pro výrobu energie z plynů': '#FF0010',
    'Spektrometry': '#5EF1F2',
    'Komponenty pro solární energetiku': '#00998F',
    'Tepelná čerpadla a HVAC': '#E0FF66',
    'Infrastruktura (nové tratě a elektrifikace stávajících)': '#740AFF',
    'Baterie': '#990000',
    'Měření odběru a výroby plynů, tekutin, elektřiny': '#FFFF80',
    'Komponenty pro vodní energetiku': '#FFE100',
    'Měření vlastností plynů a tekutin': '#FF5005',
    'Optická měření': '#F0A0FF',
    'Materiálové využití': '#0075DC',
    'Měření ionizujícího záření': '#993F00',
    'Ostatní ukládání (přečerpávací vodní, ohřátá voda,…)': '#4C005C',
    'Hydrometry': '#191919',
    'Elektrifikace ve výrobě': '#005C31',
    'Domácí elektrické spotřebiče': '#2BCE48',
    'Chromatografy': '#FFCC99',
    'Osciloskopy': '#808080',
}


# Load data
def load_data():
    # Replace with the path to your data file
    df                          = pd.read_csv('GreenComplexity_CZE_2022.csv')
    df                          = df[df.Included == "IN"]
    df['stejna velikost']       = 0.02
    df['CZ-EU Podíl 2022 %']      = 100 * df['CZ-EU Podíl 2022 %'] 
    df['EU Světový Podíl 2022 %'] = 100 * df['EU Světový Podíl 2022 %'] 
    df['CZ Světový Podíl 2022 %'] = 100 * df['CZ Světový Podíl 2022 %'] 
    df['CZ Export 2022 CZK']        = USD_to_czk*df['CZ Export 2022 CZK'] 
    #df['EU_Import_2022']        = USD_to_czk*df['EU_Import_2022'] 
    #df['CZ_Import_2022']        = USD_to_czk*df['CZ_Import_2022'] 
    df['Světový export 2022 CZK']      = USD_to_czk*df['Světový export 2022 CZK'] 
    df['EU Export 2022 CZK']        = USD_to_czk*df['EU Export 2022 CZK'] 
    #df['EU_Total_Export_25_30'] = USD_to_czk*df['EU_Total_Export_25_30'] 
    #df['CZ_Total_Export_25_30'] = USD_to_czk*df['CZ_Total_Export_25_30'] 
    #df['EU_2030_export']        = USD_to_czk*df['EU_2030_export'] 
    #df['CZ_2030_export']        = USD_to_czk*df['CZ_2030_export'] 
    df['HS_ID']                 = df['HS_ID'].astype(str)

    return df

df = load_data()

# Create lists of display names for the sidebar
ji_display_names = ['Skupina', 'Podskupina', 'Kategorie výrobku']
plot_display_names = [
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    #'EU Import 2022 CZK',
    #'CZ Import 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'ubiquity',
    'density',
    'cog',
    #'CZ 2030 Export CZK',
    #'CZ Celkový Export 25-30 CZK',
    #'EU 2030 Export CZK',
    #'EU Celkový Export 25-30 CZK',
    #'CAGR 2022-2030 Předpověď',
    'Stejná Velikost'
]

hover_display_data = [
    'HS_ID',
    'Produkt_HS6',
    'Název Produktu',
    #'Produkt_HS4',
    #'Produkt_HS2',
    #'CZ Celkový Export 25-30 CZK',
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'EU Největší Exportér 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    #'EU Import 2022 CZK',
    'CZ Import 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    #'CZ 2030 Export CZK',
    #'CZ Celkový Export 25-30 CZK',
    #'EU 2030 Export',
    #'EU Celkový Export 25-30 CZK',
    #'CAGR 2022-2030 Předpověď',
    'Zdroj',
    #'IS_REALCAGR'
]

# Sidebar selection boxes using display names
x_axis      = st.sidebar.selectbox("Vyber osu X:", plot_display_names, index=0)
y_axis      = st.sidebar.selectbox("Vyber osu Y:", plot_display_names, index=4)
markersize  = st.sidebar.selectbox("Velikost dle:", plot_display_names, index=5)
color       = st.sidebar.selectbox("Barva dle:", ji_display_names)
hover_info  = st.sidebar.multiselect("Co se zobrazí při najetí myší:", hover_display_data, default='Název Produktu')


# Sidebar for filtering the color variable
color_values    = df[color].unique()
selected_colors = st.sidebar.multiselect(f"Filtrovat dle: {color}", options=color_values, default=color_values)

# Filter section
if 'filters' not in st.session_state:
    st.session_state.filters = []

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Add a filter"):
        st.session_state.filters.append({'column': None, 'range': None})
with col2:
    if st.button("Clear filters"):
        st.session_state.filters = []

# Display existing filters using display names
for i, filter in enumerate(st.session_state.filters):
    filter_col= st.sidebar.selectbox(f"Filter {i+1} column", plot_display_names, key=f"filter_col_{i}")
    filter_min, filter_max = df[filter_col].min(), df[filter_col].max()
    filter_range = st.sidebar.slider(f"Filter {i+1} range", float(filter_min), float(filter_max), (float(filter_min), float(filter_max)), key=f"filter_range_{i}")
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply filters to dataframe
filtered_df = df.copy()

# Apply color filter
filtered_df = filtered_df[filtered_df[color].isin(selected_colors)]

# Apply numerical filters
for filter in st.session_state.filters:
    if filter['column'] is not None and filter['range'] is not None:
        filtered_df = filtered_df[
            (filtered_df[filter['column']] >= filter['range'][0]) &
            (filtered_df[filter['column']] <= filter['range'][1])
        ]

# Replace negative values in markersize column with zero
filtered_df[markersize] = filtered_df[markersize].clip(lower=0)

# Remove NA values
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis, color, markersize])

HS_select = st.multiselect("Filtrovat HS6 kódy",filtered_df['Název Produktu'])
plotlystyle = st.sidebar.selectbox("Styl grafu:",["plotly_dark","plotly","ggplot2","seaborn","simple_white","none"])
background_color = st.sidebar.selectbox('Barva pozadí',[None,'#0D1A27','#112841'])
pio.templates.default = plotlystyle
# Initialize the hover_data dictionary with default values of False for x, y, and markersize
hover_data = {col: True for col in hover_info}
# Ensure x_axis, y_axis, and markersize default to False if not explicitly provided in hover_info
hover_data.setdefault(x_axis, False)
hover_data.setdefault(y_axis, False)
hover_data.setdefault(markersize, False)

if HS_select == []:
    fig = px.scatter(filtered_df,
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     #title=f'{x_axis_display} vs {y_axis_display} barva podle {color_display}',
                     hover_data=hover_data,
                     #height='100%',
                     opacity=0.7,
                     size=markersize,
                     size_max=40)
    

else:
    fig = px.scatter(filtered_df[filtered_df['Název Produktu'].isin(HS_select)],
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     title=f'{x_axis} vs {y_axis} barva podle {color}',
                     hover_data=hover_data,
                     #height=700,
                     opacity=0.7,
                     size=markersize,
                     size_max=40
                     )

fig.update_layout(
    hoverlabel=dict(
        #bgcolor="white",
        #font_size=16,
        font_family="verdana"
    ),
        legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="top",    # Align the legend's top with the graph's bottom
        y=-0.3,           # Push the legend further below (negative moves it below the plot)
        xanchor="center", # Center the legend horizontally
        x=0.5             # Position it at the center of the graph
    ),
    plot_bgcolor=background_color,
    paper_bgcolor = background_color
    
                
)
st.plotly_chart(fig)
st.subheader("Big picture:")


#st.code("Vybraný český export za rok 2022: "+ "{:,.0f}".format(sum(filtered_df['CZ_export_2022']))+" CZK\n"+
#        "Vybraný český export 2025 až 2030: "+ "{:,.0f}".format(sum(filtered_df['CZ_Total_Export_25_30']))+" CZK\n"+
#        "Vybraný evropský export 2025 až 203: "+ "{:,.0f}".format(sum(filtered_df['EU_Total_Export_25_30']))+" CZK")
#

mybuff = StringIO()
fig.write_html(mybuff, include_plotlyjs='cdn')
html_bytes = mybuff.getvalue().encode()
st.download_button(
    label = "Stáhnout HTML",
    data = html_bytes,
    file_name = "plot.html",
    mime="text/html"
)