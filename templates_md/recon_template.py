
def get_recon_template():
    return '''Template

---

## Nmap Summary
| Port | Software    | Version                                 | Status  |
| ---- | ----------- | --------------------------------------- | ------- |
| 53   | domain      | Simple DNS                              | open    |
| 80   | http        | Apache http 2.4.29                      | open    |
| 139  | netbios-sec | Microsfot Windows netbios-ssn           | open    |
| 389  | ldap        | Microsoft Windows Active Directory LDAP | open    |


## Information Recon

Ports tcp open in nmap format

```bash

```

Ports services and versions nmap format

```bash

```

Ports UDP nmap format

```bash

```

---

## Enumeration

## Port 80 - HTTP (Apache)



---

'''
    