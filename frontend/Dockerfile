FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

# 添加 host.docker.internal 支持
RUN apk --no-cache add bash
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"] 