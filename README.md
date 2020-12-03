# Foscam IP Camera Vulnerability assessment

## Notes
Foscam CGI syntax
Are passwords visible in CGI url?
https://www.foscam.es/descarga/Foscam-IPCamera-CGI-User-Guide-AllPlatforms-2015.11.06.pdf


## Web interface
1. Login not supported over HTTPS. At least not on port 80.
   On port 88 it is http only for logging in.
   Internet explorer is suggested
   Can't connect plugin with Windows 10 -> trying Windows 7
   Windows 7 works with plugin. Still no HTTPS, so we might intercept something.

   There are some known vulerabilities with lighttpd/1.4.49, might be worth to research this.

   > Security, speed, compliance, and flexibility -- all of these describe lighttpd (pron. lighty) which is rapidly redefining efficiency of a webserver; as it is designed and optimized for high performance environments. With a small memory footprint compared to other web-servers, effective management of the cpu-load, and advanced feature set (FastCGI, SCGI, Auth, Output-Compression, URL-Rewriting and many more) lighttpd is the perfect solution for every server that is suffering load problems. And best of all it's Open Source licensed under the revised BSD license. 

   Form does not send credentials with standard http request, must be something else.


2. Nikto results
```
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.178.122
+ Target Hostname:    192.168.178.122
+ Target Port:        88
+ Start Time:         2020-12-02 08:06:46 (GMT-6)
---------------------------------------------------------------------------
+ Server: lighttpd/1.4.49
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ 8735 requests: 7 error(s) and 3 item(s) reported on remote host
+ End Time:           2020-12-02 08:07:54 (GMT-6) (68 seconds)

```


3. Gobuster results
```
Gobuster dir -u http://192.168.178.122:88 -w /usr/share/wordlists/dirb/common.txt

Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.178.122:88
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2020/12/02 08:42:16 Starting gobuster in directory enumeration mode
===============================================================
/cgi-bin              (Status: 301) [Size: 0] [--> http://192.168.178.122:88/cgi-bin/]
/cgi-bin/             (Status: 403) [Size: 345]                                       
/configs              (Status: 301) [Size: 0] [--> http://192.168.178.122:88/configs/]
/css                  (Status: 301) [Size: 0] [--> http://192.168.178.122:88/css/]    
/html                 (Status: 301) [Size: 0] [--> http://192.168.178.122:88/html/]   
/images               (Status: 301) [Size: 0] [--> http://192.168.178.122:88/images/] 
/js                   (Status: 301) [Size: 0] [--> http://192.168.178.122:88/js/]     
/lg                   (Status: 301) [Size: 0] [--> http://192.168.178.122:88/lg/]     
/plugin               (Status: 301) [Size: 0] [--> http://192.168.178.122:88/plugin/] 
                                                                                      
===============================================================
2020/12/02 08:42:26 Finished
===============================================================

```

4. None of these report contain valuable information, unles we can get the portal to work.

5. Nmap Results

```
nmap -sV -sC -A -oN nmap/initial.txt 192.168.178.122

Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-03 03:42 CST
Nmap scan report for 192.168.178.122
Host is up (0.0025s latency).
Not shown: 999 filtered ports
PORT    STATE SERVICE  VERSION
443/tcp open  ssl/http lighttpd 1.4.49
| ssl-cert: Subject: commonName=*.myfoscam.org/organizationName=Shenzhen Foscam Intelligent Technology Co.,Ltd/stateOrProvinceName=Guangdong/countryName=CN
| Subject Alternative Name: DNS:*.myfoscam.org, DNS:myfoscam.org
| Not valid before: 2017-05-31T08:06:15
|_Not valid after:  2020-05-29T08:06:15
|_ssl-date: TLS randomness does not represent time

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 41.97 seconds


nmap -sV -sC -A -p-  -oN nmap/initial.txt 192.168.178.122

Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-03 03:47 CST
Nmap scan report for 192.168.178.122
Host is up (0.0048s latency).
Not shown: 65532 filtered ports
PORT      STATE SERVICE  VERSION
88/tcp    open  http     lighttpd 1.4.49
|_http-server-header: lighttpd/1.4.49
|_http-title: IPCam Client
443/tcp   open  ssl/http lighttpd 1.4.49                                                                       
| ssl-cert: Subject: commonName=*.myfoscam.org/organizationName=Shenzhen Foscam Intelligent Technology Co.,Ltd/stateOrProvinceName=Guangdong/countryName=CN
| Subject Alternative Name: DNS:*.myfoscam.org, DNS:myfoscam.org
| Not valid before: 2017-05-31T08:06:15
|_Not valid after:  2020-05-29T08:06:15
|_ssl-date: TLS randomness does not represent time
34539/tcp open  unknown

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 300.29 seconds

```

## Reverse Engineering Source

1. Does not work, has an SSL Protection on it. Will take 200 years to crack so not an option


## Brute Forcing Web Portal

1. Will only work if we get it to work.
   
   CGI script might be bruteforcable.
   ```
   /cgi-bin/CGIProxy.fcgi?cmd=logIn&usrName=admin&remoteIp=192.168.1.12&groupId=673982479&pwd=&usr=admin&pwd=
   ```

   CGI bruteforcing works
   1. There is no check where request is coming from.
   2. It does not have a delay to slow down bruteforcing
   3. It does not make use of a token whatsoever.



## Intercepting Login Credentials

1. Will work if we can somehow decrypt the traffic
2. Web portal does not have HTTPS login support, so this might be a possibility?

## Command injection
1. Not tried.
2. Webportal makes use of CGI, possible?

## SQL Injection
1. Not tried

## Pretending to be a camera
1. Not tried.
2. We could create a fake login portal, but this is not really a vulnerabilitie issue
3. Possibly intercept credentials with this.

