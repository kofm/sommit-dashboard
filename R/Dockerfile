FROM rocker/r-ver:4.3

RUN R -e "install.packages(c('FactoMineR'), repos =  'https://packagemanager.posit.co/cran/__linux__/jammy/latest', dependencies=TRUE)"

COPY mfa.R /usr/local/bin/process_data.R

WORKDIR /data

CMD ["Rscript", "/usr/local/bin/process_data.R"]

