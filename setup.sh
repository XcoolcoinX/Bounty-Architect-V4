```bash
#!/bin/bash
mkdir -p results
touch targets.txt
docker build -t jaht-station .
docker run -d --name jaht-station -p 8080:5000 -v $(pwd):/home/coder/project jaht-station
echo "Paigaldus valmis. Ava Web Preview pordil 8080 parooliga 1122334455"

```
