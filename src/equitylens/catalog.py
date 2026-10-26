"""Instrument identity is independent of the data provider and UI."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    symbol: str
    name: str
    sector: str
    exchange: str = "NSE"
    currency: str = "INR"
    country: str = "IN"

    @property
    def key(self) -> str:
        return f"{self.exchange}:{self.symbol}"


# A demo universe, not a claim of current listing status or provider coverage.
INSTRUMENTS = (
    Instrument("RELIANCE", "Reliance Industries", "Diversified"),
    Instrument("TCS", "Tata Consultancy Services", "Information technology"),
    Instrument("INFY", "Infosys", "Information technology"),
    Instrument("HDFCBANK", "HDFC Bank", "Banking"),
    Instrument("ICICIBANK", "ICICI Bank", "Banking"),
    Instrument("ITC", "ITC", "Consumer goods"),
    Instrument("LT", "Larsen & Toubro", "Engineering"),
    Instrument("SUNPHARMA", "Sun Pharmaceutical Industries", "Healthcare"),
    Instrument("TITAN", "Titan Company", "Consumer discretionary"),
    Instrument("MARUTI", "Maruti Suzuki India", "Automotive"),
)


def search_instruments(query: str = "") -> tuple[Instrument, ...]:
    query = query.strip().casefold()
    return tuple(i for i in INSTRUMENTS if query in f"{i.symbol} {i.name} {i.sector}".casefold())


def get_instrument(key: str) -> Instrument:
    for instrument in INSTRUMENTS:
        if instrument.key == key:
            return instrument
    raise ValueError(f"Unsupported instrument: {key}")
