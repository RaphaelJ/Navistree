#!/usr/bin/python
#-*- coding: Utf-8 -*-

import datetime, urllib
import navistree, db, template

PUBLIC_IP_SERVICE = "http://87.98.147.3/public/ip.php"
SERVER_HOST = "navistree.no-ip.org"

NS1 = "navistree.no-ip.org"
NS2 = "rapha222.dyndns.org"
TTL = 10800 # 3h
ADMIN_EMAIL = "{username}.navistree.org"
#ADMIN_EMAIL = "{username}.{domain}"

DOMAINS_HOME = navistree.GENERATED + "/named"
NAMED_DOMAINS_LIST = DOMAINS_HOME + "/named.domains.conf"
ZONES_HOME = DOMAINS_HOME + "/zones"
ZONES = ZONES_HOME + "/named.{domain}.zones"

HOST_RECORD = "{hostname}	IN	CNAME	{server_host}."
#HOST_RECORD = "{hostname}	IN	A	{server_ip}"

class Named:
    _public_ip = None

    def __init__(self, db=db.Connection()):
        self.db = db

    def close(self):
        self.db.close()

    @property
    def public_ip(self):
        """ Donne l'IP accessible depuis l'extérieur """
        if self._public_ip == None:
            self._public_ip = urllib.urlopen(PUBLIC_IP_SERVICE).read()
        return self._public_ip

    def gen_domains(self):
        """ Génère la liste des déclarations des domaines """
        def current_serial():
            """ Génère le numéro de série du domaine """
            return datetime.datetime.now().strftime("%Y%m%d%H")

        def gen_hosts_records(domain_id):
            """ Génère la liste des enregistrements des hôtes d'un domaine """
            cur_hosts = self.db.cursor()
            cur_hosts.execute("""SELECT hostname
                FROM hosts
                WHERE domain_id = %(domain_id)s""", {
                    "domain_id":domain_id
                })

            for host in cur_hosts:
                hostname = host[0]

                yield HOST_RECORD.format(hostname=hostname,
                    server_host=SERVER_HOST,
                    server_ip=self.public_ip)

            cur_hosts.close()

        cur_doms = self.db.cursor()
        cur_doms.execute("""SELECT d.id, d.domain, u.username
            FROM domains AS d
            INNER JOIN users AS u
                ON u.id = d.user_id""")

        serial = current_serial()

        for dom in cur_doms:
            dom_id = dom[0]
            dom_name = dom[1]
            dom_owner = dom[2]

            # Génère la liste des domaines
            tpl_decl = template.Template("domain")
            tpl_decl.replace({
                "domain": dom_name,
                "zone": ZONES.format(domain=dom_name)
            })

            # Génère les zones
            tpl_zone = template.Template("zone")
            tpl_zone.replace({
                "domain": dom_name,
                "TTL": TTL,
                "admin_email": ADMIN_EMAIL.format(username=dom_owner,
                    domain=dom_name),
                "serial": serial,
                "ns1": NS1,
                "ns2": NS2,
                "server_ip": self.public_ip,
                "hosts": '\n'.join(gen_hosts_records(dom_id))
            })

            yield (dom_name, tpl_decl, tpl_zone)

        cur_doms.close()

    def write_domains(self):
        """ Ecrit la liste des domaines et les zones """
        with open(NAMED_DOMAINS_LIST, 'w') as domains_list:
            for dom in self.gen_domains():
                dom[1].write(dest_file=domains_list)

                zone_filename = ZONES.format(domain=dom[0])
                dom[2].write(zone_filename)

if __name__ == "__main__":
    d = Named()
    d.write_domains()
    d.close()