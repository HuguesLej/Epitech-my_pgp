# my_pgp - A song of ciphers and primes

Cryptography is an {Epitech} 3rd year project. It's part of *Computer Numerical Analysis* module.

**⚠️ If you're an Epitech student, be aware that copying any part of this code is considered cheating and would cause an -42!**

## Team

This project was developed by the following team members:
- [HuguesLej](https://github.com/HuguesLej)
- [quentinbol](https://github.com/quentinbol)

## Purpose

The purpose of this project is to implement cryptography algorithms to cipher or decipher data.

The following algorithms must be implemented:
- [XOR](https://en.wikipedia.org/wiki/XOR_cipher)
- [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [RSA](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29)
- PGP-XOR: computation using both RSA and XOR algorithm
- PGP-AES: computation using both RSA and 128-bit AES algorithm

## Constraints

The project has to be developed following one constraint:
all numbers must be represented in [little endian](https://en.wikipedia.org/wiki/Endianness) (the lower byte is on the lower address), including displayed numbers.

## Tests results

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Percentage</th>
      <th>Tests</th>
      <th>Crash ?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Rigor</td>
      <td>75%</td>
      <td>6/8</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Cryptographic rigor</td>
      <td>33.3%</td>
      <td>2/6</td>
      <td>No</td>
    </tr>
    <tr>
      <td>XOR</td>
      <td>100%</td>
      <td>4/4</td>
      <td>No</td>
    </tr>
    <tr>
      <td>XOR - eval</td>
      <td>100%</td>
      <td>8/8</td>
      <td>No</td>
    </tr>
    <tr>
      <td>RSA - Cryptography</td>
      <td>100%</td>
      <td>6/6</td>
      <td>No</td>
    </tr>
    <tr>
      <td>RSA - Cryptography - eval</td>
      <td>100%</td>
      <td>8/8</td>
      <td>No</td>
    </tr>
    <tr>
      <td>RSA - Keygen</td>
      <td>0%</td>
      <td>0/5</td>
      <td>No</td>
    </tr>
    <tr>
      <td>RSA - Keygen - eval</td>
      <td>0%</td>
      <td>0/3</td>
      <td>No</td>
    </tr>
    <tr>
      <td>RSA - Optimization</td>
      <td>0%</td>
      <td>0/2</td>
      <td>No</td>
    </tr>
    <tr>
      <td>AES</td>
      <td>100%</td>
      <td>4/4</td>
      <td>No</td>
    </tr>
    <tr>
      <td>AES - eval</td>
      <td>100%</td>
      <td>8/8</td>
      <td>No</td>
    </tr>
    <tr>
      <td>PGP-XOR</td>
      <td>0%</td>
      <td>0/2</td>
      <td>No</td>
    </tr>
    <tr>
      <td>PGP-XOR - eval</td>
      <td>0%</td>
      <td>0/2</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PGP-AES</td>
      <td>0%</td>
      <td>0/2</td>
      <td>No</td>
    </tr>
    <tr>
      <td>PGP-AES - eval</td>
      <td>0%</td>
      <td>0/2</td>
      <td>No</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th>Total</th>
      <th>65.7%</th>
      <th>46/70</th>
      <th>Yes</th>
    </tr>
  </tfoot>
</table>

## How to use

### Requirements

To use this program, you need to install some tools:
- [Python 3](https://www.python.org/)

### Usage

To compile the executable, run:
```sh
make
```

To clean the execution cache, run:
```sh
make clean
```

To clean both the execution cache and the executable, run:
```sh
make fclean
```

To use the executable, run:
```sh
./my_pgp
```
It will provide help about how to use the program.
The message to cipher/decipher is read from the standard input.

### Examples

Here is an example using the AES algorithm:
```sh
$ echo "I want some soup" > message
$ ./my_pgp aes -c -b 57696e74657220697320636f6d696e67 < message > ciphered
$ cat -e ciphered
aaddb0190c37f3ee69854181e1e7aaee$
$ ./my_pgp aes -d -b 57696e74657220697320636f6d696e67 < ciphered | cat -e
I want some soup$
```
