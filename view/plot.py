import pandas as pd
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.plotting import output_file, save
import io
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mpl_dates

plt.style.use('ggplot')



def plot_png(df_graph: pd.DataFrame, symbol, tf='1s', params=None):
    columns_names = ['Open', 'Close', 'Low', 'High', 'Volume']
    df = df_graph.copy()
    columns_rename = {col: col[0].upper() + col[1:].lower() for col in df.columns if col not in columns_names and col[0].upper() + col[1:].lower() in columns_names}
    df.rename(columns=columns_rename, inplace=True)
    df.index.name = 'Date'
    if isinstance(params, dict):
        apds = []
        if isinstance(params.get('lines'), list):
            apds.append(mpf.make_addplot(df[params['lines']]))
        if isinstance(params.get('notes'), list):
            notes_col = []
            for col in params.get('notes'):
                notes_col.append(f'{col}_YVAL')
                df[f'{col}_YVAL'] = df[col].apply(lambda x: 1 if x else np.nan)
                df[f'{col}_YVAL'] = df[f'{col}_YVAL'] * df['Low'] * 0.95
                # df[f'{col}_YVAL'] = int(df[col]) * df['Low'] * 0.95
                # df[f'{col}_YVAL'].replace(0, np.nan, inplace=True)
            apds.append(mpf.make_addplot(df[notes_col], type='scatter', markersize=200, marker='^'))
    else:
        apds = None
    df = df.fillna(value=np.nan)
    buf = io.BytesIO()
    mpf.plot(df, addplot=apds, type='candle', title=f'\n{symbol}', volume=False, savefig=buf)
    del df
    buf.seek(0)
    # IPydisplay.Image(buf.read())
    return buf

def plot_html(df_graph, symbol, tf='1s', params=None):
    html = None
    try:
        # df_graph.reset_index(inplace=True)
        # df_graph = df_graph.rename(columns = {'index':'datetime'})

        # plot = figure(x_axis_type="datetime", plot_width=600, plot_height=400, title=symbol)
        plot = figure(x_axis_type="datetime", width=600, height=400, title=symbol)


        #w = 12 * 60 * 60 * 1000  # half day in ms
        if tf == '1s': # TODO move to function
            w = 500  # half sec
        elif tf == '1m':
            w = 60 * 500  # half min
        elif tf == '5m':
            w = 5 * 60 * 500  # half 5 min
        else:
            w = 12 * 60 * 60 * 1000  # half day in ms
        plot.segment(df_graph.index, df_graph.high, df_graph.index, df_graph.low, color="black")
        inc = df_graph.close > df_graph.open
        plot.vbar(df_graph.index[inc], w, df_graph.open[inc], df_graph.close[inc], fill_color="lawngreen", line_color="lime")
        dec = df_graph.open > df_graph.close
        plot.vbar(df_graph.index[dec], w, df_graph.open[dec], df_graph.close[dec], fill_color="tomato", line_color="red")




        # show(plot)
        html = file_html(plot, CDN,  symbol)
        #
        # output_file(f"./{symbol}.html")
        # save(plot)

    # return html
    except Exception as err:
        print(err)

    return html
