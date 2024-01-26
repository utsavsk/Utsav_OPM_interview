from flask import Blueprint, render_template, request 
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo



### Running a blueprint because this code is part of a much larger website
views = Blueprint('views', __name__)


### Loading the data from Predict_NASDAQ.csv
df_all_NASDAQ = pd.read_csv('Predict_NASDAQ.csv')
df_all_NASDAQ['Close_date'] = pd.to_datetime(df_all_NASDAQ['Close_date'])
df_all_NASDAQ['Predicted_date'] = pd.to_datetime(df_all_NASDAQ['Predicted_date'])
tickers_NASDAQ = df_all_NASDAQ['Ticker'].unique()


### function to draw a simple chart for selected ticker
def get_chart_data(df_all, tickers):
    plot_columns = ['Close_date', 'Predicted_date', 'MaxHigh_30',	'MinHigh_30',	'MaxHigh_90',	'MinHigh_90',	'Close',  'Predicted_price', 'average_volume']

    selected_ticker = request.form.get('ticker_dropdown')
    #print(f'Received request for ticker: {selected_ticker}')

    df_selected = df_all[df_all['Ticker'] == selected_ticker][plot_columns]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_selected['Close_date'], y=df_selected['MaxHigh_30'], mode='lines',                   legendgroup="resistance", name='Resistance Levels', line=dict(color='lime')))
    fig.add_trace(go.Scatter(x=df_selected['Close_date'], y=df_selected['MaxHigh_90'], mode='lines', showlegend=False, legendgroup="resistance", name='Resistance Levels', line=dict(color='lime')))
    fig.add_trace(go.Scatter(x=df_selected['Close_date'], y=df_selected['MinHigh_30'], mode='lines',                   legendgroup="support", name='Support Levels', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df_selected['Close_date'], y=df_selected['MinHigh_90'], mode='lines', showlegend=False, legendgroup="support", name='Support Levels', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df_selected['Close_date'], y=df_selected['Close'], mode='lines',                   legendgroup="close", name='Close', line=dict(color='black')))
    

    fig.update_layout(title=f'Ticker: {selected_ticker}', xaxis_title='Date', yaxis_title='Price')
                  

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    fig.update_layout(xaxis_range=[min(df_selected['Close_date']), max(df_selected['Close_date'])  ] )
    
    # Disable the mode bar
    config = {'displayModeBar': False}

    formatted_predicted_date = df_selected['Predicted_date'].tolist()[0].strftime('%B %d, %Y')
    formatted_predicted_range = df_selected['Predicted_price'].tolist()[0]
    formatted_average_volume = df_selected['average_volume'].tolist()[0]

    chart_html = pyo.plot(fig, output_type='div', include_plotlyjs=False, config=config, show_link=False)

    sent_list = [chart_html, [formatted_predicted_date, formatted_predicted_range, formatted_average_volume]]

    return sent_list


#------------------------------
# Begin routes
#------------------------------

### Loading data one more time
predicted_data_NASDAQ = pd.read_csv('Predict_NASDAQ.csv')
ticker_list_unique_NASDAQ = predicted_data_NASDAQ[['Ticker', 'Company_Name']].drop_duplicates()


### Note: if I refer to the function directly using urlfor then this route can be anything.
@views.route('/', methods=['GET', 'POST'])
def dashboardNASDAQ():
    ticker_list = ticker_list_unique_NASDAQ.to_dict(orient='records')
    if request.method == 'POST':
        return render_template('getChart_partial.html', plot=get_chart_data(df_all_NASDAQ, tickers_NASDAQ)[0], textVal = get_chart_data(df_all_NASDAQ, tickers_NASDAQ)[1])
    else:
        return render_template("home.html", ticker_list = ticker_list, dashboard_name = "NASDAQ listed companies")
