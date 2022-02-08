import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output

df = pd.read_csv('data/stock.csv', header=None)
df.rename(columns={0: 'stock_name', 
                    1: 'previous_close', 
                    2: 'current_price', 
                    3: 'day_min', 
                    4: 'day_max',
                    5: 'Minimum Threshold',
                    6: 'Maximum Threshold',
                    7: 'date_time'}, inplace=True)

filtered_df = df.groupby(['stock_name']).max().reset_index()

app = Dash(__name__)

# update table colors   
app.layout = html.Div([
    html.H1('Stock Alert'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
    ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    ),
    html.Br(),
    # graph by stock name select box
    html.Div([
        html.Label('Select Stock Name'),
        dcc.Dropdown(
            id='stock-name-select',
            options=[{'label': i, 'value': i} for i in filtered_df['stock_name'].unique()],
            value='SAIL'
        )
    ]),
    html.Br(),    
    html.Div([
        dcc.Graph(id='stock-name-graph'),
    ]),
])

@app.callback(
    Output('stock-name-graph', 'figure'),
    Input('stock-name-select', 'value'))
def update_graph(stock_name):
    filtered_df = df[df['stock_name'] == stock_name]

    return {
        'data': [{
            'x': filtered_df['date_time'],
            'y': filtered_df['current_price'],
            'name': 'Current Price',
            'mode': 'lines',
            'line': {'width': 1}
        }, 
        {
            'x': filtered_df['date_time'],
            'y': filtered_df['Minimum Threshold'],
            'name': 'Min Threshold',
            'mode': 'lines',
            'line': {'width': 3, 'dash': 'dash', 'color': 'red'},
        },
        {
            'x': filtered_df['date_time'],
            'y': filtered_df['Maximum Threshold'],
            'name': 'Max Threshold',
            'mode': 'lines',
            'line': {'width': 3, 'dash': 'dash', 'color': 'green'},
        }],

        'layout': {
            'title': stock_name,
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'},
            'height': 600,
            'margin': {'l': 60, 'r': 10},
            'legend': {'x': 0, 't': 0, 'y': 1},
            'hovermode': 'closest',
            'showlegend': True,
            'legend': {'x': 0, 'y': 1},
            # y axis range
            'yaxis': {'range': [min(filtered_df['Minimum Threshold']) - 10, max(filtered_df['Maximum Threshold']) + 10]}

        }
    }

@app.callback(
    Output('table', 'data'),
    Input('interval-component', 'n_intervals'))
def update_data(n):
    df = pd.read_csv('data/stock.csv', header=None)
    df.rename(columns={0: 'stock_name', 
                        1: 'previous_close', 
                        2: 'current_price', 
                        3: 'day_min', 
                        4: 'day_max',
                        5: 'Minimum Threshold',
                        6: 'Maximum Threshold',
                        7: 'date_time'}, inplace=True)
    filtered_df = df.groupby(['stock_name',]).max().reset_index()
    return filtered_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000)