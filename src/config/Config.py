import configparser

class Config():
    _instance = None
    _config = None
    _default_lines_read = 0
    _default_sql_doctors = ""
    _default_sql_patients = ""
    _default_sql_medicalrecords = ""
    _default_sql_doctor_medicalrecords = ""

    def __new__(cls):

        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._config = configparser.ConfigParser()
            cls._config.read("config.ini")
        return cls._instance
    
    def read_section(self, section_name:str) -> dict:

        section_data = {}
        if section_name in self._config:
            for key, value in self._config.items(section_name):
                section_data[key] = value
        return section_data

    @property
    def default_dbs(self):
        return self.read_section("Databases")

    @property
    def default_logs(self):
        return self.read_section("Logs")

    @property
    def default_data(self):
        return self.read_section("Data")

    @property
    def default_memory(self):
        return self.read_section("Memory")

    @property
    def default_lines_read(self):
        return self._default_lines_read
    
    @default_lines_read.setter
    def default_lines_read(self, value):
        self._default_lines_read = value

    @property
    def default_sql_doctors(self):
        return self._default_sql_doctors
    
    @default_sql_doctors.setter
    def default_sql_doctors(self, value):
        self._default_sql_doctors = value
    
    @property
    def default_sql_patients(self):
        return self._default_sql_patients
    
    @default_sql_patients.setter
    def default_sql_patients(self, value):
        self._default_sql_patients = value

    @property
    def default_sql_medicalrecords(self):
        return self._default_sql_medicalrecords
    
    @default_sql_medicalrecords.setter
    def default_sql_medicalrecords(self, value):
        self._default_sql_medicalrecords = value
    
    @property
    def default_sql_doctor_medicalrecords(self):
        return self._default_sql_doctor_medicalrecords
    
    @default_sql_doctor_medicalrecords.setter
    def default_sql_doctor_medicalrecords(self, value):
        self._default_sql_doctor_medicalrecords = value