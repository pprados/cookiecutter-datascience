# ce dockerfile décrit l'environnement minimum
# à installer sur une machine ubuntu pour
# fonctionner le simulateur_ironcar
FROM ubuntu:latest

# tzdata ask region confirmation, use UTC
RUN apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata &&\
    apt-get install -y libopencv-dev &&\
    apt-get install -y povray &&\
    apt-get install -y python3 &&\
    apt-get install -y python3-pip
