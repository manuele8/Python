for num in range(however_many_nums):
    array_nomi = [f"array_nomi_locanda{num}"]
    array_tipi = [f"array_tipi_locanda{num}"]
    ...

    globals()[f"personaggi_locanda{num}"] = [Personaggio(nomi, tipi, stats[0], stats[1], abilities, deathrattles) for
                                             nomi, tipi, stats, abilities, deathrattles in
                                             zip(array_nomi, array_tipi, array_stats, array_of_abilities,
                                                 array_of_deathrattles)]