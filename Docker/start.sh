#!/vin/bash

cd image
docker build -t misko/kafka .
cd ..

docker stop kafka1
docker stop kafka2
docker stop kafka3
docker network delete kafkanet
docker rm kafka1
docker rm kafka2
docker rm kafka3

docker network create kafkanet

docker run --name "kafka1" --net=kafkanet --net-alias=kafka1 --env ZK_SERVER_ID=1 -d misko/kafka
docker run --name "kafka2" --net=kafkanet --net-alias=kafka2 --env ZK_SERVER_ID=2 -d misko/kafka
docker run --name "kafka3" --net=kafkanet --net-alias=kafka3 --env ZK_SERVER_ID=3 -d misko/kafka
