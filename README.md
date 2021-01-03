# 植物溫濕度觀測站
別人的專題。

## Preview

## Features
- 顯示目前觀測數值
- 每 30 分鐘自動記錄數值

## Requirements
- Raspberry Pi
- DHT11/ DHT22
- Python 3.7 and above

## Setup
### Hardware Install
1. 

### Install MariaBD (a.k.a MySql)
1. Install
    ```
    sudo apt update
    sudo apt install mariadb-server
    ```

1. Login to MariaDB (Default password is your RPi's password)
    ```
    sudo mysql -u root -p
    ```

3. Create a user for this project
    ```
    CREATE USER 'dht22'@'localhost' IDENTIFIED BY 'password';
    ```

4. Create DATABASE
    ```
    CREATE DATABASE dht22 CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
    ```

5. Permission 777, wow
    ```
    GRANT ALL PRIVILEGES ON dht22.* TO 'dht22'@'localhost';
    FLUSH PRIVILEGES;
    ```

6. Create TABLE
   ```
   CREATE TABLE `history` (
   `id` INT NOT NULL AUTO_INCREMENT,
   `time` DATETIME NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
   `temp` INT NOT NULL,
   `hum` INT NOT NULL,
   `dirtHum` INT NOT NULL,
   PRIMARY KEY (`id`)
    ) ENGINE=InnoDB;
   ```

### Install the main part
1. Install dependencies
    ```
    pip install -r requirements.txt
    or
    pip3 install -r requirements.txt
    ```

2. Start the server
   ```
   python main.py
   or
   python3 main.py
   ```