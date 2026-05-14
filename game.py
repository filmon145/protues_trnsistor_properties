class BahireHasab:
    TINTE_METIK = 49 % 30
    TINTE_ABEKTE = 161 % 30
    WERAT = [
        "Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit",
        "Megabit", "Miyazia", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"
    ]
    WENGELAWI_NAMES = ["Yohannes", "Matewos", "Markos", "Lukas"]
    ELET_TEWSAK = {"Segno": 6, "Maksegno": 5, "Rebu": 4, "Hamus": 3, "Arb": 2, "Kedame": 8, "Ehud": 7}
    ELETAT = ["Kedame", "Ehud", "Segno", "Maksegno", "Rebu", "Hamus", "Arb"]
    BEALAT_TEWSAK = [0, 14, 41, 62, 67, 69, 93, 108, 118, 119, 121]
    BEALAT_NAMES = [
        "Tsome Nenewe", "Abiy Tsom", "Debre Zeyt", "Hosaena", "Siklet", "Tensae",
        "Rkbe Kahnat", "Erget", "Beale Hamsa", "Tsome Hawaryat", "Tsome Dhnet"
    ]

    def __init__(self, year):
        self.year = year
        self.amete_alem = self.year + 5500
        self.medeb_value = self._calculate_medeb()
        self.wenber_value = self._calculate_wenber()
        self.abekte_value = self._calculate_abekte()
        self.metene_rabiet_value = self._calculate_metene_rabiet()
        self.metk_value = self._calculate_metk()
        self.beale_metk_date = self._calculate_beale_metk()
        self.new_year_day = self._calculate_new_year_day()
        self.mebaja_hamer_value = self._calculate_mebaja_hamer()
        self.neneweh_date = self._calculate_neneweh()

    def _calculate_medeb(self) -> int:
        _medeb = self.amete_alem % 19
        return _medeb

    def _calculate_wenber(self) -> int:
        _wenber = self.medeb_value - 1
        return _wenber if self.medeb_value else 18

    def _calculate_abekte(self) -> int:
        _abekte = self.wenber_value * self.TINTE_ABEKTE
        if _abekte > 30:
            _abekte %= 30
        return _abekte if _abekte else 30

    def _calculate_metene_rabiet(self) -> int:
        return self.amete_alem // 4

    def _calculate_metk(self) -> int:
        _m = self.wenber_value * self.TINTE_METIK
        return _m % 30 if _m % 30 else 30

    def _calculate_beale_metk(self) -> str:
        metk = self.metk_value
        if 15 <= metk <= 30:
            return f"Meskerem {metk}"
        elif 2 <= metk <= 14:
            return f"Tikimt {metk}"
        return "Tikimt 30"

    def get_wengelawi(self) -> str:
        return self.WENGELAWI_NAMES[self.amete_alem % 4]

    def get_new_year_day(self) -> str:
        return self.new_year_day

    def get_elete_ken(self, elet_date: str) -> str:
        elet_parts = elet_date.split()
        month_name = elet_parts[0]
        day_number = int(elet_parts[-1])
        atsfe_wer = (self.WERAT.index(month_name) + 1) * 2
        tnete_yon = (self.metene_rabiet_value + self.amete_alem) % 7 - 1
        if tnete_yon < 0:
            tnete_yon += 7
        _day_index = (day_number + tnete_yon + atsfe_wer) % 7
        return self.ELETAT[_day_index]

    def _calculate_new_year_day(self):
        _ = (self.amete_alem + self.metene_rabiet_value + 2) % 7
        return self.ELETAT[_]

    def _calculate_mebaja_hamer(self):
        _beale_metk_day_name = self.get_elete_ken(self.beale_metk_date)
        _mh = self.metk_value + self.ELET_TEWSAK.get(_beale_metk_day_name)
        return _mh

    def get_neneweh_date(self) -> str:
        return self.neneweh_date

    def _calculate_neneweh(self) -> str:
        _mh = self.mebaja_hamer_value
        _neneweh_day = _mh % 30 if _mh % 30 else 30
        _neneweh_month = "Yekatit"
        if _mh > 30:
            _neneweh_month = "Yekatit"
        elif self.metk_value == 30 or self.metk_value == 0:
            _neneweh_month = "Yekatit"
        elif self.beale_metk_date.split()[0] == "Meskerem":
            _neneweh_month = "Tir"
        return f"{_neneweh_month} {_neneweh_day}"

    def get_holiday_date(self, holiday_name: str) -> str:
        try:
            _offset_index = self.BEALAT_NAMES.index(holiday_name)
            _tewsak = self.BEALAT_TEWSAK[_offset_index]
        except ValueError:
            return f"Error: '{holiday_name}' not found in known holidays."

        if _tewsak == 0:
            return self.neneweh_date

        _neneweh_month, _neneweh_day_str = self.neneweh_date.split()
        _neneweh_day = int(_neneweh_day_str)
        _total_days_from_neneweh = _neneweh_day + _tewsak
        _start_month_index = self.WERAT.index(_neneweh_month)
        _new_month_offset = _total_days_from_neneweh // 30
        _new_day = _total_days_from_neneweh % 30

        if _new_day == 0:
            _new_month_index = _start_month_index + _new_month_offset - 1
            _new_day = 30
        else:
            _new_month_index = _start_month_index + _new_month_offset

        _new_month_name = self.WERAT[_new_month_index]
        return f"{_new_month_name} {_new_day}"

    def get_abiy_tsom(self):
        return self.get_holiday_date(holiday_name="Abiy Tsom")

    def get_debre_zeyt(self):
        return self.get_holiday_date(holiday_name="Debre Zeyt")

    def get_hosaena(self):
        return self.get_holiday_date(holiday_name="Hosaena")

    def get_sklet(self):
        return self.get_holiday_date(holiday_name="Siklet")

    def get_tnsae(self):
        return self.get_holiday_date(holiday_name="Tensae")

    def get_rkbe_kahnat(self):
        return self.get_holiday_date(holiday_name="Rkbe Kahnat")

    def get_erget(self):
        return self.get_holiday_date(holiday_name="Erget")

    def get_beale_hamsa(self):
        return self.get_holiday_date(holiday_name="Beale Hamsa")

    def get_tsome_hawaryat(self):
        return self.get_holiday_date(holiday_name="Tsome Hawaryat")

    def get_tsome_dhnet(self):
        return self.get_holiday_date(holiday_name="Tsome Dhnet")

bh = BahireHasab(2019)

print(f"--- Ethiopian Calendar Key Dates for {bh.year} EC ---")
print(f"wengelawi: {bh.get_wengelawi()}")
print(f"New Year's Day ({bh.WERAT[0]} 1): {bh.get_new_year_day()}")
print(f"Beale Metk Date: {bh.beale_metk_date}")

print("\n--- Major Lents and Movable Holidays ---")
for holiday_name in bh.BEALAT_NAMES:
    date = bh.get_holiday_date(holiday_name)
    print(f"{holiday_name}: {date}")
