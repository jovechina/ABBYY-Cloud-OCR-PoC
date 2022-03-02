import configparser
import os


class EnvVariables:

    @staticmethod
    def get_section_values(sections):
        valid_path = "demo.properties"
        cf = configparser.SafeConfigParser()
        cf.read(valid_path)

        env_variables = {}
        for section in sections:
            for key in cf.options(section):
                val = cf.get(section, key, vars=os.environ)  # use it here
                # print('### [{}] -> {}: {!r}'.format(section, key, val))
                env_variables[key.upper()] = val

        return env_variables


class Headers:
    content_headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }
    content_headers_abbyy = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }


class Endpoint:
    sections = ["APIS"]
    env_variables = EnvVariables.get_section_values(sections)
    abbyy_api = env_variables.get("ABBYY_API")


class Auth:
    auth_sections = ["AUTH"]
    auth_variables = EnvVariables.get_section_values(auth_sections)
    abbyy_appid = auth_variables.get("ABBYY_APPID")
    abbyy_pwd = auth_variables.get("ABBYY_PWD")
