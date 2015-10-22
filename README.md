# pysnapscan
---

Python bindings for SnapScan's REST API

## Todo

* Add tests and test code fully
* Add validators

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

url = ss.generate_qr_code_url(
    uid='1234', # unique identifier for payment
    amount=100, # amount in Rands
    snap_code_size=250, # 50 - 500
    img_type='.svg', # .svg or .png
    strict=True # amount cannot be edited, QR cannot be reused
)

payments = ss.get_payments(
    page=1, # if pagination is needed
    per_page=10,
    offset=0
)

cashup_period = ss.create_cash_up_period(datetime.now(), 'adg322sgq3')
...
```

