# Command Line Input Output

Bunch of tools that take input from stdin, do some stuff and give output to stdout, making them perfect for use in piped commands.

For example:

`subfinder -silent -d askubuntu.com|resolves|useshttp -p 80,443 -s success,401|2cmd 2cmd-cutycapt.txt -v`

This command tries to find subdomains of askubuntu.com with subfinder. The subdomains that can be be resolved with DNS are checked if it serves HTTP/HTTPS on ports 80 &443. If the websites found give back a HTTP status code of 2xx or 401, the URLs are taken screenshots of and saved into corresponding files:
* http-askubuntu.com.png
* http-chat.askubuntu.com.png
* https-askubuntu.com.png
* https-www.askubuntu.com.png
* http-www.askubuntu.com.png

`gobuster dir -u scanme.nmap.org -q -w /usr/share/dirb/wordlists/common.txt -e -n -r|2cmd 2cmd-cutycapt.txt -v`

This command tries to enumerated directories on scanme.nmap.org and creates screenshots of the URLs found:

* http-scanme.nmap.org-.hta.png
* http-scanme.nmap.org-.htaccess.png
* http-scanme.nmap.org-.htpasswd.png
* http-scanme.nmap.org-.svn-entries.png
* http-scanme.nmap.org-.svn.png
* http-scanme.nmap.org-images.png
* http-scanme.nmap.org-index.png
* http-scanme.nmap.org-index.html.png
* http-scanme.nmap.org-server-status.png
* http-scanme.nmap.org-shared.png

When combining hakrawler with wappalyzer and wappaligner through the use of 2cmd:
`hakrawler -plain -scope=strict -domain scanme.nmap.org|2cmd ~/.scripts/pipe-tools/2cmd-wappalyzer.txt`

It will give results like these:

* URL = http://scanme.nmap.org/ (HTTP status 200)
* Apache 2.4.7 (100%) - http://apache.org - https://www.google.com/search?q=%22Apache%22%20%222.4.7%22%20cve%20%7Cexploit%20%7Cvulnerability%20%7Cupdates%20%7Cchangelog
* Google AdSense (100%) - https://www.google.fr/adsense/start/ - https://www.google.com/search?q=%22Google%20AdSense%22%20cve%20%7Cexploit%20%7Cvulnerability%20%7Cupdates%20%7Cchangelog
* Google Analytics (100%) - http://google.com/analytics - https://www.google.com/search?q=%22Google%20Analytics%22%20cve%20%7Cexploit%20%7Cvulnerability%20%7Cupdates%20%7Cchangelog
* Ubuntu (100%) - http://www.ubuntu.com/server - https://www.google.com/search?q=%22Ubuntu%22%20cve%20%7Cexploit%20%7Cvulnerability%20%7Cupdates%20%7Cchangelog
