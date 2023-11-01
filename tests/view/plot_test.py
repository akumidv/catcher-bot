import io

import pytest
from view import plot


import pandas as pd


@pytest.fixture
def df():
    df = pd.DataFrame.from_dict({
        '2022-11-17 04:10:00': {'open':  0.00488, 'high':  0.00488, 'low':    0.00486, 'close':    0.00487, 'MAL':  0.004954, 'MAS':  0.004974, 'note': None},
        '2022-11-17 04:15:00': {'open':  0.00487, 'high':  0.00489, 'low':  0.00486, 'close':    0.00489, 'MAL': 0.004953, 'MAS':  0.004966, 'note': None},
        '2022-11-17 04:20:00': {'open':  0.00489, 'high':  0.00490, 'low':  0.00488, 'close':    0.00489, 'MAL':   0.004952, 'MAS':  0.004959, 'note': 'test'},
        '2022-11-17 04:25:00': {'open':  0.00489, 'high':  0.00490, 'low':  0.00488, 'close':    0.00490, 'MAL': 0.004952, 'MAS':  0.004953, 'note': None},
        '2022-11-17 04:30:00': {'open':  0.00490, 'high':  0.00494, 'low':  0.00489, 'close':    0.00494, 'MAL':   0.004952, 'MAS':  0.004952, 'note': 'signal'},
        '2022-11-17 04:35:00': {'open':  0.00494, 'high':  0.00557, 'low':  0.00494, 'close':    0.00543, 'MAL':   0.004956, 'MAS':  0.004997, 'note': None},
        }, orient='index')
    df.index = pd.to_datetime(df.index)
    df['ts'] = df.index.astype('int64') / 1000000
    return df


params = {
    'lines': ['MAL', 'MAS'],
    'notes': ['note']
}

@pytest.mark.skip
def test__get_graph_png(df):
    png = plot.plot_png(df, 'STMXUSDT', '5m', params)
    assert isinstance(png, io.BytesIO)
    with open('./test.png', 'wb') as f:
        f.write(png.getbuffer())

@pytest.mark.skip
def test__get_graph_html(df):

    params = {'root_time': 1668659100325, 'top_time': 1668659700123,
            'kontr_min_time': 1668658200020, 'kontr_max_time':   1668658800400}
    print(pd.to_datetime('2022-11-17 04:20:00').to_datetime64().astype('int64')/1000000)
    # print(pd.to_datetime(scan['root_time']).floor('S'))
    html = plot.plot_html(df, 'STMXUSDT', '5m', params)
    # TODO test html
    # TODO implelemen symbols, plot lines and soon settled by params


