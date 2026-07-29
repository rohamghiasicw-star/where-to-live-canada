"""Per-country configuration.

Everything that differs between the Canadian and US builds lives here, so the app
code, the CSS and the question engine stay single-source. The rule: if a string
names a country, an agency, a statistical geography or a projection, it belongs in
this file and not in app/.

Both countries emit places with a `prov` field. For Canada that holds the province
code, for the US the two-letter state code. The app never needs to know which,
which is why the field kept its original name instead of being renamed to
something neutral and churning every call site.
"""

# ---- Canada -----------------------------------------------------------------
# Statistics Canada Lambert Conformal Conic, EPSG:3347: the projection Canada is
# actually drawn in.
CA_PROJ = dict(p1=49.0, p2=77.0, lat0=63.390675, lon0=-91.866666666)

CA = dict(
    cc='CA',
    country='Canada',
    adjective='Canadian',
    unit='province',
    out='index.html',
    staging='staging/index.html',
    rings='data/canada_rings.json',
    rings_key='prov',
    proj=CA_PROJ,
    # padding as a fraction of extent: fit the sheet to the inhabited band, not the
    # full national extent. Canada reaches 83N but nobody here lives past 64N.
    pad=dict(x=0.045, y=0.10, ybot=0.7),
    climate_period='1981-2010',
    smoke_period='2013-2024',
    pop_year='2025',
    census_year='2021',
    vote_year='2025',
    riding_label='Riding',
    # per-dimension provenance, shown on the column tooltips
    sources={
        'climate': 'Environment Canada normals 1981-2010',
        'smoke': 'ECCC FireWork, the model run with fires minus the run without',
        'census': '2021 Census',
        'pop': "StatCan's July 2025 estimate",
        'politics': 'Elections Canada, 2025 result, vote-weighted',
        'politics_unit': 'federal riding',
        'religion': '2021 Census, religion (25% sample)',
    },
    # the one-line provenance under the result
    prov_line=("Climate from Environment Canada normals. Smoke from the ECCC FireWork model, "
               "fires differenced out. Population, income, housing, age and religion from the "
               "2021 Census and StatCan's 2025 estimate. Politics from the 2025 federal result."),
    detail_note=("Population is StatCan's July 2025 estimate; income, home value and the rest are "
                 "2021 Census. Home value is what owners estimated in 2021, not a market price."),
)

# ---- United States ----------------------------------------------------------
# USGS Albers Equal Area Conic for the contiguous US, EPSG:5070, with Alaska and
# Hawaii projected separately and placed as insets (see src/us/build_map.py).
US = dict(
    cc='US',
    country='the United States',
    country_short='the USA',
    adjective='American',
    unit='state',
    out='us/index.html',
    staging='staging/us/index.html',
    rings='data/us/us_rings.json',
    rings_key='state',
    proj=None,               # already projected to metres by src/us/build_map.py
    pad=dict(x=0.02, y=0.04, ybot=1.0),
    climate_period='1991-2020',
    smoke_period=None,       # set once the smoke dataset lands
    pop_year='2023',
    census_year='2023',
    vote_year='2024',
    riding_label='County',
    sources={
        'climate': 'NOAA climate normals 1991-2020',
        'smoke': None,
        'census': 'American Community Survey 5-year',
        'pop': 'ACS 5-year estimate',
        'politics': '2024 presidential result, county level, vote-weighted',
        'politics_unit': 'county',
        'religion': None,    # the US census does not ask about religion
    },
    prov_line=("Climate from NOAA climate normals. Population, income, housing and age from the "
               "American Community Survey. Politics from the 2024 presidential result at county "
               "level, which is a coarse instrument in big counties."),
    detail_note=("Population, income, home value and the rest are American Community Survey "
                 "5-year estimates. Home value is a self-reported median, not a market price."),
)

BY_CC = {'CA': CA, 'US': US}


def other(cc):
    """The sibling country, for the switch link. Paths are relative to the built
    page, which is why the two directions are not symmetrical: Canada sits at the
    root and the US one directory down."""
    if cc == 'CA':
        return dict(cc='US', label='the USA', href='us/')
    return dict(cc='CA', label='Canada', href='../')
