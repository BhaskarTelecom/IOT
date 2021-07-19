from operator import index
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

data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
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
x = pd.Series.to_frame(x)

x.reset_index(drop=True, inplace=True)

df = pd.DataFrame()
output["Time"] = x
#print(output)

#bar chart definition ---------------------------------------------------------------------------------------------------------------------
#fig = px.bar(output,y=["True","False"],x="Time",color_discrete_map={"True":"green","False":"red"})
#y=[output["True"],output["False"]],labels={output["True"]:"true",output["False"]:"False"}

#web layout ---------------------------------------------------------------------------------------------------------------------------------
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    { "href" : "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", 
       "rel" : "stylesheet",
       "integrity" :"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
       "crossorigin": "anonymous"
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
                interval=1*1000,
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
                                {"label": "Room 1", "value": "Room 1"}
                                
                            ],
                            value="Room 1",
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
                                for (sensorType,sensorID) in [("Soldering Station Temp","SST0100"),("Pressure","SPS0100")]
                                
                            ],
                            value="SST0100",
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
                    children=[
                        html.Div(
                            daq.Thermometer(
                                id='my-thermometer',
                                label="Room Temperature",
                                value=22,
                                min=15,
                                max=35,
                                showCurrentValue=True,
                                units="°C",
                                style={
                                    'margin-bottom': '5%'
                                },
                                className="temp-widget",
                            )
                        ),
                        html.Div(
                            daq.Gauge(
                                id='my-gauge',
                                label="Relative Room Humidity",
                                value=60,
                                max=100,
                                min=0,
                                units="%",
                                showCurrentValue=True,
                                className="gauge",
                            ),        
                        ),  
                    ],
                    className="col-md-3 left-box",
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
                            ),
                            className="card",
                        ),
                    ],
                    className="col-md-6 wrapper",
                ),
                html.Div(
                    children=[
                        html.Div(
                            html.P(
                                id="humidity-act",
                                children=['Humidity Actuator:']
                            ),
                            className="card right"  
                        ),
                        html.Div(
                            html.P(
                                id="temp-act",
                                children=['Temperature Actuator:']
                            ),
                            className="card right"  
                        ),
                        html.Div(
                            html.P(
                                id="osc-eqp",
                                children=['Oscillator Equipment:']
                            ),
                            className="card right"  
                        ),
                        html.Div(
                            html.P(
                                id="cb-eqp",
                                children=['init']
                            ),
                            className="card right"  
                        ),
                        html.Div(
                            [
                            html.H6("Test Bench"),
                            html.Table(
                                id="tb-eqp",
                                children=["init"],
                             className="table table-striped table-hover"           
                            )
                            
                            ],className="card right"
                        ),
                    ], className="col-md-3 right-box"
                )
            ],className="row"
        ),
    ]
)

#------------------------------------------------------------------------------------------------------------------
# Humidity Actuator

@app.callback(
    Output("humidity-act","children"),
    Input('my-interval','n_intervals')
)

def update_humidity_act_card(n_intervals):
    
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    sensorID = 'AHA0100'
    temp_mask = pd.notna(data[sensorID])
    
    return [html.Span("Humidity Actuator: "+data[sensorID][temp_mask].iloc[-1])]

#------------------------------------------------------------------------------------------------------------------
# Temperature Actuator

@app.callback(
    Output("temp-act","children"),
    Input('my-interval','n_intervals')
)

def update_temp_act_card(n_intervals):
    
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    sensorID = 'ARA0100'
    temp_mask = pd.notna(data[sensorID])
    
    return [html.Span("Temperature Actuator: "+data[sensorID][temp_mask].iloc[-1])]

#------------------------------------------------------------------------------------------------------------------
# Oscillator Equipment

@app.callback(
    Output("osc-eqp","children"),
    Input('my-interval','n_intervals')
)
def update_osc_card(n_intervals):
    
    sensorID = 'EOS0100'
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    temp_mask = pd.notna(data[sensorID])
    
    return [html.Span("Oscilloscope: "+data[sensorID][temp_mask].iloc[-1])]

#------------------------------------------------------------------------------------------------------------------
# Test Bench Equipment

@app.callback(
    Output("tb-eqp","children"),
    Input('my-interval','n_intervals')
)
def update_test_bench_card(n_intervals):
    
    sensorID = 'ETB0100'
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    
    tb_mask = pd.notna(data[sensorID])
    test_bench_dict = ast.literal_eval(data[sensorID][tb_mask].iloc[-1])
    
    
    
    return [html.Table(
                [   
                    html.Tr(
                        [
                            html.Th("Zero"),
                            html.Th("Span"),
                        ],className="text-center"
                    ),
                    html.Tr(
                        [
                            html.Td("Voltage: "+str(round(test_bench_dict["minValueVolt"],2))+"V",className="text-center"),
                            html.Td("Voltage: "+str(round(test_bench_dict["maxValueVolt"],2))+"V",className="text-center")
                        ]    
                    ),
                    html.Tr(
                        [
                            html.Td("Current: "+str(round(test_bench_dict["minValueCurr"],2))+"mA",className="text-center"),
                            html.Td("Current: "+str(round(test_bench_dict["maxValueCurr"],2))+"mA",className="text-center")
                        ]
                    )
                ]
                )
            ]

#------------------------------------------------------------------------------------------------------------------
# Conveyor Belt

@app.callback(
    Output("cb-eqp","children"),
    Input('my-interval','n_intervals')
)
def update_conveyor_belt_card(n_intervals):
    
    sensorID = 'ECB0100'
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    temp_mask = pd.notna(data[sensorID])
    
    return [html.Span("Conveyor Belt : "+data[sensorID][temp_mask].iloc[-1])]

#------------------------------------------------------------------------------------------------------------------
# Temperature Sensor

@app.callback(
    Output('my-thermometer', 'value'),
    [Input('my-interval','n_intervals')]
)
def update_thermometer(value):

    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    temp_mask = pd.notna(data['SRT0100'])
    
    return data['SRT0100'][temp_mask].iloc[-1]

#------------------------------------------------------------------------------------------------------------------
# Humidity Sensor

@app.callback(
    Output('my-gauge', 'value'),
    [Input('my-interval','n_intervals')]
)
def update_gauge(value):

    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    humidity_mask = pd.notna(data["SHS0100"])

    return data['SHS0100'][humidity_mask].iloc[-1]

#------------------------------------------------------------------------------------------------------------------
# Dropdown Sensor graph

@app.callback(
    [Output("chart-1","figure"),
    Output("chart-2","figure")],
    [Input('my-interval','n_intervals'),
    Input('sensor-filter','value')]
)
def update_graphs(figure,sensorID): 
    
    data = pd.read_csv("/home/bhaskar/IOT/IOT/IOT-devAshwini/dataBase/room01DB.csv")
    
    sensorMask = pd.notna(data[sensorID])
    
    real_time = data["time"][sensorMask]
    real_time = pd.to_datetime(real_time)

    unitCountMask = pd.notna(data["SIR0100"])
    unitCount = data["SIR0100"][unitCountMask]

    time1 = data["time"][unitCountMask]


    output = pd.DataFrame()
    for item in unitCount:
        item = ast.literal_eval(item)
        output = output.append(item, ignore_index=True)



    x = pd.to_datetime(time1)
    x = pd.Series.to_frame(x)

    x.reset_index(drop=True, inplace=True)

    df = pd.DataFrame()
    output["Time"] = x

    if(sensorID=="SST0100"):
        sensor_graph_title = "Soldering Station Temperature (°C)"
    elif (sensorID == "SPS0100"):
        sensor_graph_title = "Output Pressure Value (kg)"
    
    sensorGraph = {
        "data": [
            {
                "x": real_time,
                "y": data[sensorID][sensorMask],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": sensor_graph_title,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": False},
            "yaxis": {"ticksufix": "C", "fixedrange": False},
            "colorway": ["#17B897"],
        },
    }

    fig = px.bar(output,y=["True","False"],x="Time",color_discrete_map={"True":"green","False":"red"})

    return sensorGraph,fig


if __name__ == "__main__":
    app.run_server(debug=False,port=5055)





