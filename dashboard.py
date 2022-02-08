import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output

df = pd.read_csv('data/stock.csv', header=None)
df.rename(columns={0: 'Stock Name', 
					1: 'Previous Close', 
					2: 'Current Price', 
					3: 'Minimum Day', 
					4: 'Maximum Day',
					5: 'Minimum Threshold',
					6: 'Maximum Threshold',
					7: 'DateNTime',
					8: 'difference'}, inplace=True)

df = df.round(2)
df['Up/Down'] = df['difference'].map(lambda x: 'Up' if x > 0 else 'Down')
filtered_df = df.groupby(['Stock Name']).max().reset_index()
app = Dash(__name__)


# update table colors   
app.layout = html.Div([
	html.H1('Stock Alert Dashboard - Beta Version'),
	dash_table.DataTable(
		id='table',
		columns=[{"name": i, "id": i} for i in filtered_df.columns],
		data=filtered_df.to_dict('records'),
		style_cell={'textAlign': 'center'},
		style_data_conditional=[
			{
				'if': {
					'filter_query': '{Up/Down} = "Down"'},
				# background color based on up/down column
				'backgroundColor': 'rgb(255, 204, 204)' # red
			},
			{
				'if': {
					'filter_query': '{Up/Down} = "Up"'},
				# background color based on up/down column
				'backgroundColor': 'rgb(204, 255, 204)' # green
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
			options=[{'label': i, 'value': i} for i in filtered_df['Stock Name'].unique()],
			value='Birlasoft Ltd'
		)
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
			'line': {'width': 1}
		}, 
		{
			'x': filtered_df['DateNTime'],
			'y': filtered_df['Minimum Threshold'],
			'name': 'Min Threshold',
			'mode': 'lines',
			'line': {'width': 3, 'dash': 'dash', 'color': 'red'},
		},
		{
			'x': filtered_df['DateNTime'],
			'y': filtered_df['Maximum Threshold'],
			'name': 'Max Threshold',
			'mode': 'lines',
			'line': {'width': 3, 'dash': 'dash', 'color': 'green'},
		}],

		'layout': {
			'title': stock,
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
	df.rename(columns={0: 'Stock Name', 
						1: 'Previous Close', 
						2: 'Current Price', 
						3: 'Minimum Day', 
						4: 'Maximum Day',
						5: 'Minimum Threshold',
						6: 'Maximum Threshold',
						7: 'DateNTime',
						8: 'difference'}, inplace=True)
	
	df = df.round(2)
	df['Up/Down'] = df['difference'].map(lambda x: 'Up' if x > 0 else 'Down')
	filtered_df = df.groupby(['Stock Name']).max().reset_index()

	filtered_df = df.groupby(['Stock Name',]).max().reset_index()
	return filtered_df.to_dict('records')


if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=8000, debug=True)