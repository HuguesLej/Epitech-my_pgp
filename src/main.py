import sys
import arg_handler as argparse

if __name__ == "__main__":
    args = argparse.parse_arguments()

    if args['MODE'] == '-g':
        message = ''
    else:
        message = sys.stdin.read()

    result = argparse.choose_crypto_system(args, message.strip())

    if result:
        print(result)
