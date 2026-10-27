"""Read-only remote evidence collector, run via SSH stdin; emits sanitized JSON only.
No writes, SDK calls, hardware configuration, credentials, or full config export.
"""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import subprocess

out = {"captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "files": {}, "commands": []}
base = Path('/usr/share/sonic/device/x86_64-cel_seastone_2-r0')

def record(path, transform=lambda text: text):
    p = Path(path)
    raw = p.read_bytes()
    result = {"source_sha256": hashlib.sha256(raw).hexdigest(), "evidence": transform(raw.decode())}
    out['files'][str(p)] = result
    return result

def selected_lines(pattern):
    return lambda text: [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if re.search(pattern, line)]

def command(args):
    r = subprocess.run(args, capture_output=True, text=True, timeout=15)
    out['commands'].append({'argv': args, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
    return r.stdout

for name in ('default_sku', 'Seastone_2/port_config.ini', 'Seastone_2/hwsku.json', 'platform.json', 'SONIX/port_config.ini'):
    record(base / name)
for name in ('SONIX/td3-seastone_2-32x100G-vxlan.config.bcm', 'Seastone_2/td3-seastone_2-32x100G-vxlan.config.bcm', 'Seastone_2/td3-seastone_2-32x100G.config.bcm'):
    record(base / name, selected_lines(r'^portmap_'))
record(base / 'SONIX/sai.profile', selected_lines(r'^SAI_(INIT_CONFIG_FILE|NUM_ECMP_MEMBERS)='))
record(base / 'plugins/sfputil.py', lambda text: [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if 14 <= i <= 20 or 46 <= i <= 51 or 63 <= i <= 68 or 77 <= i <= 80 or 91 <= i <= 95])
record('/host/machine.conf', selected_lines(r'^onie_(platform|machine|arch|vendor_id|machine_rev)='))
record('/etc/sonic/sonic_version.yml', selected_lines(r'^(build_version|asic_type|debian_version|kernel_version|build_date):'))

def config_subset(text):
    d = json.loads(text)
    m = d.get('DEVICE_METADATA', {}).get('localhost', {})
    return {'DEVICE_METADATA': {k: m[k] for k in ('platform', 'hwsku', 'type', 'switch_type') if k in m},
            'PORT': {name: {k: v for k, v in props.items() if k in ('alias', 'index', 'lanes', 'speed', 'valid_speeds', 'fec', 'admin_status')} for name, props in d.get('PORT', {}).items()}}
record('/etc/sonic/config_db.json', config_subset)
record('/proc/modules', selected_lines(r'^(linux_.*(bcm|knet|bde))'))

def knet_subset(text):
    result = []
    for block in text.split('My Station: ')[1:]:
        entry = {'name': block.split()[0]}
        for key in ('port', 'phys_port', 'type', 'flags'):
            m = re.search(r'^\s*' + key + r'\s*=\s*(\S+)', block, re.M)
            if m:
                entry[key] = m.group(1)
        result.append(entry)
    return result
record('/proc/bcm/knet/ndev', knet_subset)
record('/sys/class/seastone2_fpga/SFP1/sfp_modabs')
command(['hostname'])
command(['uname', '-srm'])
command(['systemctl', 'is-active', 'docker', 'swss', 'syncd'])
command(['docker', 'ps', '--format', '{{.Names}} {{.Image}}'])
command(['sonic-db-cli', 'ASIC_DB', 'HGETALL', 'ASIC_STATE:SAI_OBJECT_TYPE_HOSTIF:oid:0xd00000000067e'])
command(['sonic-db-cli', 'ASIC_DB', 'HGET', 'ASIC_STATE:SAI_OBJECT_TYPE_PORT:oid:0x1000000000014', 'SAI_PORT_ATTR_HW_LANE_LIST'])
command(['sonic-db-cli', 'ASIC_DB', 'HGET', 'ASIC_STATE:SAI_OBJECT_TYPE_PORT:oid:0x1000000000014', 'SAI_PORT_ATTR_SPEED'])
print(json.dumps(out, indent=2, sort_keys=True))
