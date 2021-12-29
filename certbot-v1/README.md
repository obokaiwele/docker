# Certbot

## Inspiration:
- https://github.com/thecarlo/letsencrypt-docker-nginx/tree/master/src/letsencrypt
- https://getbootstrap.com/docs/4.5/getting-started/introduction/#starter-template
- https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx

## Start Server
```bash
sudo docker-compose -p certbot up

cd /home/ubuntu/certbot/docker
source ./.env
sudo docker run -it --rm -v /home/ubuntu/certbot/docker/letsencrypt/etc/:/etc/letsencrypt/ -v /home/ubuntu/certbot/docker/letsencrypt/var/lib/:/var/lib/letsencrypt/ -v /home/ubuntu/certbot/docker/letsencrypt/var/log/:/var/log/letsencrypt/ -v /home/ubuntu/certbot/docker/www/:/var/www/html/public/ certbot/certbot certonly --webroot --register-unsafely-without-email --agree-tos --webroot-path=/var/www/html/public/ --staging -d $DOMAIN -d www.$DOMAIN

```
