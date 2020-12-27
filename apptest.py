# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 20:34:05 2020

@author: dsmit
https://github.com/TommyBlanchard/FlaskHerokuStockTicker/blob/master/app.py
"""


#Try some stuff

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

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():
    output_file('C:/Users/dsmit/Documents/flask2/flask-framework/templates') 

    #ticker = request.form['ticker']
    ticker = 'GNTX'
    ts = TimeSeries(key='MO8BPQU6ZKVP11BJ',output_format='pandas')
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday(ticker )
    
    data['date'] = data.index
    
    new_data = {'x' : data.date,
                'y'   : data['1. open'].to_list(),
       }
    
    source = ColumnDataSource(new_data)


    p = figure(title = 'test', x_axis_type="datetime")
    p.line('x', 'y', source = source)
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)



if __name__ == '__main__':
    app.run(port=33507)