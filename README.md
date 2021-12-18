

## Enabling Authentication in MongoDB

### 1. Create the user administrator

Change to the **admin** database:

```
use admin
```



You need to create a user with the [**userAdminAnyDatabase**](https://docs.mongodb.com/manual/reference/built-in-roles/#userAdminAnyDatabase) role, which grants the privilege to create other users on any existing database. The following example will create the **admin** user with password “**nothing**”:

```shell
> db.createUser(
  {
    user: "admin",
    pwd: "nothing",
    roles: [ { role: "root", db: "admin" } ]
  }
)
```



### 2. Enable authentication in mongod configuration file

update `mongod.conf` 

```shell
security:
    authorization: "enabled"
```

then restart `mongod`.



## Creating Service

Copy file `cims.service` under `python-server/linux-service` to `/etc/systemd/system/`

```
sudo cp ./python-server/linux-service/cims.service /etc/systemd/system/cims.service 
```

Now give executable permissions to `cims` under `python-server/linux-service`

```
sudo chmod u+x ./linux-service/cims
```



### Starting the Service

```
sudo systemctl daemon-reload
sudo systemctl enable olb.service
sudo systemctl start olb
sudo systemctl status olb
```



### Checking logs

```
sudo journalctl -f --unit=olb 
```