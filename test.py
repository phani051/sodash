import mysql.connector
from sqlalchemy import create_engine
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

connection_string = "mysql+mysqlconnector://root:password@localhost:3306/sodash"
engine = create_engine(connection_string, echo=True)

df = pd.read_sql('SELECT * FROM sodata where soname="cfphsor03.sldc.sbc.com"', con=connection_string)

#print(df)

app = Dash()

# App layout
app.layout = [
    html.Div(children='StoreOnce capacity Planning'),
    html.Hr(),
    dcc.RadioItems(options=['dataondisk', 'userdata'], value='dataondisk', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure={}, id='controls-and-graph')
]

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='date', y=col_chosen)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)