FROM python:alpine3.20

RUN pip install trollius pyexcel pyexcel-xls pyexcel-xlsx pyyaml modbus_tk coloredlogs
RUN mkdir -p /home/SMARTShip/sim_nmea

COPY . /home/SMARTShip/sim_nmea/


RUN sed -i 's/for ranges in sheet.merged_cells.ranges\[:\]/for ranges in list(sheet.merged_cells.ranges)[:]/' /usr/local/lib/python3.12/site-packages/pyexcel_xlsx/xlsxr.py


WORKDIR /home/SMARTShip/sim_nmea

EXPOSE 9980
EXPOSE 9981
EXPOSE 9982
EXPOSE 9983
EXPOSE 9984
EXPOSE 9985
EXPOSE 9986
EXPOSE 9987
EXPOSE 9988
EXPOSE 9989
EXPOSE 9990
EXPOSE 9991
EXPOSE 9992
EXPOSE 9993
EXPOSE 9994
EXPOSE 9995
EXPOSE 9996
EXPOSE 9997

ENTRYPOINT python __init__.py
