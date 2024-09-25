from library.api.extended_ldclient.base import LDEnum


class OrderType(LDEnum):
    """
    Determines the strategy for which enumeration results are generated
    """
    SEQUENTIAL = "sequential"
    RANDOM = "random"


class ReactionProductFilterType(LDEnum):
    MOLECULAR_WEIGHT = "molecular_weight"
    NUMBER_ROTATABLE_BONDS = "number_rotatable_bonds"
    NUMBER_H_BOND_ACCEPTORS = "number_h_bond_acceptors"
    NUMBER_H_BOND_DONORS = "number_h_bond_donors"
    MOLECULAR_LOG_P = "molecular_log_p"
    POLAR_SURFACE_AREA = "polar_surface_area"
    RING_COUNT = "ring_count"
    NUMBER_AROMATIC_RINGS = "number_aromatic_rings"


class ReactionInputSourceType(LDEnum):
    SCHRODINGER_COLLECTION = "schrodinger_collection"
    USER_DEFINED = "user_defined"


class StartupHookStatus(LDEnum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
