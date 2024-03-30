import configparser

class Config():
    _instance = None
    _config = None
    _config_file = None
    _default_postgres_lines_read = 0
    _default_postgres_last_file_read = 1
    _default_mongo_lines_read = 0
    _default_mongo_last_file_read = 1

    def __new__(cls):

        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._config = configparser.ConfigParser()
            cls._config_file = "config.ini"
        return cls._instance
    
    def section_read(self, section_name:str) -> dict:
        """This function reads the content of a specific section from the config file"""

        self._config.read(self._config_file)
        section_data = {}
        if section_name in self._config:
            for key, value in self._config.items(section_name):
                section_data[key] = value
        return section_data
    
    def section_remove(self, section_name):
        """This function removes a specific section from the config file"""

        self._config.remove_section(section_name)
        with open(self._config_file, 'w') as configfile:
            self._config.write(configfile)
    
    def section_add(self, section_name:str):
        """This function adds a specific section to the config file"""

        self._config[section_name] = {}
        with open(self._config_file, 'w') as configfile:
            self._config.write(configfile)

    def option_create_modify(self, section_name:str, option:str, value:str):
        """This function creates or modifies a specific option from the config file"""

        self._config.set(section_name, option, value)
        with open(self._config_file, 'w') as configfile:
            self._config.write(configfile)

    def option_remove(self, section_name:str, option:str):
        """This function removes a specific option from the config file"""

        self._config.remove_option(section_name, option)
        with open(self._config_file, 'w') as configfile:
            self._config.write(configfile)

    @property
    def default_dbs(self):
        return self.section_read("Databases")

    @property
    def default_logs(self):
        return self.section_read("Logs")

    @property
    def default_data(self):
        return self.section_read("Data")

    @property
    def default_memory(self):
        return self.section_read("Memory")

    @property
    def default_postgres_lines_read(self):
        return self._default_postgres_lines_read
    
    @default_postgres_lines_read.setter
    def default_postgres_lines_read(self, value):
        self._default_postgres_lines_read = value

    @property
    def default_postgres_last_file_read(self):
        return self._default_postgres_last_file_read
    
    @default_postgres_last_file_read.setter
    def default_postgres_last_file_read(self, value):
        self._default_postgres_last_file_read = value

    @property
    def default_mongo_lines_read(self):
        return self._default_mongo_lines_read
    
    @default_mongo_lines_read.setter
    def default_mongo_lines_read(self, value):
        self._default_mongo_lines_read = value

    @property
    def default_mongo_last_file_read(self):
        return self._default_mongo_last_file_read
    
    @default_mongo_last_file_read.setter
    def default_mongo_last_file_read(self, value):
        self._default_mongo_last_file_read = value