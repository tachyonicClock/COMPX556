from sc2.ids.unit_typeid import UnitTypeId
import gp

UNIT_MAPPING = {
    gp.Marine: UnitTypeId.MARINE,
    gp.Marauder: UnitTypeId.MARAUDER,
    gp.SiegeTank: UnitTypeId.SIEGETANK
}

PRODUCTION_UNIT = {
    UnitTypeId.MARINE: UnitTypeId.BARRACKS,
    UnitTypeId.MARAUDER: UnitTypeId.BARRACKS,
    UnitTypeId.SIEGETANK: UnitTypeId.FACTORY
}
