import sys
import os
import ruamel.yaml
import json
from collections import defaultdict

data = defaultdict(lambda: [0, 0])
fileset = set()

def handle_file(fn):
    if fn in fileset:
        return
    fileset.add(fn)
    yaml = ruamel.yaml.YAML()
    with open(fn, 'r') as fd:
        for x in yaml.load_all(fd):
            if x.get('Pass', None) != 'hwasan' or x.get('Name', None) != 'ignoreAccess':
                continue
            data[fn + ':' + x['Function']][x.tag == '!Passed'] += 1

if __name__ == '__main__':
    for root, dirs, files in os.walk(sys.argv[1]):
        for filename in files:
            if not filename.endswith('yaml'):
                continue
            handle_file(os.path.join(root, filename))
            print('.', end='')
            sys.stdout.flush()
    with open('result.json', 'w') as fd:
        json.dump(data, fd)

