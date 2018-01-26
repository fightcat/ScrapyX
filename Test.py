# -*- coding: utf-8 -*-
import multiprocessing
import time

def proxy(cls_instance, i):
    return cls_instance.func(i)

class Klass(object):
    def __init__(self):
        print ("Constructor ... %s" % multiprocessing.current_process().name)

    def __del__(self):
        print ("... Destructor %s" % multiprocessing.current_process().name)

    def func(self, x):
        print(x * x)

    def run(self):
        pool = multiprocessing.Pool(processes=3)
        for num in range(8):
            #pool.apply_async(self.func, args=(num,))
            pool.apply_async(proxy, args=(self, num,))
            time.sleep(5)
        pool.close()
        pool.join()

if __name__ == '__main__':
    _kls = Klass()
    _kls.run()