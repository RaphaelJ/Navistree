#!/usr/bin/python
#-*- coding: Utf-8 -*-

import navistree, db, template

HTTPD_HOME = navistree.GENERATED + "/httpd"
HTTPD_HOSTS = HTTPD_HOME + "/hosts.conf"

ADMIN_EMAIL = "{username}@navistree.org"
#ADMIN_EMAIL = "{username}@{domain}"

class Httpd:
    def __init__(self, db=db.Connection()):
        self.db = db

    def close(self):
        self.db.close()

    def gen_hosts(self):
        """ Génère la liste des hôtes virtuelles d'Apache """
        cur = self.db.cursor()
        cur.execute("""SELECT d.domain, d.path, u.username, d.domain
            FROM domains AS d
            INNER JOIN users AS u
                ON u.id = d.user_id
            UNION
            SELECT h.hostname || '.' || d.domain, h.path,
                u.username, d.domain
            FROM hosts AS h
            INNER JOIN domains AS d
                ON d.id = h.domain_id
            INNER JOIN users AS u
                ON u.id = d.user_id""")

        for host in cur:
            server_name = host[0]
            
            # folders can't stop with a / with apache
            document_root = host[1].rstrip('/')
            
            owner = host[2]
            top_level_domain = host[3]

            tpl = template.Template("virtual_host")
            tpl.replace({
                "server_name": server_name,
                "document_root": document_root,
                "server_admin": ADMIN_EMAIL.format(username=owner,
                    domain=top_level_domain)
            })

            yield (server_name, tpl)

        cur.close()

    def write_hosts(self):
        """ Ecrit la liste des hôtes """
        with open(HTTPD_HOSTS, 'w') as hosts_list:
            for host in self.gen_hosts():
                host[1].write(dest_file=hosts_list)

if __name__ == "__main__":
    d = Httpd()
    d.write_hosts()
    d.close()