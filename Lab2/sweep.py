import re
import subprocess
from io import StringIO
import matplotlib.pyplot as plt

loss = re.compile(r'Loss: (\d+.\d+)')

ks = list(range(2, 16))
losses = []
for k in ks:
    proc = subprocess.Popen(['python', 'mdav.py', '--file', 'Tarragona.csv', '--k', str(k)], stdout=subprocess.PIPE)
    for line in proc.stdout:
        content = line.decode().strip()
        match = loss.match(content)
        if match:
            losses.append(float(match.group(1)))

plt.title('Utility vs Anonymity')
plt.xlabel('k')
plt.ylabel('Loss')
plt.ylim(0, 0.5)
plt.plot(ks, losses)
plt.show()
