
def serialize_exchange_diff(diff):
    if diff > 0:
        return f'({diff}{EMOJI_UP})'
    elif diff < 0:
        return f'({abs(diff)}{EMOJI_DOWN})'
    return ''

def get_exchange_diff(last, now):
    return {
       'sale_diff': round(float(now['sale']) - float(last['sale']), 6),
       'buy_diff': round(float(now['buy']) - float(last['buy']), 6)
    }


# CCY is an abbreviation for the word, "currency."  Therefore, CCY = Currency.
# For Example: 50 CCY means 50 units of the base currency of your credit/debit card.


def serialize_ex(ex_json, diff=None):
    result = f'''<b>{ex_json['base_ccy']} -> {ex_json['ccy']}:</b>\n\nBuy: {ex_json['buy']}'''
    if diff:
        result += f''' {serialize_exchange_diff(diff['buy_diff'])}\nSell: {ex_json['sale']} {serialize_exchange_diff(diff['sale_diff'])}\n'''
    else:
        result += f"\nSell: {ex_json['sale']}\n"
    return result
