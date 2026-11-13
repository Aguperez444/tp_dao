from app.application.dto.commands.address_command import AddressCommand
from app.application.dto.commands.city_command import CityCommand
from app.application.dto.commands.establishment_command import EstablishmentCommand
from app.application.dto.commands.named_command import NamedCommand
from app.application.dto.commands.product_command import ProductCommand
from app.application.dto.commands.supplier_command import SupplierCommand

CatalogCommand = (
    NamedCommand
    | CityCommand
    | AddressCommand
    | EstablishmentCommand
    | SupplierCommand
    | ProductCommand
)
