[![Makefile CI process for Github](https://github.com/ant358/text_controller/actions/workflows/devops-github.yml/badge.svg)](https://github.com/ant358/text_controller/actions/workflows/devops-github.yml)

# text_controller

creates the doc nodes in the graph
pulls the neo4j container 


GDS required the manual download of the plugin to the docker volume and the following last 2 neo4j.conf settings
also the neo4j.conf file is in the docker volume

neo4j.conf

db.tx_log.rotation.retention_policy=100M size
server.memory.pagecache.size=512M
server.default_listen_address=0.0.0.0
server.directories.plugins=/plugins
server.directories.logs=/logs
dbms.security.auth_enabled=false
dbms.security.procedures.unrestricted=gds.*
dbms.security.procedures.allowlist=gds.*
