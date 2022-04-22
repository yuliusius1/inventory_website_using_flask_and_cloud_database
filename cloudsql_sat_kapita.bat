@ECHO OFF
:: Menjalankan cloud sql proxy sat kapita
TITLE Cloud SQL Proxy Sat Kapita
ECHO Jangan di close selama proses ini berlangsung
"cloud_sql_proxy_x64" -instances=sat-kapita-selekta-b:asia-southeast2:training-kapita-selekta=tcp:5433
