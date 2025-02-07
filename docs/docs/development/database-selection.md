---
sidebar_position: 3
---
# Choosing a Database

- `sqlite`: Default configuration.
- `mysql`: Best configuration to prevent data loss. You will need to create the database manually and point the configuration files to it.

## MariaDB on Mac

The following commands can be ussed on Mac to install MariaDB.

```
brew install mariadb
sudo mysql_secure_installation
```

```
brew services start mariadb
```

```
brew services stop mariadb
```

### Related Links

- https://mariadb.com/resources/blog/installing-mariadb-10-1-16-on-mac-os-x-with-homebrew/

## MySQL

Just go to the MySQL website and download the installer for your platform.