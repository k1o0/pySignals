# pySignals
Signals in Python

## Running
```python
import signals as sig

net = sig.Net()  # Create new network
o = net.origin('input')  # Create input signal
s = o + 2  # Derive signal from input

o.post(2)  # Post to input signal
print(s.node.get_value())  # 4
```

## Tests
```
cd pySignals/signals
python -m unittest discover
```
