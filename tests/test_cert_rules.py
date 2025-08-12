from datetime import date
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.services.cert_rules import dates_overlap


def test_dates_overlap():
    assert dates_overlap(date(2020,1,1), date(2020,1,10), date(2020,1,5), date(2020,1,15))
    assert not dates_overlap(date(2020,1,1), date(2020,1,10), date(2020,1,11), date(2020,1,20))
