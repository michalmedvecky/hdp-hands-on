FROM spotify/kafka

COPY zoo.cfg /etc/zookeeper/conf/zoo.cfg
COPY zkServer.sh /usr/share/zookeeper/bin/zkServer.sh
COPY start-kafka.sh /usr/bin/start-kafka.sh
RUN chmod +x /usr/share/zookeeper/bin/zkServer.sh
RUN chmod +x /usr/bin/start-kafka.sh

