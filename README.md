# Overview
This project was implemented as a prototype whiteboard protocol for the course ELEC-E7320 Internet protocols at Aalto University, spring 2022.
## Authors
[Hussam-Aldeen Alkhafaji](https://www.github.com/Sam97ish) <br/>
[Sepehr Javid](https://www.github.com/sepehrjavid) <br/>
[Bipin Khatiwada](https://www.github.com/bipinkh)

# Installation guide
- Clone the repo
- Run`pip3 install -r requirements.txt ` to install all dependencies
- Run `python3 main.py`

### Configurations
Configure the server by setting flags and values in the `config.json` file.

### Enabling TLS
To enable TLS, set the SSL flag to true in the config file called `config.json`. After that, add the certificate called cert.pem to the CA of your browser (preferably firefox). You can also create your own certificate chain by generating a self-signed certificate as CA and an application certificate to be used by the server.