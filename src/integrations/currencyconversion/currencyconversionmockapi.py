from src.contracts.currencyconversion.currencyconversionapi import CurrencyConversionApi
from decimal import Decimal

# Example class
class CurrencyConversionMockApi(metaclass=CurrencyConversionApi):
    validCurrencies = ['USD', 'BRL', 'EUR', 'BTC', 'ETH']

    def __init__(self):
        pass

    def convert(self, conversionRequest):
        # Simulated response with currencies based on google's currency conversion 2019-08-04
        response = {
            "success": True,
            "terms": "https://currencylayer.com/terms",
            "privacy": "https://currencylayer.com/privacy",
            "timestamp": 1432400348,
            "source": 'USD',
            "quotes": {
                'USDUSD': 1,
                'USDBRL': 3.89,
                'USDEUR': 0.9,
                'USDBTC': 0.000088,
                'USDETH': 0.0044
            }
        }

        from_ = conversionRequest['from']
        to = conversionRequest['to']
        amount = conversionRequest['amount']

        # HERE, we can't directly convert using a free subscription because the 'from' parameter MUST be 'USD'.
        # So a simple alternative is to use some algebra in case from_ is not 'USD' ;)
        # On the other hand, when 'to' is USD, we need only to revert the opperand
        quotes = response['quotes']

        returnAmount = None
        # Simple conversion
        if to == 'USD':
            returnAmount = Decimal(amount) / Decimal(quotes[to + from_])

        elif from_ == 'USD':
            returnAmount = Decimal(amount) * Decimal(quotes[from_ + to])

        # Algebra
        else:
            fromQuote = quotes['USD' + from_]
            toQuote = quotes['USD' + to]

            returnAmount = Decimal(amount) * (Decimal(toQuote) / Decimal(fromQuote))

        # TODO: extract to helper function
        SIXPLACES = Decimal(10) ** -6

        return returnAmount.quantize(SIXPLACES)
