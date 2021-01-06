# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:04:41 2020

@author: dsmit
"""


from flask import Flask, render_template, request, redirect
#"""
import alpha_vantage
import requests


from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.io import curdoc, show

import pandas as pd
from bokeh.layouts import row
from bokeh.io import output_file, show
from bokeh.plotting import figure, save
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource, Select
from bokeh.io import curdoc
from alpha_vantage.timeseries import TimeSeries
from bokeh.embed import components 
from bokeh.io import output_file, show





def fetch(ticker) :
    ticker=ticker.upper()
    

    ts = TimeSeries(key='MO8BPQU6ZKVP11BJ',output_format='pandas')
    data, meta_data = ts.get_intraday(ticker)
        
    data['date'] = data.index
        
    new_data = {'x' : data.date,'y'   : data['1. open'].to_list(),
           }
        
    df = ColumnDataSource(new_data)
    return(df) 








def make_figure(df):

	p=figure(x_axis_type="datetime", width=400, height=300)
	p.line('x', 'y', source = df)


	p.grid.grid_line_alpha=0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Price'
	output_file('templates/plot.html')
	save(p)
	script, div=components(p)
	return(script, div)



app = Flask(__name__)

app.vars = {}



@app.route('/')
def index():
  return render_template('index.html')


@app.route('/plotpage', methods=['POST'])
def plotpage():
	tickStr=request.form['tickerText']
	app.vars['ticker']=tickStr.upper()
	df=fetch(app.vars['ticker'])
	script,div=make_figure(df)
	return render_template('plot.html', script=script, div=div)



if __name__ == '__main__':
    app.run(port=33507)

