class sqlite(object):
    def __init__(self):
        self.db = sqlite3.connect("pool.db")
        self.c = self.db.cursor()
    
    def insertdb(self, ip, port):
        #OP, SOP = 0
        PCOL = ""
        self.c.execute(
            'select IP from proxy where IP = ?', (ip,)
        )
        result = self.c.fetchone()
        if result is not None:
            if result[0] == ip:
                print "IP already exist"
            else:
                self.c.execute(
                    "insert into proxy(IP,Port,OnlinePoint,HTTP,SOPoint,HTTPS) values(?,?,?,?,?,?)", (ip, port, 0, PCOL, 0, PCOL)
                )
                self.db.commit()
        else:
            self.c.execute(
                    "insert into proxy(IP,Port,OnlinePoint,HTTP,SOPoint,HTTPS) values(?,?,?,?,?,?)", (ip, port, 0, PCOL, 0, PCOL)
                )
            self.db.commit()

    def allip(self):
        self.c.execute(
            "select * from proxy"
        )
        return self.c.fetchall()

    def closedb(self):
        self.c.close()

    def uphttppoint(self, id, point):
        self.c.execute(
            "UPDATE proxy SET OnlinePoint=? where ID=?", (point, id)
        )
        self.db.commit()
    
    def uphttpspoint(self, id, point):
        self.c.execute(
            "UPDATE proxy SET SOPoint=? where ID=?", (point, id)
        )
        self.db.commit()

    def point(self, id):
        self.c.execute(
            "select OnlinePoint from proxy where ID=?", (int(id),)
        )
        return self.c.fetchone()

    def protocol(self, id, pcol):
        if pcol == "HTTP":
            self.c.execute(
                "UPDATE proxy SET HTTP=? where ID=?", (pcol, id)
            )
        elif pcol == "HTTPS":
            self.c.execute(
                "UPDATE proxy SET HTTPS=? where ID=?", (pcol, id)
            )
        self.db.commit()