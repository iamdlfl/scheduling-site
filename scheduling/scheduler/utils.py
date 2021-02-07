def sort_positions(sorting_item):
    # To use in sorting the shifts so they are always in Driver -> Cashier -> Bagger order
    return sorting_item.split(' ')[2]