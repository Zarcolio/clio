# Command Line Input Output

Bunch of tools that take input from stdin, do some stuff and give output to stdout, making them perfect for use in piped commands.

For example:

*subfinder -silent -d askubuntu.com|resolves|useshttp -p 80,443,8443 -s success,403,401|2cmd 2cmd-cutycapt.txt -v*

This command tries to find subdomains of askubuntu.com with subfinder. The subdomains that can be be resolved with DNS are checked if it serves HTTP/HTTPS on ports 80,443 & 8443. If the websites found give back a HTTP status code of 2xx, 403 or 401, the URLs are taken screenshots of and saved into corresponding files:
* http-askubuntu.com.png
* http-chat.askubuntu.com.png
* https-askubuntu.com.png
* https-www.askubuntu.com.png
* http-www.askubuntu.com.png

*gobuster dir -u scanme.nmap.org -q -w /usr/share/dirb/wordlists/common.txt -e -n -r|2cmd 2cmd-cutycapt.txt -v*

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

