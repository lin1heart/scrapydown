# coding=utf-8
import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
from Queue import Queue
from scrapydown.settings import PROXIES
from scrapydown.settings import USER_AGENT

_BE_PROXY_QUEUE = Queue()
path = 'mt_proxy.txt'
ip_proxy = []

class Consumer_Thread(Thread):
    def run(self):
        global _BE_PROXY_QUEUE
        while not _BE_PROXY_QUEUE.empty():
            p = _BE_PROXY_QUEUE.get()
            try:
                if test_useful(p):
                    with open(path, 'r') as f:
                        al = f.read()
                        if al.find(p) ==-1:
                            with open(path, 'a') as f:
                                f.write(p + '\n')
            except Exception, e:
                print '[HERE]', e
                pass
            finally:
                _BE_PROXY_QUEUE.task_done()


def test_useful(proxy):
    print '[INFO] Testing proxy ', proxy, ' now...'
    try:
        proxies = {'http': proxy}
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print '[Congra] Successfully get one'
        return True
    except Exception, e:
        print e
        return False


def get_proxies_from_KDL(max_page):
    global ip_proxy
    print '[Scrapy] Start Scrapying Proxies in KDL'

    base_url = 'http://www.kuaidaili.com/free/'
    options = ['intr/', 'inha/']

    p_pool = []

    print '===============\n', 'Scraping XICI DAILI' '\n===============\n'
    xici_page = 1

    while xici_page <= 3:
        #   xicidaili
        new_count = 0
        print 'PAGE', str(xici_page)
        xici_url = 'http://www.xicidaili.com/nt/' + str(xici_page)
#        iplist=[]
#        proxy_support = request.ProxyHandler({'http':random.choice(iplist)})
#        opener = request.build_opener(proxy_support)
#        opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')]
#        request.install_opener(opener)
        user_agent = random.choice(USER_AGENT)
        print ip_proxy
        ip_li = random.choice(ip_proxy)
        print ip_li
        proxy = {'http': ip_li['ip_port']}
        print proxy
        headers = {'user-agent': user_agent}
        sibs = []
        try:
            rx = requests.get(xici_url, timeout=15, headers=headers, proxies=proxy)
            p = requests.get('http://icanhazip.com', headers=headers, proxies=proxy)#获取真实的当前ip
            print '真的ip', p.text
            print 'proxy is', proxy
            bobj_2 = BeautifulSoup(rx.content.decode('utf-8'))
            sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
        except Exception, e:
            try:
                print 'error 1 proxy is', proxy
                print 'error 1:', e
                print("ZZzzzz...")
                time.sleep(3)
                continue
#                proxy = {'http': ip_li["ip_port"]}
#                headers = {'user-agent': user_agent}
#                rx = requests.get(xici_url, timeout=15, headers=headers, proxies=proxy)
#                p = requests.get('http://icanhazip.com', headers=headers, proxies=proxy)
#                print 'error 真的ip', p.text
#                print 'error 1 proxy is', proxy
#                bobj_2 = BeautifulSoup(rx.content.decode('utf-8'))
#                sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings

            except Exception, e:
                print 'error 2', e
                break

        for sib in sibs:
            try:
                get_proxy = sib.findAll('td')[2].get_text() + ':' + sib.findAll('td')[3].get_text()
                p_pool.append(get_proxy)
                new_count += 1
            except AttributeError:
                pass
        print 'get ', new_count, ' proxies in page', xici_page
        xici_page += 1
    # 第几个分页面
    opt = 0
    while opt <= 1:
        page = 1
        print '===============\n', 'Scraping ', options[opt], '\n===============\n'
        while page < max_page:
            url = base_url + options[opt] + str(page) + '/'
            driver = webdriver.PhantomJS(
                executable_path=r"phantomjs.exe")
            #driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            driver.get(url)
            print 'Sleep 0.7 sec...'
            time.sleep(0.7)
            bobj = BeautifulSoup(driver.page_source)
            driver.close()
            siblings = bobj.findAll(name='table', attrs={'class': 'table table-bordered table-striped'})[
                0].tbody.tr.next_siblings
            count = 0
            for sibling in siblings:
                try:
                    get_proxy = sibling.findAll(name='td')[0].get_text() + ':' + sibling.findAll(name='td')[
                        1].get_text()
                    p_pool.append(get_proxy)
                    count += 1
                except AttributeError:
                    pass
            print 'Get', str(count), 'proxy'
            page += 1
        opt += 1



    print '*****************************'
    print 'Finished! Get ', len(p_pool), ' useful proxies in total'
    return p_pool
    # with open('proxy_kdl.txt', 'w') as f:
    #    for p in p_pool:
    #        p = p + '\n'
    #        f.write(p)
    # print 'Successfully written in \'proxy_kdl.txt\''


def get_proxies_from_file():
    with open('proxy_kdl.txt', 'r') as f:
        return f.readlines()


def test_proxies_efficience(proxy):
    proxies = {'http': proxy}
    start = time.time()
    for i in range(3):
        r = requests.get('http://www.baidu.com', proxies=proxies)
        print i, '  ', r.text
    cost = time.time() - start
    print 'With Proxy: cost ', cost / 3, ' seconds'

    start = time.time()
    for i in range(3):
        r = requests.get('http://ip.cip.cc')
        print i, '  ', r.text
    cost = time.time() - start
    print 'Without Proxy: cost ', cost / 3, ' seconds'

#检查原文件中ip是否可用
#def modifyip(sstr):
#    try:
#        with open(path, 'r') as f:
#            lines = f.readlines()
##        lines = open(path, 'r').readlines()
#        flen = len(lines)
#        for i in range(flen):
#            if sstr in lines[i]:
#                lines[i].remove
#                lines[i] = lines[i].replace(sstr, rstr)
#        open(path, 'w').writelines(lines)
#    except Exception, e:
#        print e

#检查原文件中ip是否可用
def checkip():
    global ip_proxy
    print '===============\n', '检查旧代理ip中', '\n===============\n'
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        flen = len(lines)
        for i in range(flen):
            if i ==0:
                lines[i] = time.ctime()
            if i>=2:
                lines[i] = lines[i].strip()
                if(ip_check(lines[i])):
                    lines[i] = '\n'
            else:
                lines[i] = lines[i].strip()
        for j in range(len(lines)):
            if j>1:
                if lines[j]!='\n':
                    ip_proxy.append({'ip_port': lines[j]})
        with open(path, 'w') as f:
            for i in lines:
                if i !='\n':
                    f.write(i + '\n')
    except Exception, e:
        print e        

def ip_check(proxy):
    proxies = {'http': proxy}
    try:
        res = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
    except:
        print 'connect failed'
        return True
    else:
        print 'success'
        return False

def main():
    # 检查已有的文件
    checkip()
    
#    with open(path, 'w') as f:
#        f.write(time.ctime() + '\n')
#        f.write('========================\n')
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []
    # 2大页面，每个大页面3个分页
    pool = get_proxies_from_KDL(3)
    print 'uher2'
    for i in range(len(pool)):
        _BE_PROXY_QUEUE.put(pool[i])
    for i in range(max_thread):
        threads.append(Consumer_Thread())
    for i in range(max_thread):
        threads[i].start()
    # 陷入等待 线程不够 是因为线程没有死循环就退出
    _BE_PROXY_QUEUE.join()

    print '###########################################'
    print 'SUCCESS!'
    print '###########################################'


if __name__ == '__main__':
    main()
