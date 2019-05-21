import requests
import json
import pickle
from PyQt5 import QtCore


TRADEFLOW = {
    'All': 'all',
    'Import': '1',
    'Export': '2',
    're-Import': '3',
    're-Export': '4',
}

COUNTRY = {
    'All': 'all',
    'World': '0',
    'Afghanistan': '4',
    'Africa CAMEU region, nes': '472',
    'Albania': '8',
    'Algeria': '12',
    'American Samoa': '16',
    'Andorra': '20',
    'Angola': '24',
    'Anguilla': '660',
    'Antarctica': '10',
    'Antigua and Barbuda': '28',
    'Areas, nes': '899',
    'Argentina': '32',
    'Armenia': '51',
    'Aruba': '533',
    'Australia': '36',
    'Austria': '40',
    'Azerbaijan': '31',
    'Bahamas': '44',
    'Bahrain': '48',
    'Bangladesh': '50',
    'Barbados': '52',
    'Belarus': '112',
    'Belgium': '56',
    'Belgium-Luxembourg': '58',
    'Belize': '84',
    'Benin': '204',
    'Bermuda': '60',
    'Bhutan': '64',
    'Bolivia (Plurinational State of)': '68',
    'Bonaire': '535',
    'Bosnia Herzegovina': '70',
    'Botswana': '72',
    'Bouvet Island': '74',
    'Br. Antarctic Terr.': '80',
    'Br. Indian Ocean Terr.': '86',
    'Br. Virgin Isds': '92',
    'Brazil': '76',
    'Brunei Darussalam': '96',
    'Bulgaria': '100',
    'Bunkers': '837',
    'Burkina Faso': '854',
    'Burundi': '108',
    'Cabo Verde': '132',
    'CACM, nes': '471',
    'Cambodia': '116',
    'Cameroon': '120',
    'Canada': '124',
    'Caribbean, nes': '129',
    'Cayman Isds': '136',
    'Central African Rep.': '140',
    'Chad': '148',
    'Chile': '152',
    'China': '156',
    'China, Hong Kong SAR': '344',
    'China, Macao SAR': '446',
    'Christmas Isds': '162',
    'Cocos Isds': '166',
    'Colombia': '170',
    'Comoros': '174',
    'Congo': '178',
    'Cook Isds': '184',
    'Costa Rica': '188',
    "Côte d'Ivoire": '384',
    'Croatia': '191',
    'Cuba': '192',
    'Curaçao': '531',
    'Cyprus': '196',
    'Czechia': '203',
    'Czechoslovakia': '200',
    "Dem. People's Rep. of Korea": '408',
    'Dem. Rep. of the Congo': '180',
    'Denmark': '208',
    'Djibouti': '262',
    'Dominica': '212',
    'Dominican Rep.': '214',
    'East and West Pakistan': '588',
    'Eastern Europe, nes': '221',
    'Ecuador': '218',
    'Egypt': '818',
    'El Salvador': '222',
    'Equatorial Guinea': '226',
    'Eritrea': '232',
    'Estonia': '233',
    'Ethiopia': '231',
    'Europe EFTA, nes': '697',
    'Europe EU, nes': '492',
    'Faeroe Isds': '234',
    'Falkland Isds (Malvinas)': '238',
    'Fiji': '242',
    'Finland': '246',
    'Fmr Arab Rep. of Yemen': '886',
    'Fmr Dem. Rep. of Germany': '278',
    'Fmr Dem. Rep. of Vietnam': '866',
    'Fmr Dem. Yemen': '720',
    'Fmr Ethiopia': '230',
    'Fmr Fed. Rep. of Germany': '280',
    'Fmr Pacific Isds': '582',
    'Fmr Panama, excl.Canal Zone': '590',
    'Fmr Panama-Canal-Zone': '592',
    'Fmr Rep. of Vietnam': '868',
    'Fmr Rhodesia Nyas': '717',
    'Fmr Sudan': '736',
    'Fmr Tanganyika': '835',
    'Fmr USSR': '810',
    'Fmr Yugoslavia': '890',
    'Fmr Zanzibar and Pemba Isd': '836',
    'Fr. South Antarctic Terr.': '260',
    'France': '251',
    'Free Zones': '838',
    'French Guiana': '254',
    'French Polynesia': '258',
    'FS Micronesia': '583',
    'Gabon': '266',
    'Gambia': '270',
    'Georgia': '268',
    'Germany': '276',
    'Ghana': '288',
    'Gibraltar': '292',
    'Greece': '300',
    'Greenland': '304',
    'Grenada': '308',
    'Guadeloupe': '312',
    'Guam': '316',
    'Guatemala': '320',
    'Guinea': '324',
    'Guinea-Bissau': '624',
    'Guyana': '328',
    'Haiti': '332',
    'Heard Island and McDonald Islands': '334',
    'Holy See (Vatican City State)': '336',
    'Honduras': '340',
    'Hungary': '348',
    'Iceland': '352',
    'India': '699',
    'India, excl. Sikkim': '356',
    'Indonesia': '360',
    'Iran': '364',
    'Iraq': '368',
    'Ireland': '372',
    'Israel': '376',
    'Italy': '381',
    'Jamaica': '388',
    'Japan': '392',
    'Jordan': '400',
    'Kazakhstan': '398',
    'Kenya': '404',
    'Kiribati': '296',
    'Kuwait': '414',
    'Kyrgyzstan': '417',
    'LAIA, nes': '473',
    "Lao People's Dem. Rep.": '418',
    'Latvia': '428',
    'Lebanon': '422',
    'Lesotho': '426',
    'Liberia': '430',
    'Libya': '434',
    'Lithuania': '440',
    'Luxembourg': '442',
    'Madagascar': '450',
    'Malawi': '454',
    'Malaysia': '458',
    'Maldives': '462',
    'Mali': '466',
    'Malta': '470',
    'Marshall Isds': '584',
    'Martinique': '474',
    'Mauritania': '478',
    'Mauritius': '480',
    'Mayotte': '175',
    'Mexico': '484',
    'Mongolia': '496',
    'Montenegro': '499',
    'Montserrat': '500',
    'Morocco': '504',
    'Mozambique': '508',
    'Myanmar': '104',
    'N. Mariana Isds': '580',
    'Namibia': '516',
    'Nauru': '520',
    'Nepal': '524',
    'Neth. Antilles': '530',
    'Neth. Antilles and Aruba': '532',
    'Netherlands': '528',
    'Neutral Zone': '536',
    'New Caledonia': '540',
    'New Zealand': '554',
    'Nicaragua': '558',
    'Niger': '562',
    'Nigeria': '566',
    'Niue': '570',
    'Norfolk Isds': '574',
    'North America and Central America, nes': '637',
    'Northern Africa, nes': '290',
    'Norway': '579',
    'Oceania, nes': '527',
    'Oman': '512',
    'Other Africa, nes': '577',
    'Other Asia, nes': '490',
    'Other Europe, nes': '568',
    'Pakistan': '586',
    'Palau': '585',
    'Panama': '591',
    'Papua New Guinea': '598',
    'Paraguay': '600',
    'Peninsula Malaysia': '459',
    'Peru': '604',
    'Philippines': '608',
    'Pitcairn': '612',
    'Poland': '616',
    'Portugal': '620',
    'Qatar': '634',
    'Rep. of Korea': '410',
    'Rep. of Moldova': '498',
    'Rest of America, nes': '636',
    'Réunion': '638',
    'Romania': '642',
    'Russian Federation': '643',
    'Rwanda': '646',
    'Ryukyu Isd': '647',
    'Sabah': '461',
    'Saint Helena': '654',
    'Saint Kitts and Nevis': '659',
    'Saint Kitts, Nevis and Anguilla': '658',
    'Saint Lucia': '662',
    'Saint Maarten': '534',
    'Saint Pierre and Miquelon': '666',
    'Saint Vincent and the Grenadines': '670',
    'Samoa': '882',
    'San Marino': '674',
    'Sao Tome and Principe': '678',
    'Sarawak': '457',
    'Saudi Arabia': '682',
    'Senegal': '686',
    'Serbia': '688',
    'Serbia and Montenegro': '891',
    'Seychelles': '690',
    'Sierra Leone': '694',
    'Sikkim': '698',
    'Singapore': '702',
    'Slovakia': '703',
    'Slovenia': '705',
    'So. African Customs Union': '711',
    'Solomon Isds': '90',
    'Somalia': '706',
    'South Africa': '710',
    'South Georgia and the South Sandwich Islands': '239',
    'South Sudan': '728',
    'Spain': '724',
    'Special Categories': '839',
    'Sri Lanka': '144',
    'State of Palestine': '275',
    'Sudan': '729',
    'Suriname': '740',
    'Swaziland': '748',
    'Sweden': '752',
    'Switzerland': '757',
    'Syria': '760',
    'Tajikistan': '762',
    'TFYR of Macedonia': '807',
    'Thailand': '764',
    'Timor-Leste': '626',
    'Togo': '768',
    'Tokelau': '772',
    'Tonga': '776',
    'Trinidad and Tobago': '780',
    'Tunisia': '788',
    'Turkey': '792',
    'Turkmenistan': '795',
    'Turks and Caicos Isds': '796',
    'Tuvalu': '798',
    'Uganda': '800',
    'Ukraine': '804',
    'United Arab Emirates': '784',
    'United Kingdom': '826',
    'United Rep. of Tanzania': '834',
    'United States Minor Outlying Islands': '581',
    'Uruguay': '858',
    'US Misc. Pacific Isds': '849',
    'US Virgin Isds': '850',
    'USA': '842',
    'USA (before 1981)': '841',
    'Uzbekistan': '860',
    'Vanuatu': '548',
    'Venezuela': '862',
    'Viet Nam': '704',
    'Wallis and Futuna Isds': '876',
    'Western Asia, nes': '879',
    'Western Sahara': '732',
    'Yemen': '887',
    'Zambia': '894',
    'Zimbabwe': '716'
}


def repaintText(object, message):
    object.append(message)
    QtCore.QCoreApplication.processEvents()


def getUNCodeList():
    code_all = list()
    code_6 = list()
    url = 'https://comtrade.un.org/Data/cache/classificationHS.json'
    res = requests.get(url=url)
    if res.status_code == 200:
        uncomtrade = json.loads(res.text)['results']
        for i in uncomtrade:
            try:
                int(i['id'])
                code = i['id']
                code_all.append(code)
                if len(code) == 6:
                    code_6.append(code)
            except:
                pass
        f = open('code_all.pkl', 'wb')
        pickle.dump(code_all, f)
        f = open('code_6.pkl', 'wb')
        pickle.dump(code_6, f)
        message = 'Update UN Comtrade list.'
    else:
        message = 'Get UN Comtrade list error.\nCode is {}.\nContent is {}.'.format(res.status_code, res.text)
    return message


def getUNComtradeLen():
    f = open('code_all.pkl', 'rb')
    code_all = len(pickle.load(f))
    f = open('code_6.pkl', 'rb')
    code_6 = len(pickle.load(f))
    if code_all == 0 or code_6 == 0:
        message = 'HS Code list is none, please update HS Code.'
    else:
        message = 'HS Code All is {}.\nHS Code 6 is {}.'.format(code_all, code_6)
    return (code_all, code_6, message)


def getData(params, index, text_message):
    url = 'https://comtrade.un.org/api/get'
    data = dict()
    f = open('code_all.pkl', 'rb')
    code_list = pickle.load(f)
    for i in range(int(index), len(code_list), 20):
        params['cc'] = code_list[i:i+20]
        repaintText(text_message, 'Request data index {}, HS codes {}'.format(i, params['cc']))
        try:
            res = requests.get(url=url, params=params)
            dataset = json.loads(res.text)['dataset']
            if res.status_code == 200 and i <= 200:
                for j in dataset:
                    desc = j['rgDesc']
                    code = j['cmdCode']
                    data[code] = {
                        desc: j,
                    }
                    repaintText(text_message, 'Get code {} {} data.'.format(code, desc))
                repaintText(text_message, '\n')
            else:
                repaintText(text_message, 'Error, else condition.\nindex is {}, status is {}, content is {}\n'.format(i, res.status_code, res.text))
                return data
        except Exception as e:
            repaintText(text_message, 'Except, index is {}, status is {}, content is {}\n'.format(i, res.status_code, res.text))
            return data
    return data


def getParams(year, index, token, reporter, partner, trade_flow):
    params = {
        'max': 500,
        'type': 'C',
        'freq': 'A',
        'px': 'HS',
        'ps': year,
        'r': COUNTRY.get(reporter),
        'p': COUNTRY.get(partner),
        'rg': TRADEFLOW.get(trade_flow),
        'uitoken': token,
    }
    return params


def checkInput(**kwargs):
    message = str()
    for key, value in kwargs.items():
        if len(value) == 0:
            message += 'Please input {}.\n'.format(key)
        else:
            if key != 'Token':
                try:
                    int(value)
                except Exception as e:
                    message += 'Please input {} as number.\n'.format(key)
    if len(message) > 0:
        return (False, message)
    else:
        return (True, message)


def checkSelect(**kwargs):
    message = str()
    for key, value in kwargs.items():
        if value == 'None':
            message += 'Please select {}.\n'.format(key)
    if len(message) > 0:
        return (False, message)
    else:
        return (True, message)
