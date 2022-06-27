<h1 align="center">
  Secure Console Chat App
</h1>

## About

This is a simple application written in python made for university work. It uses python socket, threads and a encryption package. It uses client-server architecture.

## Features

* Private messages
  * Send private messages to your friends.
* Friends list
    * Add friends.
* Encryption
  * End to end encrypted messaging with [fernet](https://github.com/pyca/cryptography).

## Usage

To run this program you will need [git](https://git-scm.com/), [python](https://www.python.org/), [cryptography](https://github.com/pyca/cryptography). On your console:

```bash
# Clone the repository
git clone https://github.com/alinategh-js/secure-console-chat.git
# Go inside the folder
cd secure-console-chat
# Install dependencies
pip install cryptography
# run the server
py server.py
```
Now that you have an instance of the server running, you can open another terminal and run multiple clients:

```bash
# run a client
py client.py
```