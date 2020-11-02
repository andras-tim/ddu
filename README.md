# ddu
DigitalOcean DNS Updater for Dynamic IP


## Use with Docker
1. Create a `config.json` file (details bellow)
1. Execute the daemon:
    ``` sh
    docker run --rm -ti \
        -v '/path/of/config.json:/srv/ddu/config.json:ro' \
        andrastim/ddu -v
    ```


## Configuration
You can use the `config-example.json` for base.

| Key              | Type          | Description |
| ---------------- | ------------- | --- |
| `my_ip_url`      | `str`         | Public IP service URL. This will be called by `GET` and expected **JSON** *string* or *dict*. |
| `my_ip_attr`     | `str`, `null` | Key for getting IP from *dict* response or `null` if response is a `string` |
| `check_freq_s`   | `int`         | Public IP check interval |
| `dns_token`      | `str`         | Read-write token for [DigitalOcean API](https://cloud.digitalocean.com/account/api/tokens) |
| `dns_domain`     | `str`         | Top level domain name ([DigitalOcean Networking](https://cloud.digitalocean.com/networking/domains/))  |
| `dns_record_ids` | `List[str]`   | List of DNS record API IDs |


*(You can deploy an [andras-tim/my-ip](https://github.com/andras-tim/my-ip) instance for public IP service.)*


### List available DNS records
You can use this container for enumerate records with the necessary `dns_record_ids`:
``` sh
   docker run --rm -ti \
       -v '/path/of/config.json:/srv/ddu/config.json:ro' \
       andrastim/ddu --list-records
```
