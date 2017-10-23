#! python
import socket
import random

def addrToHex(addr):
    div_num = addr.split(".")
    counter = 0
    con_addr = ""

    for number in div_num:
        temp = int(number)

        # Creates a hex address and formats it into the final address
        if temp > 255:
            print("ERROR: INVALID ip (> 255)")
            break
        else:
            if (counter % 2) != 0:
                con_addr += '{:0>2s}'.format(hex(temp)[2::]) + ":"
                counter += 1
            else:
                con_addr += '{:0>2s}'.format(hex(temp)[2::]) + ""
                counter += 1

    return con_addr

def convert6to4(addr):
    FP_TLA = "2002"
    return FP_TLA + ":" + addrToHex(addr) + ":/64"

def convertTeredo(addr, client_addr):
    # The default prefix for Teredo is 2001:000:
    t_prefix = "2001:0000:"

    # Send the server address to the function addToHex to get hexadecimal version
    serv_addr = addrToHex(addr)

    # Windows uses a random 4 bit number in the middle of on of its flags to provide security
    gen = str(bin(random.randint(0, 15)))[2::]
    gen = '{:0>4s}'.format(gen)

    # fl_a is the first half of the address flag
    fl_a = "10" + gen + "00"
    fl_a = hex(int(fl_a, 2))

    # fl_b is the second half of the address flag
    fl_b = str(hex(random.randint(0, 255)))[2::]
    fl_b = '{:0>2s}'.format(fl_b)

    # Remove the '0x' from fl_a and concatenate the two halves of the flag
    flags = str(fl_a)[2::] + str(fl_b)

    if('yes' == input("Do you want to specify the port used(yes or no)? ")):
        # Ask the user if they wish to use a different port than the standard UDP port
        # This is the outgoing port from the user
        used_port = int(input("Enter a desired port (default is 32000): "))
    else:
        used_port = 32000

    if isinstance(used_port, int):
        if used_port > 0 and used_port < 65535:
            used_port = used_port
        else:
            used_port = 32000
    else:
        used_port = 32000

    # As a security feature the port is XORed with 'ffff' to it cannot be read in plain text
    used_port = hex(int(used_port) ^ 0xffff)
    used_port = '{:0>2s}'.format(str(used_port))[2::]

    div_num = client_addr.split(".")
    counter = 0
    con_addr = ""

    # This code is almost the same as in addrToHex but it also XORs each number by 'ff'
    # a standard that provides security for the user's address
    for number in div_num:
        temp = int(number)

        if temp > 255:
            print("ERROR: INVALID ip (> 255)")
            break
        else:
            temp = hex(int(temp) ^ 0xff)
            if (counter % 2) != 0:
                con_addr += '{:0>2s}'.format(str(temp)[2::]) + ":"
                counter += 1
            else:
                con_addr += '{:0>2s}'.format(str(temp)[2::]) + ""
                counter += 1

    return t_prefix + serv_addr + flags + ":" + used_port + ":" + con_addr


address = socket.gethostbyname(socket.gethostname())

# Displays clinet IP
print("Local IP is: " + address)
print("Local host as 6to4 address is: " + convert6to4(address))

cont = "yes"

# Always to continue until client ends the process
while cont == "yes" or cont == "Yes":
    site = input("Type in your favorite website and we will convert it to 6to4 too! ")

    print(site + "'s IPv4 is: " + socket.gethostbyname(site))

    serv_addr = socket.gethostbyname(site)
    print(site + "'s IPv6 in 6to4 is: " + convert6to4(serv_addr))
    print(site + "'s Teredo tunnel is: " + convertTeredo(serv_addr, address))

    # To Exit
    cont = input("Do you want to continue(yes or no)? ")
