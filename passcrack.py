import hashlib
import sys
import time

# Supported hashing algorithms
HASH_ALGORITHMS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
}

def crack_hash(hash_to_crack, hash_type, wordlist_path):
    hash_type = hash_type.lower()

    if hash_type not in HASH_ALGORITHMS:
        print(f"[!] Unsupported hash type: {hash_type}")
        return

    spinner = ['|', '/', '-', '\\']
    spin_index = 0

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for count, line in enumerate(file, 1):
                password = line.strip()
                hash_func = HASH_ALGORITHMS[hash_type]()
                hash_func.update(password.encode('utf-8'))
                hashed = hash_func.hexdigest()

                
                sys.stdout.write(f"\r[~] Trying password #{count}: {password[:20]:<20} {spinner[spin_index]}")
                sys.stdout.flush()
                spin_index = (spin_index + 1) % len(spinner)
                time.sleep(0.01)  

                if hashed == hash_to_crack.lower():
                    print(f"\n[+] Password found: {password}")
                    return password
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print("\n[-] Password not found in wordlist.")
    return None

# Example usage
if __name__ == "__main__":
    target_hash = input("Enter the hash to crack: ").strip()
    hash_type = input("Enter the hash type (md5, sha1, sha224, sha256, sha384, sha512): ").strip()
    wordlist_path = input("Enter path to wordlist file: ").strip()

    crack_hash(target_hash, hash_type, wordlist_path)