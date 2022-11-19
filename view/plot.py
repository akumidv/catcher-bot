import pandas as pd
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.plotting import output_file, save



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
