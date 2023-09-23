class CONSTANTS:
    CHECK_COEFFICIENT = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    CHECK_NUMBER_MAP = {
        i: j
        for i, j in zip(range(0, 11),  [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2])
    }


def main(id_number: int | str) -> bool:
    if len(str(id_number)) != 18:
        raise ValueError(f'{id_number} is not a valid China ID')
    for i in id_number:
        if not i.isdigit() or i.upper() != 'X':
            raise ValueError(f"{id_number} is not a valid China ID, or u don't use the English Letter x for last")

    try:
        id_number = [int(i) for i in str(id_number)]
    except ValueError:
        id_number = [int(i) for i in str(id_number)[:-1]] + ['X']
    check_number = []
    for index in range(17):
        check_number.append(id_number[index] * CONSTANTS.CHECK_COEFFICIENT[index])
    check_number = sum(check_number) % 11
    return CONSTANTS.CHECK_NUMBER_MAP[check_number] == id_number[17]
