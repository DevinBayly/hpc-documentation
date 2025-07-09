#!/bin/bash

singularity exec --overlay andres_usd_overlay matt_rehme.sif /bin/bash pcap_to_usd.sh $@
#singularity exec --overlay andres_usd_overlay andres.sif /bin/bash pcap_to_usd.sh $@
