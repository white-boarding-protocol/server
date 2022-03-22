# Overview
This project was implemented as a prototype whiteboard protocol for the course ELEC-E7320 Internet protocols at Aalto University, spring 2022.
## Authors
[Hussam-Aldeen Alkhafaji](https://www.github.com/Sam97ish) <br/>
[Sepehr Javid](https://www.github.com/)<br/>
[Bipin Khatiwada](https://www.github.com/)

# Installation guide
1- First you have to download all the requirements by running:
`sudo pip3 install -r requirements.txt ` <br/>
2- Second you run the server by running:
`python3 main.py`

### Configurations
You can configure the server by setting flags in the `config.json` file.

### Enabling TLS
To enable TLS, you have to set the SSL flag to true in the config file called `config.json`. After that, you have to add the certificate called cert.pem to the CA of your browser (preferably firefox). You can also create your own certificate chain by generating a self-signed certificate as CA and an application certificate to be used by the server.