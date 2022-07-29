FROM openjdk:11-jdk as base

COPY confluent-community-5.4.0-2.12.zip .

# RUN apk update && apk add --no-cache bash

RUN mkdir -p /usr \
&& unzip confluent-community-5.4.0-2.12.zip -d /usr \
&& rm confluent-community-5.4.0-2.12.zip 

EXPOSE 9092 2181

COPY start-kafka.sh /
RUN chmod +x /start-kafka.sh

CMD ["/bin/bash", "/start-kafka.sh"]

