import hashlib

type_of_hash = str(input('Which type of hash do you want to bruteforce?: '))
file_path = str(input('Enter path to the file to bruteforce: '))
hash_to_decrypt = str(input('Enter hash value to bruteforce: '))

with open(file_path, 'r') as file:
    for line in file.readlines():
        if type_of_hash == 'md5':
            hash_object = hashlib.md5(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Found MD5 password: ' + line.strip())
                exit(0)

        if type_of_hash == 'sha1':
            hash_object = hashlib.sha1(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Found SHA1 password: ' + line.strip())
                exit(0)
    print('Password not in file.')



# string_to_md5 = hashlib.md5("encodemystring".encode())
# print(string_to_md5.hexdigest())