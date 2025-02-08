
two_dp = '{:,.2f}'
three_dp = '{:,.3f}'
no_dp = '{:,.0f}'


def format_title_price(price):
    price_format = no_dp if price > 100 else two_dp if price > 10 else three_dp
    return price_format.format(price)

def human_format(num:float, force=None, ndigits=3):
    perfixes = ('p', 'n', 'u', 'm', '', 'K', 'M', 'G', 'T')
    one_index = perfixes.index('')
    if force:
        if force in perfixes:
            index = perfixes.index(force)
            magnitude = 3*(index - one_index)
            num = num/(10**magnitude)
        else:
            raise ValueError('force value not supported.')
    else:
        div_sum = 0
        if(abs(num) >= 1000):
            while abs(num) >= 1000:
                div_sum += 1
                num /= 1000
        else:
            while abs(num) <= 1:
                div_sum -= 1
                num *= 1000
        temp = round(num, ndigits) if ndigits else num
        if temp < 1000:
            num = temp 
        else:
            num = 1
            div_sum += 1
        index = one_index + div_sum
    return str(num).rstrip('0').rstrip('.') + perfixes[index]

def format_scale_price(num, pos):

    if num < 1:
        return "{:.3f}".format(num).lstrip('0')

    if num < 10:
        return "{:.2f}".format(num)

    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    magnitude_char = ['', 'K', 'M', 'B', 'T'][magnitude]
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), magnitude_char)
