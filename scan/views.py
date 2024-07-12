import subprocess
from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm

def ping_to_target(target_ip):
    try:
        ping = subprocess.run(['ping', '-c', '1', target_ip], stdout=subprocess.PIPE, universal_newlines=True)
        output = ping.stdout
        if "1 packets transmitted, 1 received" in output:
            return True
        else:
            return False
    except Exception as e:
        return False

def port_check(target_ip, target_port):
    try:
        command = f"echo | timeout 1 bash -c 'cat > /dev/tcp/{target_ip}/{target_port}' 2>&1"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = result.stdout
        if 'Connection refused' not in output:
            return True
        else:
            return False
    except Exception as e:
        return False

def scan_ports(target_ip, ports):
    open_ports = []
    for port in ports:
        if port_check(target_ip, port):
            open_ports.append(port)
    return open_ports

def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            ports = form.cleaned_data['ports']
            if not ports:
                ports = range(1, 65536)
            else:
                port_list = []
                for port in ports.split():
                    if '-' in port:
                        start, end = map(int, port.split('-'))
                        port_list.extend(range(start, end + 1))
                    else:
                        port_list.append(int(port))
                ports = port_list

            if ping_to_target(ip_address):
                open_ports = scan_ports(ip_address, ports)
                return render(request, 'scan/result.html', {'ip_address': ip_address, 'open_ports': open_ports})
            else:
                return render(request, 'scan/result.html', {'ip_address': ip_address, 'error': 'IP address is NOT Accessible'})
    else:
        form = InputForm()
    return render(request, 'scan/index.html', {'form': form})
