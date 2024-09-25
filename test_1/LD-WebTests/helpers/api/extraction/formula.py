def get_formula_names(ldclient, lr_id):
    """
    Get names of formulae present in LR

    :param ldclient: LDClient, ldclient object
    :param lr_id: str, ID of LiveReport

    :return:list, list of formula names in LR
    """
    return ldclient.list_formulas_by_live_report_id(lr_id)
