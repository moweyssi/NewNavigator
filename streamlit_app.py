import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
from PIL import Image

st.set_page_config(
    page_title="Mapa Příležitostí",
    page_icon="favicon.png"
)
st.logo('logo.svg')
st.error('Toto je pracovní verze. Data s vyjímkou budoucího růstu pochází z CEPII databáze BACI. Projekce 2025-30 berte s velikou rezervou. Krom toho, že jsou odhadem, neberou v potaz inflaci.', icon="⚠️")
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
@st.cache_data
def load_data():
    # Replace with the path to your data file
    #df                          = pd.read_csv('GreenComplexity_CZE_2022.csv')
    url = 'https://docs.google.com/spreadsheets/d/1mhv7sJC5wSqJRXdfyFaWtBuEpX6ENj2c/gviz/tq?tqx=out:csv'
    taxonomy = pd.read_csv(url)
    CZE = pd.read_csv('CZE.csv')
    GreenProducts = taxonomy.merge(CZE,how='left',left_on='HS_ID',right_on='prod')
    # Calculate 2030 export value
    GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
    GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8

    # Calculate Total Export Value from 2025 to 2030
    # We calculate for each year and sum up
    GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))

    df = GreenProducts.rename(columns={'ExportValue': 'CZ Export 2022 CZK',
                              'pci': 'Komplexita výrobku 2022',
                               'relatedness': 'Příbuznost CZ 2022',
                               'PCI_Rank':'Žebříček komplexity 2022',
                               'PCI_Percentile':'Percentil komplexity 2022',
                               'relatedness_Rank':'Žebříček příbuznosti CZ 2022',
                               'relatedness_Percentile':'Percentil příbuznosti CZ 2022',
                               'WorldExport':'Světový export 2022 CZK',
                               'EUExport':'EU Export 2022 CZK',
                               'EUWorldMarketShare':'EU Světový Podíl 2022 %',
                               'euhhi':'Koncentrace evropského exportu 2022',
                               'hhi':'Koncentrace světového trhu 2022',
                               'CZE_WorldMarketShare':'CZ Světový Podíl 2022 %',
                               'CZE_EUMarketShare':'CZ-EU Podíl 2022 %',
                               'rca':'Výhoda CZ 2022',
                               'EUTopExporter':'EU Největší Exportér 2022',
                               'CZ_Nazev':'Název Produktu',
                               'CountryExport2030':'CZ 2030 Export CZK',
                               'EUExport2030':'EU 2030 Export CZK',
                               'CountryExport_25_30':'CZ Celkový Export 25-30 CZK',
                               'EUExport_25_30':'EU Celkový Export 25-30 CZK',
                               'CAGR_2022_30_FORECAST':'CAGR 2022-2030 Předpověď'
                               })
    df                          = df[df.Included == "IN"]
    df['stejna velikost']       = 0.02
    df['CZ-EU Podíl 2022 %']      = 100 * df['CZ-EU Podíl 2022 %'] 
    df['EU Světový Podíl 2022 %'] = 100 * df['EU Světový Podíl 2022 %'] 
    df['CZ Světový Podíl 2022 %'] = 100 * df['CZ Světový Podíl 2022 %'] 
    df['CZ Export 2022 CZK']        = USD_to_czk*df['CZ Export 2022 CZK'] 
    df['Světový export 2022 CZK']      = USD_to_czk*df['Světový export 2022 CZK'] 
    df['EU Export 2022 CZK']        = USD_to_czk*df['EU Export 2022 CZK'] 
    df['EU Celkový Export 25-30 CZK'] = USD_to_czk*df['EU Celkový Export 25-30 CZK'] 
    df['CZ Celkový Export 25-30 CZK'] = USD_to_czk*df['CZ Celkový Export 25-30 CZK'] 
    df['EU 2030 Export CZK']        = USD_to_czk*df['EU 2030 Export CZK'] 
    df['CZ 2030 Export CZK']        = USD_to_czk*df['CZ 2030 Export CZK'] 
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
    'Percentil příbuznosti CZ 2022',
    'Percentil komplexity 2022',
    'Žebříček příbuznosti CZ 2022',
    'Žebříček komplexity 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'ubiquity',
    'density',
    'cog',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export CZK',
    'EU Celkový Export 25-30 CZK',
    'CAGR 2022-2030 Předpověď',
    'Stejná Velikost'
]

hover_display_data = [
    'HS_ID',
    'Název Produktu',
    'CZ Celkový Export 25-30 CZK',
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'EU Největší Exportér 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export',
    'ubiquity',
    'EU Celkový Export 25-30 CZK',
    'CAGR 2022-2030 Předpověď',
    'Zdroj',
    'Percentil příbuznosti CZ 2022',
    'Percentil komplexity 2022',
    'Žebříček příbuznosti CZ 2022',
    'Žebříček komplexity 2022',
    'IS_REALCAGR'
]

# Sidebar selection boxes using display names
x_axis      = st.sidebar.selectbox("Vyber osu X:", plot_display_names, index=4)
y_axis      = st.sidebar.selectbox("Vyber osu Y:", plot_display_names, index=5)
markersize  = st.sidebar.selectbox("Velikost dle:", plot_display_names, index=9)
color       = st.sidebar.selectbox("Barva dle:", ji_display_names)


skupiny = df['Skupina'].unique()
Skupina = st.sidebar.multiselect('Skupina',skupiny,default=skupiny)
podskupiny = df['Podskupina'][df['Skupina'].isin(Skupina)].unique()
Podskupina = st.sidebar.multiselect('Podskupina',podskupiny,default=podskupiny)

# Filter section
if 'filters' not in st.session_state:
    st.session_state.filters = []

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Přidat filtr"):
        st.session_state.filters.append({'column': None, 'range': None})
with col2:
    if st.button("Odstranit filtry"):
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


filtered_df = filtered_df[filtered_df['Skupina'].isin(Skupina)]
filtered_df = filtered_df[filtered_df['Podskupina'].isin(Podskupina)]

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


HS_select = st.multiselect("Filtrovat HS6 kódy",filtered_df['HS_ID'])
hover_info  = st.sidebar.multiselect("Co se zobrazí při najetí myší:", hover_display_data, default='Název Produktu')
plotlystyle = st.sidebar.selectbox("Styl grafu:",["plotly_dark","plotly","ggplot2","seaborn","simple_white","none"])
background_color = st.sidebar.selectbox('Barva pozadí',[None,'#0D1A27','#112841'])
# Create a button in the sidebar that clears the cache
if st.sidebar.button('Obnovit Data'):
    load_data.clear()  # This will clear the cache for the load_data function
    st.sidebar.write("Sušenky vyčištěny!")
debug = st.sidebar.toggle('Debug')
pio.templates.default = plotlystyle
# Initialize the hover_data dictionary with default values of False for x, y, and markersize
#hover_data = {col: True for col in hover_info}

hover_data = {}
no_decimal = [
    'HS_ID',
    'CZ Celkový Export 25-30 CZK',
    'CZ Export 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export',
    'EU Celkový Export 25-30 CZK',
    'Žebříček příbuznosti CZ 2022',
    'Žebříček komplexity 2022',
]
one_sigfig = [
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'Komplexita výrobku 2022',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'ubiquity',
    'Percentil příbuznosti CZ 2022',
    'Percentil komplexity 2022',
    'CAGR 2022-2030 Předpověď',
]

# Iterate over the columns in hover_info
for col in hover_info:
    # If the column requires formatting, add it as the value in hover_data
    if col in no_decimal:
        hover_data[col] = ':.0r'
    elif col in one_sigfig:
        hover_data[col] = ':.3r'
    else:
        hover_data[col] = True  # No formatting needed, just show the column

# Ensure x_axis, y_axis, and markersize default to False if not explicitly provided in hover_info
#hover_data.setdefault(x_axis, False)
#hover_data.setdefault(y_axis, False)
hover_data.setdefault(markersize, False)

if HS_select == []:
    fig = px.scatter(filtered_df,
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40)
    

else:
    fig = px.scatter(filtered_df[filtered_df['HS_ID'].isin(HS_select)],
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     title=f'{x_axis} vs {y_axis} barva podle {color}',
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40
                     )

fig.update_layout(
    hoverlabel=dict(
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
    paper_bgcolor = background_color#,
    #hovermode='x unified'
    
                
)
st.plotly_chart(fig)
col1, col2, col3 = st.columns(3)
if HS_select == []:
    col1.metric("Vybraný český export za rok 2022", "{:,.0f}".format(sum(filtered_df['CZ Export 2022 CZK'])/1000000000),'miliard CZK' )
    col2.metric("Vybraný český export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['CZ Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    col3.metric("Vybraný evropský export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['EU Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    if debug:
        #st.dataframe(filtered_df)
        st.dataframe(df)
else:
    col1.metric("Vybraný český export za rok 2022", "{:,.1f}".format(sum(filtered_df[filtered_df['Název Produktu'].isin(HS_select)]['CZ Export 2022 CZK'])/1000000000),'miliard CZK' )
    col2.metric("Vybraný český export 2025 až 2030", "{:,.1f}".format(sum(filtered_df[filtered_df['Název Produktu'].isin(HS_select)]['CZ Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    col3.metric("Vybraný evropský export 2025 až 2030", "{:,.1f}".format(sum(filtered_df[filtered_df['Název Produktu'].isin(HS_select)]['EU Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    if debug:
        st.dataframe(filtered_df[filtered_df['Název Produktu'].isin(HS_select)])


mybuff = StringIO()
fig.write_html(mybuff, include_plotlyjs='cdn')
html_bytes = mybuff.getvalue().encode()
st.download_button(
    label = "Stáhnout HTML",
    data = html_bytes,
    file_name = "plot.html",
    mime="text/html"
)

