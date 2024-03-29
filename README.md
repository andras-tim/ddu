# ddu
DigitalOcean DNS Updater for Dynamic IP


## Use with Docker
1. Create a `config.json` file (details bellow)
1. Execute the daemon:
    ``` sh
    docker run --rm -ti \
        -v '/path/of/config.json:/srv/ddu/config.json:ro' \
        "ghcr.io/andras-tim/ddu -v
    ```


## Configuration
You can use the `config-example.json` for base.

| Key              | Type          | Description                                                                                           |
|------------------|---------------|-------------------------------------------------------------------------------------------------------|
| `my_ip_host`     | `str`         | Public IP service host                                                                                |
| `my_ip_port`     | `int`         | Public IP service port                                                                                |
| `my_ip_command`  | `str`, `null` | Command/hello string if necessary, otherwise `null`                                                   |
| `retry_s`        | `int`         | Public IP re-check interval                                                                           |
| `dns_token`      | `str`         | Read-write token for [DigitalOcean API](https://cloud.digitalocean.com/account/api/tokens)            |
| `dns_domain`     | `str`         | Top level domain name ([DigitalOcean Networking](https://cloud.digitalocean.com/networking/domains/)) |
| `dns_ttl`        | `int`         | TTL value of the record                                                                               |
| `dns_record_ids` | `List[str]`   | List of DNS record API IDs                                                                            |


*(You can deploy an [andras-tim/my-ip-tcp](https://github.com/andras-tim/my-ip-tcp) instance for public IP service.)*


### List available DNS records
You can use this container for enumerate records with the necessary `dns_record_ids`:
``` sh
   docker run --rm -ti \
       -v '/path/of/config.json:/srv/ddu/config.json:ro' \
       "ghcr.io/andras-tim/ddu --list-records
```
