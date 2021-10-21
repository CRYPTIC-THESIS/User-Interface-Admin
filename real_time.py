from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import calendar
cg = CoinGeckoAPI()

def get_cur():
    d = datetime.utcnow()
    t = datetime.utcnow() - timedelta(days = 1 )
    u_d = calendar.timegm(d.utctimetuple())
    u_t = calendar.timegm(t.utctimetuple())

    b = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp=u_t,to_timestamp=u_d)
    btc = b.get('prices')
    btc = [val[1] for val in btc]
    btc_c = btc[-1]
    btc_h = max(btc)
    btc_l = min(btc)

    e = cg.get_coin_market_chart_range_by_id(id='ethereum',vs_currency='usd',from_timestamp=u_t,to_timestamp=u_d)
    eth = e.get('prices')
    eth = [val[1] for val in eth]
    eth_c = eth[-1]
    eth_h = max(eth)
    eth_l = min(eth)

    d = cg.get_coin_market_chart_range_by_id(id='dogecoin',vs_currency='usd',from_timestamp=u_t,to_timestamp=u_d)
    dog = d.get('prices')
    dog = [val[1] for val in dog]
    dog_c = dog[-1]
    dog_h = max(dog)
    dog_l = min(dog)

    data = [btc_c,btc_h,btc_l,eth_c,eth_h,eth_l,dog_c,dog_h,dog_l]
    return data
