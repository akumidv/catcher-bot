import multiprocessing
import timeit

# https://docs.python.org/3/library/multiprocessing.html

def test_pipe_and_queue():
    ticker = {'open': 1234, 'close': 1235}
    ticker_str = "{'open': 1234, 'close': 1235}"

    iter = 250_000
    num = 10

    res_p_d = timeit.timeit(lambda: pipe_iter(ticker, iter), number=num)  # Only from one process to another one.
    print(f'Duplex pipes {iter}', round(res_p_d), 'sec', int(iter/(res_p_d/num)), 'per/sec',
          round((res_p_d/num)/iter * 1000, 4), 'ms per msg')

    res_p = timeit.timeit(lambda: pipe_iter(ticker, iter, is_duplex=False), number=num)  # Only from one process to another one.
    print(f'Not duplex pipes {iter}', round(res_p), 'sec', int(iter / (res_p / num)), 'per/sec',
          round((res_p / num) / iter * 1000, 4),
          'ms per msg')

    res_pst = timeit.timeit(lambda: pipe_iter(ticker_str, iter, is_duplex=False),
                          number=num)  # Only from one process to another one.
    print(f'Not duplex pipes for str {iter}', round(res_pst), 'sec', int(iter / (res_pst / num)), 'per/sec',
          round((res_pst / num) / iter * 1000, 4),
          'ms per msg')

    print('Pipes can\'t be shared between different process, Skipped')

    res_q = timeit.timeit(lambda: queue_iter(ticker, iter), number=num)  # Multiple process can get, but is's slowler
    print(f'Queue {iter}', round(res_q), 'sec', int(iter/(res_q/num)), 'per/sec',
          round((res_q/num)/iter * 1000, 4), 'ms per msg', 'pipe/queue:', round(res_p/res_q * 100, 2), '%')


    res_qs = timeit.timeit(lambda: queue_iter(ticker, iter, is_simple=True), number=num)  # Multiple process can get, but is's slowler
    print(f'Simple Queue {iter}', round(res_qs), 'sec', int(iter/(res_qs/num)), 'per/sec',
          round((res_qs/num)/iter * 1000, 4), 'ms per msg', 'pipe/queue:', round(res_p/res_qs * 100, 2), '%')

    res_qstr = timeit.timeit(lambda: queue_iter(ticker, iter, is_simple=True),
                           number=num)  # Multiple process can get, but is's slowler
    print(f'Simple Queue fro str {iter}', round(res_qstr), 'sec', int(iter / (res_qstr / num)), 'per/sec',
          round((res_qstr / num) / iter * 1000, 4), 'ms per msg', 'pipe/queue:', round(res_p / res_qstr * 100, 2), '%')

    res_q2 = timeit.timeit(lambda: queue_iter_x2(ticker, iter), number=num)
    print(f'Queue x2 {iter}', round(res_q2), 'sec', int(iter/(res_q2/num)), 'per/sec',
          round((res_q2/num)/iter * 1000, 4), 'ms per msg')

    res_qs2 = timeit.timeit(lambda: queue_iter_x2(ticker, iter, is_simple=True), number=num)
    print(f'Simple Queue x2 {iter}', round(res_qs2), 'sec', int(iter / (res_qs2 / num)), 'per/sec',
          round((res_qs2 / num) / iter * 1000, 4), 'ms per msg')

    print('Pipes and queue do not work with numba. Skipped')

# Duplex pipes 250000 21 sec 117649 per/sec 0.0085 ms per msg
# Not duplex pipes 250000 17 sec 148779 per/sec 0.0067 ms per msg
# Not duplex pipes for str 250000 16 sec 160246 per/sec 0.0062 ms per msg
# Pipes can't be shared between different process, Skipped
# Queue 250000 27 sec 93174 per/sec 0.0107 ms per msg pipe/queue: 62.63 %
# Simple Queue 250000 31 sec 80118 per/sec 0.0125 ms per msg pipe/queue: 53.85 %
# Simple Queue fro str 250000 21 sec 119651 per/sec 0.0084 ms per msg pipe/queue: 80.42 %
# Queue x2 250000 30 sec 82872 per/sec 0.0121 ms per msg
# Simple Queue x2 250000 30 sec 82323 per/sec 0.0121 ms per msg
# Pipes and queue do not work with numba. Skipped



def worker_pipe_send(conn, msg, iterat):
    for i in range(iterat):
        conn.send(msg)
    conn.send('close')


def worker_pipe_receive(conn):
    while True:
        val = conn.recv()
        if val == 'close':
            break


def worker_queue_send(queue, msg, iterat):
    for i in range(iterat):
        queue.put(msg)
    queue.put('close')


def worker_queue_receeve(queue):
    while True:
        val = queue.get()
        if val == 'close':
            break


def pipe_iter(msg, iterat, is_duplex = True):
    parent_conn, child_conn = multiprocessing.Pipe(duplex = is_duplex)
    p_send = multiprocessing.Process(target=worker_pipe_send, args=(child_conn, msg, iterat))
    p_recive = multiprocessing.Process(target=worker_pipe_receive, args=(parent_conn,))
    p_send.start()
    p_recive.start()
    p_send.join()
    p_recive.join()



def queue_iter(msg, iterat, is_simple = False):
    queue = multiprocessing.SimpleQueue() if is_simple else multiprocessing.Queue()
    p_send = multiprocessing.Process(target=worker_queue_send, args=(queue, msg, iterat))
    p_recive = multiprocessing.Process(target=worker_queue_receeve, args=(queue,))
    p_send.start()
    p_recive.start()
    p_send.join()
    p_recive.join()



def queue_iter_x2(msg, iterat, is_simple = True):
    queue = multiprocessing.SimpleQueue() if is_simple else multiprocessing.Queue()
    iterat = int(iterat/2)
    p_send = multiprocessing.Process(target=worker_queue_send, args=(queue, msg, iterat))
    p_send2 = multiprocessing.Process(target=worker_queue_send, args=(queue, msg, iterat))
    p_recive = multiprocessing.Process(target=worker_queue_receeve, args=(queue,))
    p_recive2 = multiprocessing.Process(target=worker_queue_receeve, args=(queue,))
    p_send.start()
    p_send2.start()
    p_recive.start()
    p_recive2.start()
    p_send.join()
    p_send2.join()
    p_recive.join()
    p_recive2.join()

