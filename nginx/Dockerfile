FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN sudo apt install certbot python3-certbot-nginx
RUN sudo ufw status
RUN sudo ufw allow 'Nginx Full'
RUN sudo ufw delete allow 'Nginx HTTP'
RUN sudo ufw status
RUN sudo certbot --nginx -d narvon.biz -d www.narvon.biz

