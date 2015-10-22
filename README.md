# pysnapscan
---

Python bindings for SnapScan's REST API

# Usage

```python
from pysnapscan import utils

ss = utils.get_snapscan('abcd', '8130a729-552d-4eb6-bc3a-726e9c326c1c')
url = ss.generate_qr_code_url()
payments = ss.get_payments()
...
```

