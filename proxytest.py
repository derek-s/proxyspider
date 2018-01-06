class proxytest(object):
    def __init__(self):
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.urlhttps = "https://www.baidu.com/"
        self.urlhttp = "http://bj.ganji.com/"
    
    def ip_list(self):
        proxydb = sqlite()
        ipportlist = proxydb.allip()
        proxydb.closedb()
        self.test(ipportlist)
    
    def test(self, iplist):
        proxydb = sqlite()
        for info in iplist:
            ipid = info[0]
            ipaddr = info[1]
            port = info[2]
            proxyip = str(ipaddr)+":"+str(port)
            httpprox = {
                "http": proxyip
            }
            httpsprox = {
                "https": proxyip
            }
            try:
                print 'HTTP tesing: ' + proxyip
                r = requests.get(self.urlhttp, proxies=httpprox, timeout=3)
                code = r.status_code
                if code == 200:
                    print code
                    point = proxydb.point(ipid)
                    proxydb.uphttppoint(ipid, str(int(point[0])+1))
                    proxydb.protocol(ipid, "HTTP")
            except Exception as e:
                print "Not Support HTTP"
                point = proxydb.point(ipid)
                proxydb.uphttppoint(ipid, str(int(point[0])-1))
            try:
                print 'HTTPS tesing: ' + proxyip
                r = requests.get(self.urlhttps, proxies=httpsprox, timeout=3)
                code = r.status_code
                print code
                if code == 200:
                    point = proxydb.point(ipid)
                    proxydb.uphttpspoint(ipid, str(int(point[0])+1))
                    proxydb.protocol(ipid, "HTTPS")
            except Exception as e:
                print "Not Support HTTPS"
                point = proxydb.point(ipid)
                proxydb.uphttppoint(ipid, str(int(point[0])-1))