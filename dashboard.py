import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output

df = pd.read_csv('data/stock.csv', header=None)
df.rename(columns={0: 'Stock Name', 
					1: 'Previous Close', 
					2: 'Current Price', 
					3: 'Minimum(Day)', 
					4: 'Maximum(Day)',
					5: 'Minimum Threshold',
					6: 'Maximum Threshold',
					7: 'DateNTime',
					8: 'difference'}, inplace=True)

df = df.round(2)
df['Up/Down'] = df['difference'].map(lambda x: 'Up' if x > 0 else 'Down')
filtered_df = df.groupby(['Stock Name']).max().reset_index()

app = Dash(__name__)
app.title = 'Stock Alert Dashboard - Beta Version'


# update table colors   
app.layout = html.Div([
	html.H1('Stock Alert Dashboard - Beta Version',
			style={'textAlign': 'center', 'color': '#0099ff', 'font-family': 'Courier New', 
			'font-size': '30px', 'font-weight': 'bold', 'margin-top': '20px'}),
	dash_table.DataTable(
		id='table',
		columns=[{"name": i, "id": i} for i in filtered_df.columns],
		data=filtered_df.to_dict('records'),
		style_cell={'textAlign': 'center'},
		style_data={ 
			'border': '2px solid black',
			},
		style_header={
			'border': '2px solid black',
        	'backgroundColor': 'white',
			'color': 'black',
			'fontWeight': 'bold',},
		style_data_conditional=[
			{
				'if': {
					'filter_query': '{Up/Down} = "Down"'},
				'backgroundColor': 'rgb(102, 0, 0)', # red
				'color': 'white'
			},
			{
				'if': {
					'filter_query': '{Up/Down} = "Up"'},
				'backgroundColor': 'rgb(0, 102, 51)', # green
				'color': 'white',
			}
		],
		style_table={
			'width': '100%',
			'height': '100%',
			'overflowY': 'scroll',
			'overflowX': 'scroll'
		},
	),
	dcc.Interval(
		id='interval-component',
		interval=5*1000,
		n_intervals=0
	),
	html.Br(),
	# graph by stock name select box
	html.Div([
		html.Label('Select Stock Name', style={'font-family': 'Courier',
			'font-size': '20px', 'font-weight': 'bold'}),
		dcc.Dropdown(
			id='stock-name-select',
			options=[{'label': i, 'value': i} for i in filtered_df['Stock Name'].unique()],
			value=filtered_df['Stock Name'].unique()[0],
			style={'width': '100%'}
		),
	]),
	html.Div([
		dcc.Graph(id='stock-name-graph'),
	]),
	
				
])

@app.callback(
	Output('stock-name-graph', 'figure'),
	Input('stock-name-select', 'value'))
def update_graph(stock):
	filtered_df = df[df['Stock Name'] == stock]

	return {
		'data': [{
			'x': filtered_df['DateNTime'],
			'y': filtered_df['Current Price'],
			'name': 'Current Price',
			'mode': 'lines',
			'line': {'width': 3, 'color': '#0099ff', 'dash': 'dash'},
			'hoverinfo': 'y',
		}, 
		{
			'x': filtered_df['DateNTime'],
			'y': filtered_df['Minimum Threshold'],
			'name': 'Min Threshold',
			'mode': 'lines',
			'line': {'width': 2, 'dash': 'scatter', 'color': 'red'},
			'hoverinfo': 'y',
		},
		{
			'x': filtered_df['DateNTime'],
			'y': filtered_df['Maximum Threshold'],
			'name': 'Max Threshold',
			'mode': 'lines',
			'line': {'width': 2, 'dash': 'scatter', 'color': 'green'},
			'hoverinfo': 'y',
		}],

		'layout': {
			'title': stock,
			'xaxis': {'title': 'Date', 'type': 'date' , 
					  'range' : [filtered_df['DateNTime'].min(), filtered_df['DateNTime'].max()]},
			'yaxis': {'title': 'INR (Indian Rupee)', 'type': 'linear',
					  'range': [min(filtered_df['Minimum Threshold']) - 10, max(filtered_df['Maximum Threshold']) + 10]},
			'hovermode': 'compare',
			'height': '500',
			'plot_bgcolor': '#f9f9f9',
			'paper_bgcolor': '#f9f9f9',
			'font': {'family': 'Courier', 'size': 12},
			'legend': {'x': 0.5, 'y': 1.0},
			'hoverlabel': {'bgcolor': '#0099ff', 'font': {'color': 'white'}},
			'legend': dict(
        			orientation="h",
        			yanchor="top",
        			y=1,
					x=1.1,
			        xanchor="right"),	
		}
	}


@app.callback(
	Output('table', 'data'),
	Input('interval-component', 'n_intervals'))
def update_data(n):
	filtered_df = df.groupby(['Stock Name']).max().reset_index()
	return filtered_df.to_dict('records')


if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=5000)