import requests
import hashlib
import sys

# fetches the data from the api 
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('there is a problem')
    return res

# changes the reponse to text and counts how many times the pass exist 
def pass_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# it hashes the given password to SHA1 AND REQUEST API DATA then seperates it for safety
def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5)
    return pass_count(response, tail)


def main(args):
     for password in args:
         count = pwned_api_check(password)
         if count:
             print(f'your password {password} was found and hacked {count} times. you should use another one')
         else:
            print(f'Your password {password} was not found it is save to use')


main(sys.argv[1:])