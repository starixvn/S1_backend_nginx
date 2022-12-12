import hashlib
import subprocess
from urllib import request
from os.path import exists

def check_checksum():

    remote_url = 'https://ailab-config.s3.ap-southeast-1.amazonaws.com/geoblockIp_test.txt'
    blockip = 'geoblockIp_test.txt'
    request.urlretrieve(remote_url, blockip)
    md5_hash = hashlib.md5()

    target = ''
    with open(blockip,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        target = md5_hash.hexdigest()

    origin = ''
    if (exists('checksum')):
        with open('checksum', 'r') as g:
            origin = g.read()

    if target != origin:
        with open('checksum', 'w') as h:
            h.write(target)
        return True
    else:
        return False

def update_block_ip():

    with open('geoblockIp_test.txt', 'r') as txt:
        with open('./conf/sites-multiple/maplist/GeoIPMapListBlockIp.conf', 'w') as config:
            for line in txt:
                config.write('%s;\n' % line.rstrip())

    subprocess.call('nginx -s reload', shell=True)

if __name__ == '__main__':

    if(check_checksum()):
        update_block_ip()
