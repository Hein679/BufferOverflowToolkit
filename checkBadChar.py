import subprocess

# Set the bad characters to an empty list
bad_chars = []

# Iterate through all possible ASCII characters
for i in range(256):
  # Construct a test payload with a single character ch at position i
  payload = hex(i)
  print("checking ", payload)

  # Use the subprocess module to run the exec executable with the test payload as the argument
  try:
    subprocess.run(['./leave_msg', payload], check=True)
  except subprocess.CalledProcessError:
    # If the exec command returns a non-zero exit code, it means that the payload was not successful
    # This means that the character is a bad character, so we add it to the list
    bad_chars.append(chr(i))

# Print the list of bad characters
print(bad_chars)
