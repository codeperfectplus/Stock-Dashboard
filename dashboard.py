import pytz
import datetime
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output

import warnings
warnings.filterwarnings("ignore")

IST = pytz.timezone('Asia/Kolkata')
today_date = datetime.datetime.now(IST).strftime('%d-%m-%Y')

# change min and max time from 9 to 16
min_time = today_date + ' 09:00:00'
max_time = today_date + ' 16:00:00'

#change str date to datetime
min_time = datetime.datetime.strptime(min_time, '%d-%m-%Y %H:%M:%S')
max_time = datetime.datetime.strptime(max_time, '%d-%m-%Y %H:%M:%S')

print('Min Time: ', min_time)
print('Max Time: ', max_time)



app = Dash(__name__)
app.title = 'Stock Alert Dashboard - Beta Version'

def get_filtered_data():
	df = pd.read_csv('data/stock.csv', header=None)
	df.rename(columns={0: 'Stock Name',
						1: 'Previous Close',
						2: 'Current Price',
						3: 'Minimum(Day)',
						4: 'Maximum(Day)',
						5: 'Minimum(Year)',
						6: 'Maximum(Year)',
						7: 'Minimum(Threshold)',
						8: 'Maximum(Threshold)',
						9: 'Last Update',
						10: 'difference',
						11: 'watch'}, inplace=True)

	columns = ['Stock Name', 'Previous Close', 'Current Price', 'difference', 'Minimum(Day)', 'Maximum(Day)', 'Minimum(Year)', 'Maximum(Year)', 'Minimum(Threshold)', 'Maximum(Threshold)']
	df = df.round(2)
	df['Last Update'] = pd.to_datetime(df['Last Update'])
	lastest_date = df.groupby(['Stock Name'])['Last Update'].max().reset_index()['Last Update']

	filtered_df = df[df['Last Update'].isin(lastest_date)]
	filtered_df.sort_values(by=['difference'], inplace=True, ascending=False)
	filtered_df["Last Update"] = filtered_df["Last Update"].apply(lambda x: x.strftime('%H:%M:%S'))
	fd1 = filtered_df[filtered_df['watch'] == True]
	fd2 = filtered_df[filtered_df['watch'] == False]
	fd1 = fd1[columns]
	fd2 = fd2[columns]
	return df, fd1, fd2, lastest_date[0]

df, fd1, fd2, latest_date = get_filtered_data()

def get_dash_table(table_id, df):
	return dash_table.DataTable(
			id=table_id,
			columns=[{"name": i, "id": i} for i in df.columns],
			data=df.to_dict('records'),
			style_cell={'textAlign': 'center'},
			style_data={
				'border': '1px solid black',
				},
			style_header={
				'border': '1px solid black',
				'backgroundColor': 'white',
				'color': 'black',
				'fontWeight': 'bold',
				'textAlign': 'center',
				'font-family': 'Courier New',
				},

			style_data_conditional=[
				{
					'if': {
						'filter_query': '{difference} >= 0'},
					'backgroundColor': 'rgb(0, 102, 51)',
					'color': 'white',
					'fontWeight': 'bold'
				},
				{
					'if': {
						'filter_query': '{difference} < 0'},
					'backgroundColor': 'rgb(102, 0, 0)',
					'color': 'white',
					'fontWeight': 'bold'
				}
				
			],
			style_table={
				'width': '100%',
				'height': '100%',
				'overflowY': 'scroll',
				'overflowX': 'scroll',
				'textAlign': 'center',
			},
		)
	
app.layout = html.Div([
	html.H1('Stock Alert Dashboard - Beta Version',
			style={'textAlign': 'center', 'color': '#0099ff', 'font-family': 'Courier New',
			'font-size': '30px', 'font-weight': 'bold', 'margin-top': '20px'}),
	# update dbc badge
	html.H3(id='badge-update', style={'textAlign': 'center', 'color': '#0099ff', 'font-family': 'Courier New', 'font-size': '20px', 'font-weight': 'bold'}),
	html.H2('Buy List',  style={'textAlign': 'center', 'color': '#0099ff', 'font-family': 'Courier New', 'font-size': '20px', 'font-weight': 'bold', 'margin-top': '20px'}),
	dbc.Row([
		get_dash_table('buy-table', fd1),
		dcc.Interval(
			id='interval-component',
			interval=5*1000,
			n_intervals=0
		),
		html.H2('Watch List',  style={'textAlign': 'center', 'color': '#0099ff', 'font-family': 'Courier New', 'font-size': '20px', 'font-weight': 'bold'}),
		get_dash_table('watch-table', fd2),
	]),
	# graph by stock name select box
	html.Div([
		html.Label('Select Stock Name', style={'font-family': 'Courier New', 'font-size': '20px', 'font-weight': 'bold'}),
		dcc.Dropdown(
			id='stock-name-select',
			options=[{'label': i, 'value': i} for i in df['Stock Name'].unique()],
			value='Steel Authority of India Limited',
			style={'width': '100%', 'margin-top': '20px', 'color': '#0099ff', 'font-family': 'Courier New', 'font-size': '20px'}
		)
	]),
	html.Div([
		dcc.Graph(id='stock-name-graph'),
	]),
])

# callback for interval component
@app.callback(
	Output('buy-table', 'data'),
	Input('interval-component', 'n_intervals'))
def update_data(n):
	_, fd1, _, _ = get_filtered_data()

	return fd1.to_dict('records')

@app.callback(
	Output('watch-table', 'data'),
	Input('interval-component', 'n_intervals'))
def update_data(n):
	_, _, fd2, _ = get_filtered_data()

	return fd2.to_dict('records')

@app.callback(
	Output('badge-update', 'children'),
	Input('interval-component', 'n_intervals'))
def update_badge(n):
	_, _, _, latest_date = get_filtered_data()

	return "Dashboard last updated at {}".format(latest_date.strftime('%H:%M:%S'))


@app.callback(
	Output('stock-name-graph', 'figure'),
	Input('stock-name-select', 'value'),
	Input('interval-component', 'n_intervals'))
def update_graph(stock_name, n):
	df, _, _, _ = get_filtered_data()
	filtered_df = df[df['Stock Name'] == stock_name]

	return {
		'data': [{
			'x': filtered_df['Last Update'],
			'y': filtered_df['Current Price'],
			'name': 'Current Price',
			'mode': 'lines',
			'line': {'width': 1}
		}, 
		{
			'x': filtered_df['Last Update'],
			'y': filtered_df['Minimum(Threshold)'],
			'name': 'Min Threshold',
			'mode': 'lines',
			'line': {'width': 1, 'dash': 'dash', 'color': 'red'},
		},
		{
			'x': filtered_df['Last Update'],
			'y': filtered_df['Maximum(Threshold)'],
			'name': 'Max Threshold',
			'mode': 'lines',
			'line': {'width': 1, 'dash': 'dash', 'color': 'green'},
		}],

		'layout': {
			'title': stock_name,
			'xaxis': {'title': 'Date'},
			'yaxis': {'title': 'Price'},
			'height': 600,
			'margin': {'l': 60, 'r': 10},
			'hovermode': 'closest',
			'showlegend': True,
			'orientation':"h",
			'yanchor':"bottom",
			'y':1.02,
			'xanchor':"right",
			'x':2,
			'yaxis': {'range': [min(filtered_df['Minimum(Threshold)']) - 10, max(filtered_df['Maximum(Threshold)']) + 10]},
			'xaxis': {'range': [min_time, max_time]}

		}
	}

if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=5000)