import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output

import warnings
warnings.filterwarnings("ignore")

app = Dash(__name__)
app.title = 'Stock Alert Dashboard - Beta Version'

def get_filtered_data():
	df = pd.read_csv('data/stock.csv', header=None)
	df.rename(columns={0: 'Stock Name',
						1: 'Previous Close',
						2: 'Current Price',
						3: 'Minimum(Day)',
						4: 'Maximum(Day)',
						5: 'Minimum(Threshold)',
						6: 'Maximum(Threshold)',
						7: 'Last Update',
						8: 'difference',
						9: 'watch'}, inplace=True)

	columns = ['Stock Name', 'Previous Close', 'Current Price', 'difference', 'Minimum(Day)', 'Maximum(Day)', 'Minimum(Threshold)', 'Maximum(Threshold)', 'Last Update']
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
	return df, fd1, fd2

df, fd1, fd2 = get_filtered_data()

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
		dcc.Interval(
			id='interval-component-2',
			interval=5*1000,
			n_intervals=0
		),
	]),
])

@app.callback(
	Output('buy-table', 'data'),
	Input('interval-component', 'n_intervals'))
def update_data(n):
	_, fd1, _ = get_filtered_data()

	return fd1.to_dict('records')


@app.callback(
	Output('watch-table', 'data'),
	Input('interval-component-2', 'n_intervals'))
def update_data(n):
	_, _, fd2 = get_filtered_data()

	return fd2.to_dict('records')


if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=5000)