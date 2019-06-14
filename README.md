# igb-geonode


## Installation

This repo is a geonode-project. It can be installed in the usual way, with some
specific tweaks related to concrete system and python dependencies:

-  Install LDAP system libraries

   ```bash
   
   sudo apt install \
       libldap2-dev \
       libsasl2-dev
   
   ```
   
-  Install GeoNode - Refer to [the new GeoNode installation docs][1]

-  Install the `geonode_ldap` contrib package - Refer to its [README][2] for installation details

-  Get this repo's code and pip install it

   ```bash
   git clone https://github.com/geosolutions-it/igb-geonode.git
   cd igb-geonode
   pip install --requirement requirements/production.txt
   pip install --editable .
   ```
   
-  Configure GeoServer, PostgreSQL, etc by following the instructions on the
   GeoNode pages.
   

[1]: http://docs.geonode.org/en/new-docs/install/core/index.html#geonode-installation
[2]: https://github.com/GeoNode/geonode-contribs/blob/master/ldap/README.md
