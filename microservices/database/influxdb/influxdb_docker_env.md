[influxdb docker link](https://hub.docker.com/_/influxdb)

**Environment Variables**     
The InfluxDB image uses several environment variables to automatically configure certain parts of the server. They may significantly aid you in using this image.

**INFLUXDB_DB**   
Automatically initializes a database with the name of this environment variable.

**INFLUXDB_HTTP_AUTH_ENABLED**      
Enables authentication. Either this must be set or auth-enabled = true must be set within the configuration file for any authentication related options below to work.

**INFLUXDB_ADMIN_USER**       
The name of the admin user to be created. If this is unset, no admin user is created.

**INFLUXDB_ADMIN_PASSWORD**   
The password for the admin user configured with INFLUXDB_ADMIN_USER. If this is unset, a random password is generated and printed to standard out.

**INFLUXDB_USER**       
The name of a user to be created with no privileges. If INFLUXDB_DB is set, this user will be granted read and write permissions for that database.

**INFLUXDB_USER_PASSWORD**    
The password for the user configured with INFLUXDB_USER. If this is unset, a random password is generated and printed to standard out.

**INFLUXDB_READ_USER**  
The name of a user to be created with read privileges on INFLUXDB_DB. If INFLUXDB_DB is not set, this user will have no granted permissions.

**INFLUXDB_READ_USER_PASSWORD**     
The password for the user configured with INFLUXDB_READ_USER. If this is unset, a random password is generated and printed to standard out.

**INFLUXDB_WRITE_USER**       
The name of a user to be created with write privileges on INFLUXDB_DB. If INFLUXDB_DB is not set, this user will have no granted permissions.

**INFLUXDB_WRITE_USER_PASSWORD**    
The password for the user configured with INFLUXDB_WRITE_USER. If this is unset, a random password is generated and printed to standard out.

**Initialization Files**      
If the Docker image finds any files with the extensions .sh or .iql inside of the /docker-entrypoint-initdb.d folder, it will execute them. The order they are executed in is determined by the shell. This is usually alphabetical order.

**Manually Initializing the Database**    
To manually initialize the database and exit, the /init-influxdb.sh script can be used directly. It takes the same parameters as the influxd run command. As an example:

>$ docker run --rm \
      -e INFLUXDB_DB=db0 \
      -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=supersecretpassword \
      -e INFLUXDB_USER=telegraf -e INFLUXDB_USER_PASSWORD=secretpassword \
      -v $PWD:/var/lib/influxdb \
      influxdb /init-influxdb.sh

The above would create the database db0, create an admin user with the password supersecretpassword, then create the telegraf user with your telegraf's secret password. It would then exit and leave behind any files it created in the volume that you mounted.