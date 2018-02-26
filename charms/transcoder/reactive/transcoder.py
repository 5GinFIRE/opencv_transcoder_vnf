from charmhelpers.core.hookenv import (
    action_fail,
    action_get,
    action_set,
    config,
    status_set,
)
from charms.reactive import when, set_state, remove_state
import charms.sshproxy

cfg = config()


@when('config.changed')
def config_changed():
    err = ''
    try:
        cmd = "echo '' | sudo tee -a /etc/network/interfaces.d/50-cloud-init.cfg > /dev/null && "
        cmd += "echo 'auto ens4' | sudo tee -a /etc/network/interfaces.d/50-cloud-init.cfg > /dev/null && "
        cmd += "echo 'iface ens4 inet dhcp' | sudo tee -a /etc/network/interfaces.d/50-cloud-init.cfg > /dev/null && "
        cmd += "sudo timeout 5 ifup ens4"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: ' + err)
    else:
        set_state('transcoder.configured')
        status_set('active', 'ready!')


@when('transcoder.configured')
@when('actions.start-transcoder')
def start_transcoder():
    stream_ip = action_get('stream-ip')
    output_port = action_get('output-port')

    err = ''
    try:
        cmd = "sudo rm /etc/systemd/system/opencv.service >/dev/null 2>&1; "
        cmd += "sudo systemctl stop opencv.service >/dev/null 2>&1; "
        cmd += "sudo systemctl daemon-reload"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: ' + err)
        remove_state('actions.start-transcoder')
        return

    err = ''
    try:
        cmd = "echo '[Unit]' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'Description=OpenCV' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo '' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo '[Service]' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'Type=simple' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'User=ubuntu' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'WorkingDirectory=/home/ubuntu' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'ExecStart=/usr/bin/python live_server.py {0} {1}' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && ".format(stream_ip, output_port)
        cmd += "echo 'Restart=always' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'RestartSec=5' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo '' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo '[Install]' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "echo 'WantedBy=multi-user.target' | sudo tee -a /etc/systemd/system/opencv.service > /dev/null && "
        cmd += "sudo systemctl daemon-reload && "
        cmd += "sudo systemctl start opencv.service"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: ' + err)
    else:
        action_set({'output': result, 'errors': err})
    finally:
        remove_state('actions.start-transcoder')
