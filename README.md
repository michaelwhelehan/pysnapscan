# pysnapscan
---

Python bindings for SnapScan's REST API

## Features

* Generate QR code URL
* Get Payment(s)
* Create Cashup Period

## Installation

```
git clone https://github.com/michaelwhelehan/pysnapscan.git
cd pysnapscan
python setup.py install
```

## Usage

```python
from datetime import datetime

from pysnapscan.api import SnapScan

SNAPCODE = 'abcd'
API_KEY = '8130a729-552d-4eb6-bc3a-726e9c326c1c'

ss = SnapScan(SNAPCODE, API_KEY)

url = ss.generate_qr_code_url()

payments = ss.get_payments()

cashup_period = ss.create_cash_up_period(datetime.now(), 'adg322sgq3')
...
```

