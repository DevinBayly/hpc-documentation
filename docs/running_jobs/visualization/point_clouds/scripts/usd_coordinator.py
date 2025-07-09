import subprocess as sp
from pathlib import Path

pcaps = list(Path().rglob("*pcap"))

for pcap in pcaps:
  sp.run(f'sbatch -A visteam -t 2:00:00 -n 8 -N 1 -p standard usd_coordinator.sh "{pcap}" "{pcap.parent}/{pcap.stem}.json" usd_creator.py source_mapping.py',shell=True)
  #sp.run(f"sbatch -A visteam -t 1:00:00 -n 8 -N 1 -p standard coordinator.sh",shell=True)
