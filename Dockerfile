FROM python:3

WORKDIR /usr/src/app

#Cmake
RUN apt-get update && apt-get -y install cmake

#carl
RUN git clone https://github.com/smtrat/carl.git
WORKDIR ./carl 
RUN git checkout master14
RUN mkdir build && cd build && cmake ../ && make 
WORKDIR ../

#PyCarl Dependencies
#RUN apt-get update && apt-get install -y libboost-dev --fix-missing
#apt-get install libboost-all-dev


#PyCarl
#RUN git clone https://github.com/moves-rwth/pycarl.git
#RUN cd pycarl
#python setup.py develop

#RUN pip install -U pytest

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "bash"]