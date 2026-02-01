from data_pipeline.fetch_gdp import fetch_gdp
from charts.gdp_chart import generate_gdp_chart

df = fetch_gdp()
generate_gdp_chart(df)

from data_pipeline.fetch_billboard import fetch_billboard
from charts.billboard_chart import generate_billboard_chart

df_billboard = fetch_billboard()
generate_billboard_chart(df_billboard)

from data_pipeline.fetch_imports import fetch_imports
from charts.imports_chart import generate_imports_chart

df_imports = fetch_imports()
generate_imports_chart(df_imports)