FROM ubuntu

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y python-pip python-dev build-essential
#RUN apt install -y snapd
#RUN snap install juju --classic
RUN pip install pyyaml
RUN add-apt-repository -y "deb http://osm-download.etsi.org/repository/osm/debian/ReleaseTHREE stable osmclient openvim"
RUN curl "http://osm-download.etsi.org/repository/osm/debian/ReleaseTHREE/OSM%20ETSI%20Release%20Key.gpg" | apt-key add -
RUN apt update
RUN apt install -y python-osm-im
