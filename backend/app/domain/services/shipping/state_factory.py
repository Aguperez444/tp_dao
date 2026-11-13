from app.domain.services.shipping.in_transit import InTransit
from app.domain.services.shipping.prepared import Prepared
from app.domain.services.shipping.received import Received
from app.domain.services.shipping.rejected import Rejected
from app.domain.services.shipping.sealed import Sealed
from app.domain.services.shipping.verified import Verified

STATES = {
    state.name: state
    for state in (Prepared, Sealed, InTransit, Received, Verified, Rejected)
}
