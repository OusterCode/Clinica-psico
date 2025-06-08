# Funções utilitárias para validações e CEP
import re
import requests

def is_valid_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        check = ((value * 10) % 11) % 10
        if check != int(cpf[i]):
            return False
    return True

def is_valid_phone(phone):
    return re.match(r'^\(?[1-9]{2}\)? ?9[1-9][0-9]{3}\-?[0-9]{4}$', phone)

def get_address_by_cep(cep):
    cep = re.sub(r'[^0-9]', '', cep)
    if len(cep) != 8:
        return None
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return {
                    'address': data.get('logradouro', ''),
                    'city': data.get('localidade', ''),
                    'state': data.get('uf', '')
                }
    except Exception:
        pass
    return None
