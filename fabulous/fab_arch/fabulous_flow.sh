#!/usr/bin/env bash
set -ex
yosys -p "tcl ../synth/synth_fabulous_dffesr.tcl 4 ${1} ${1}.json" ${1}.v -l ${1}_yosys_log.txt
sed 's/sequential_16bit/'${1}'/g' bitstream_temp.py>bitstream.py
${NEXTPNR:-../../nextpnr-fabulous} --pre-pack fab_arch.py --pre-place fab_timing.py --json ${1}.json --router router2 --router2-heatmap ${1}_heatmap --post-route bitstream.py --write pnr${1}.json --verbose --log ${1}_npnr_log.txt
python3 bit_gen.py -genBitstream ${1}.fasm meta_data.txt ${1}_output.bin

mkdir -p heatmap/wire/${1}
mv *heatmap*.csv heatmap/wire/${1}
