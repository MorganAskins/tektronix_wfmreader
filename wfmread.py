#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct as st
import numpy as np

class wfmread:
    '''
    Reads the .wfm binary structure
    for analysis without saving to large
    files
    '''
    def __init__(self, name):
        self.name = name
        self.__read_wfm(name)

    def __read_wfm(self, name):
        with open(name, 'rb') as f:
            self.ending = f.read(2)
            f.seek(11)
            self.bytes_to_eof = st.unpack('i', f.read(4))[0]
            self.point_size = st.unpack('b', f.read(1))[0]
            self.startpoint = st.unpack('i', f.read(4))[0]
            self.curve_bytes = self.bytes_to_eof - self.startpoint
            f.seek(150)
            self.num_curves = st.unpack('i', f.read(4))[0]
            f.seek(168)
            self.dimscale = st.unpack('d', f.read(8))[0]
            self.dimoffset = st.unpack('d', f.read(8))[0]
            f.seek(488)
            self.time_scale = st.unpack('d', f.read(8))[0]
            f.seek(822)
            self.precharge = st.unpack('i', f.read(4))[0]
            self.postcharge = st.unpack('i', f.read(4))[0]
            self.record_length = self.precharge+self.postcharge
            f.seek(self.startpoint)
            wflist = []
            for curves in range(self.num_curves):
                waveform = np.fromstring(f.read(self.record_length), dtype='b')
                waveform = waveform*self.dimscale+self.dimoffset
                wflist.append(waveform)
            self.wflist = np.array(wflist)

    def write_to_npz(self):
        out_name = self.name.rstrip('.wfm')
        time_axis = np.arange(0, self.time_scale*self.record_length, step=self.time_scale)
        np.savez(out_name, voltage=self.wflist, timescale=time_axis)


def main(fname):
    wfm = wfmread(fname)
    wfm.write_to_npz()

if __name__ == '__main__':
    main(sys.argv[1])
