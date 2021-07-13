import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_daq as daq
import plotly.express as px
import ast 

#data pre-processing-------------------------------------------------------------------------------------------------------------------------

data = pd.read_csv("https://raw.githubusercontent.com/BhaskarTelecom/IOT/devAshwini/dataBase/room01DB.csv")
masterData = pd.read_csv("https://raw.githubusercontent.com/BhaskarTelecom/IOT/devAshwini/dataBase/masteDB.csv")


a = np.linspace(20,25,646)
trial_column = pd.concat([data,pd.Series(a)],axis=1)


mask = pd.notna(trial_column["SST0100"])
values = trial_column["SST0100"][mask]


time = trial_column["time"][mask]
time = pd.to_datetime(time)


unitCountMask = pd.notna(data["SIR0100"])
unitCount = data["SIR0100"][unitCountMask]
time1 = data["time"][unitCountMask]


output = pd.DataFrame()
for item in unitCount:
    item = ast.literal_eval(item)
    output = output.append(item, ignore_index=True)

x = pd.to_datetime(time1)
df = pd.DataFrame()
df = df.append(output)
df = df.append(x)


#bar chart definition ---------------------------------------------------------------------------------------------------------------------
fig = px.bar(df,y=[output["True"],output["False"]],x=x,color_discrete_map={"True":"green","False":"red"})


#web layout ---------------------------------------------------------------------------------------------------------------------------------
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Smart Manufacturing Systems!"

app.layout = html.Div([
    dcc.Interval(
                id='my-interval',
                disabled=False,
                interval=1*5000,
                n_intervals=0,
                max_intervals=-1
            ),
        html.Div(
            children=[
                html.P(children="🏭", className="header-emoji"),
                html.H1(
                    children="Smart Manufacturing System", className="header-title"
                ),
            ],
            className="header"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Room", className="menu-title"),
                        dcc.Dropdown(
                            id="room-filter",
                            options=[
                                {"label": "region", "value": "region"}
                                
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),    
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type of Sensor", className="menu-title"),
                        dcc.Dropdown(
                            id="sensor-filter",
                            options=[
                                {"label":sensorType , "value": sensorID}
                                for (sensorType,sensorID) in [("Soldering Station Temp","SST0100"),("Pressure","SPS0100"),("Temperature","SPS0100"),]
                                
                            ],
                            value="SRT0100",
                            clearable=False,
                            className="dropdown",
                        ),    
                    ]
                )
            ],
            className="menu"
        ),
        html.Div(
            children=[
                html.Div(
                    daq.Thermometer(
                        id='my-thermometer',
                        label="Room Temperature",
                        value=22,
                        min=15,
                        max=35,
                        showCurrentValue=True,
                        units="C",
                        style={
                            'margin-bottom': '5%'
                        },
                        className="temp-widget",
                    )
                ),
                html.Div(
                    daq.Gauge(
                        id='my-gauge',
                        label="Room Humidity",
                        value=60,
                        max=100,
                        min=0,
                        className="gauge",
                    ),        
                ),  
            ],
            className="left-box",
        ),       
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="chart-1",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="chart-2",
                        config={"displayModeBar": False},
                        figure=fig,
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

#Temp callback-----------------------------------------------------------

@app.callback(
    Output('my-thermometer', 'value'),
    [Input('my-interval','n_intervals')]
)
def update_thermometer(value):
    return trial_column[0][trial_column.index[-1]]

#Humidity Callback-------------------------------------------------------

@app.callback(
    Output('my-gauge', 'value'),
    [Input('my-interval','n_intervals')]
)
def update_gauge(value):

    return 

#Charts Update ----------------------------------------------------------

@app.callback(
    Output("chart-1","figure"),
    [Input('my-interval','n_intervals'),
    Input('sensor-filter','value')]
)
def update_graphs(figure,sensorID): 
    sensorMask = pd.notna(data[sensorID])
    sensorGraph = {
        "data": [
            {
                "x": time,
                "y": data[sensorID][sensorMask],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "sensorType",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksufix": "C", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    unitCountGraph = {
        "data": [
            {
                "x": time,
                "y": data["SIR0100"][unitCountMask],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Produced Units Count",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksufix": "C", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return sensorGraph


if __name__ == "__main__":
    app.run_server(debug=True,port=5052)





