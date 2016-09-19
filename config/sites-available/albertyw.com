### Redirects ###

# Change IP address to domain name
server {
    server_name     $server_addr;
    add_header      X-Frame-Options "SAMEORIGIN";
    return          301 https://www.albertyw.com$request_uri;
}

server {
    listen          80;
    server_name     _; # catch-all
    rewrite         ^ https://www.albertyw.com$request_uri;
}

# Change naked domain to www
server {
    listen          443 spdy;
    server_name     albertyw.com;

    ssl on;
    ssl_protocols               TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers                 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_prefer_server_ciphers   on;
    ssl_session_cache           shared:SSL:10m;
    ssl_session_timeout         10m;
    ssl_certificate             /etc/nginx/ssl/1_albertyw.com_bundle.crt;
    ssl_certificate_key         /etc/nginx/ssl/server.key;
    ssl_dhparam                 /etc/nginx/ssl/dhparams.pem;

    rewrite         ^ https://www.albertyw.com$request_uri;
}


### Servers ###

server {
    listen          443 spdy;
    server_name     www.albertyw.com;
    access_log      /var/log/nginx/website.access.log;
    error_log       /var/log/nginx/website.error.log;

    ssl on;
    ssl_protocols               TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers                 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_prefer_server_ciphers   on;
    ssl_session_cache           shared:SSL:10m;
    ssl_session_timeout         10m;
    ssl_certificate             /etc/nginx/ssl/1_albertyw.com_bundle.crt;
    ssl_certificate_key         /etc/nginx/ssl/server.key;
    ssl_dhparam                 /etc/nginx/ssl/dhparams.pem;

    gzip on;
    gzip_disable "msie6";

    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript;

    # static files used for the website
    location /static {
        alias        "/var/www/website/app/static/";
        try_files $uri.html $uri $uri/ =404;
        expires     7d;
        add_header Cache-Control "public";
    }

    location / {
        uwsgi_pass      unix://tmp/website.sock;
        include         uwsgi_params;
        uwsgi_param     UWSGI_SCHEME $scheme;
        uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;
        expires     7d;
        add_header Cache-Control "public";
    }
}
