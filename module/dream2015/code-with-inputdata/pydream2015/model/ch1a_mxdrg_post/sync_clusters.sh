#!/bin/bash
#rsync -avzh --progress ~/dist2 pbs@tesla0:
rsync -avzh --progress --delete ~/dist2 pbs@ras:
rsync -avzh --progress --delete ~/dist2 pbs@raf:
rsync -avzh --progress --delete ~/dist2 pbs@mek:
rsync -avzh --progress --delete ~/dist2 pbs@erk:
rsync -avzh --progress --delete ~/dist2 pbs@darwin:
rsync -avzh --progress --delete ~/dist2 pbs@medusa48:
rsync -avzh --progress --delete ~/dist2 pbs@waddington:
rsync -avzh --progress --delete ~/dist2 pbs@red-queen:

