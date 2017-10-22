# an attempt at recreating stepmania's sm file parser.
# hashtag reinventing the wheel!
# for these purposes, I really don't need to parse the steps. so I'll focus on NOT those.
# these purposes = cutie chaser

# it looks like they have a file wrapper (surprise [eyeroll])
# that has a couple of helper functions.
# MsdFile is the type/class name - actually it really lays out the whole format...

import argparse
import re


class NotesData(object):
    def __init__(self, data):
        # data in the style of the colon delimited values after NOTES in .sm file
        # I do not expect there to be any different numbers of values
        self.style = data[0]
        self.step_artist = data[1]
        self.difficulty = data[2]
        self.level = data[3]
        self.radar = data[4].split(',')
        self.notes = data[5]


def parse_sm(smfile_path):
    with open(smfile_path, 'r') as smfile:
        contents = smfile.read()
        # regExplanation: match whatever's after the #,
        # allow it to span multiple lines, except NOT past another # or ;
        # This probably isn't optimal.
        params = re.findall('#(.*(?:\n[^#;]*)*[^#;]*);', contents, flags=re.MULTILINE)
        values = [item.split(':') for item in params]

        smdata = {}
        for value in values:
            key = value[0]
            data = value[1:]
            if key == 'NOTES':
                if key not in smdata:
                    smdata[key] = []
                smdata[key].append(NotesData(data))
            elif key in ['BPMS', 'STOPS', 'BGCHANGES', 'KEYSOUNDS']:
                data = data[0].strip() # We assume there is only one colon-delimited value
                smdata[key] = {
                        item.split('=')[0]: item.split('=')[1]
                        for item in data.split(',')
                        if data
                        }
            else:
                smdata[key] = data[0].strip()

        return smdata


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sm_path')
    args = parser.parse_args()

    smdata = parse_sm(args.sm_path)
    print(smdata)
