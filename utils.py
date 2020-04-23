def create_reid_dict(tblists):
    """
    Args:
        tblists: a list of lists of tracking boxes
    Returns:
        Dictionary[reid_id] -> List[TrackingBox]
    """
    d = {}
    for cam_id, tblist in enumerate(tblists):
        for tb in tblist:
            if d.get(tb.reid_id) is None:
                d[tb.reid_id] = {}
            d[tb.reid_id][cam_id] = tb
    return d


def refine_tracking_box(tb, mask):
    """
    Removes incorrect data from `TrackingBox` with mask given by
    `ColabImageSelector`.

    Args:
        tb: `TrackingBox` instance mask will applied to
        mask: Iterable[Boolean]
    """
    assert sum(mask) > 0  # at least one data point must be left

    def apply_mask(l, m):
        assert len(l) == len(m)
        return [item for item, mask_value in zip(l, m) if mask_value]

    for attr_name in tb.DATA_LISTS:
        attr = getattr(tb, attr_name)
        setattr(tb, attr_name, apply_mask(attr, mask))
