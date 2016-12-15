
### Installation

Installation process is described here:

Step 1. Execute in command line

```bash
sudo cp -rv htdocs/ /var/www/html/
cd /var/www/html
sudo ln -s htdocs v2
```

Step 2. Permission setting of session folder
```
chgrp www-data /var/www/html/v2/files/session
chmod g+rwx /var/www/html/v2/files/session
```

Step 3. Put following command into browser
```
http:address/index.php?module=install&act=install.php
```

### Reference

* [PC2](http://www.pathwaycommons.org/pcviz/)
* [pertbio](http://www.sanderlab.org/pertbio/)

data visualization

* [Google chart](https://developers.google.com/chart/)
* [VisJS](http://visjs.org/)


data manipulation

* [jsdata](http://learnjsdata.com/)
