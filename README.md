# Buffer Overflow Identify Bad Characters
Python script for identifying bad characters in Buffer Overflow during the stage of shellcode generation.

## Usage Examples
It's a mix of manual and automation to help you identify bad characters faster while minimizing human error. Once you identified a bad character, e.g. '\x09' replaced with '\x00', add '\x09' to the list and remove '\x00' from the dump file. Repeat the process until all bad characters are identified. <br>

![alt text](Images/usage.png)

Watch the video: [demo.mp4](https://github.com/Hein679/CheckBadCharacters/raw/main/demo.mp4)

## Expected Formats
### GDB Debugger Format
![alt text](Images/gdb.png)

### Hex Dump Format
![!\[alt text\](Images/usage.png)](Images/hex_dump.png)