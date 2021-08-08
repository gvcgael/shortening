
Install :
```
python3 -m venv shortening_env
source ./shortening_env/bin/activate
pip3 install -r requirements.txt
```

Unit tests :
```
PYTHONPATH=src py.test tests/
```

Run the server : 
```
PYTHONPATH=src python3 -m shortener
```

Run the vegeta tests :
```
python3 vegeta_data.py | vegeta attack -duration=300s -rate 10 | tee results.bin | vegeta report
Requests      [total, rate, throughput]         3000, 10.00, 10.00
Duration      [total, attack, wait]             5m0s, 5m0s, 1.357ms
Latencies     [min, mean, 50, 90, 95, 99, max]  820.602µs, 1.842ms, 2.01ms, 2.354ms, 2.604ms, 3.301ms, 4.802ms
Bytes In      [total, mean]                     46893, 15.63
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:3000  
Error Set:

```