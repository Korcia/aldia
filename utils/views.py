#coding=UTF-8
import pywapi

def get_weather():

    codigos = {
            '0':    'Tornado',
            '1': 	'Tormenta tropical',
            '2': 	u'Huracán',
            '3': 	'Tormentas',
            '4': 	'Tormentas',
            '5': 	'Lluvia',
            '6': 	'Aguanieve',
            '7': 	'Aguanieve',
            '8': 	'Llovizna',
            '9': 	'Llovizna',
            '10': 	'Lluvia',
            '11': 	'Chubascos',
            '12': 	'Chubascos',
            '13': 	'Nieve',
            '14': 	'Nieve',
            '15': 	'Nieve',
            '16': 	'Nieve',
            '17': 	'Granizo',
            '18': 	'Aguanieve',
            '19': 	'Polvo',
            '20': 	'Brumas',
            '21': 	'Neblina',
            '22': 	'Niebla',
            '23': 	'Borrascoso',
            '24': 	'Viento',
            '25': 	u'Frío',
            '26': 	'Nublado',
            '27': 	'Nublado',
            '28': 	'Nublado',
            '29': 	'Nublado',
            '30': 	'Nublado',
            '31': 	'Despejado',
            '32': 	'Soleado',
            '33': 	'Despejado',
            '34': 	'Despejado',
            '35': 	'Lluvia',
            '36': 	'Calor',
            '37': 	'Tormentas',
            '38': 	'Tormentas',
            '39': 	'Tormentas',
            '40': 	'Lluvia',
            '41': 	'Nieve',
            '42': 	'Nieve',
            '43': 	'Nieve',
            '44': 	'Nuboso',
            '45': 	'Tormentas',
            '46': 	'Nieve',
            '47': 	'Tormentas',
            '3200': 'No disponible'
        }
    html = [u'<table id="tiempo">\n<thead>\n<tr>\n<th class="fondoamarillo" colspan="4" scope="col">Hoy</th>\n<th class="fondoamarillo" colspan="3" scope="col">Mañana</th>', \
            u'\n</tr>\n<tr>\n<th scope="col">&nbsp;</th>\n<th class="fondoazul" scope="col">Máxima</th>\n<th class="fondoazul" scope="col">Mínima</th>\n', \
            u'<th class="fondoazul" scope="col">El día</th>\n<th class="fondoazul" scope="col">Máxima</th>\n<th class="fondoazul" scope="col">Mínima</th>\n<th class="fondoazul" scope="col">El día</th>\n</tr>', \
            u'\n</thead>\n<tbody>\n']
    yahoo_madrid = pywapi.get_weather_from_yahoo('SPXX0050')
    yahoo_barna = pywapi.get_weather_from_yahoo('SPXX0015')
    yahoo_valencia = pywapi.get_weather_from_yahoo('SPXX0082')
    yahoo_sevilla = pywapi.get_weather_from_yahoo('SPXX0074')
    yahoo_bilbao = pywapi.get_weather_from_yahoo('SPXX0016')
    yahoo_tenerife = pywapi.get_weather_from_yahoo('SPXX0210')
    yahoo_laspalmas = pywapi.get_weather_from_yahoo('SPXX0201')
    yahoo_palma = pywapi.get_weather_from_yahoo('SPXX0061')
    yahoo_lisboa = pywapi.get_weather_from_yahoo('POXX0039')
    yahoo_oporto = pywapi.get_weather_from_yahoo('POXX0022')
    yahoo_bruselas = pywapi.get_weather_from_yahoo('BEXX0005')
    yahoo_berlin = pywapi.get_weather_from_yahoo('GMXX0007')
    yahoo_stuttgart = pywapi.get_weather_from_yahoo('GMXX0128')
    yahoo_frankfurt = pywapi.get_weather_from_yahoo('GMXX0185')
    
    html.append('<tr>\n<td class="letraazul">Madrid</td>\n')
    html.append('<td>')
    html.append(yahoo_madrid['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_madrid['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_madrid['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_madrid['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_madrid['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_madrid['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Barcelona</td>\n')
    html.append('<td>')
    html.append(yahoo_barna['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_barna['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_barna['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_barna['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_barna['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_barna['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Valencia</td>\n')
    html.append('<td>')
    html.append(yahoo_valencia['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_valencia['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_valencia['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_valencia['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_valencia['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_valencia['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Sevilla</td>\n')
    html.append('<td>')
    html.append(yahoo_sevilla['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_sevilla['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_sevilla['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_sevilla['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_sevilla['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_sevilla['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Bilbao</td>\n')
    html.append('<td>')
    html.append(yahoo_bilbao['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_bilbao['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_bilbao['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_bilbao['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_bilbao['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_bilbao['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Tenerife</td>\n')
    html.append('<td>')
    html.append(yahoo_tenerife['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_tenerife['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_tenerife['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_tenerife['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_tenerife['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_tenerife['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Las Palmas</td>\n')
    html.append('<td>')
    html.append(yahoo_laspalmas['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_laspalmas['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_laspalmas['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_laspalmas['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_laspalmas['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_laspalmas['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Palma</td>\n')
    html.append('<td>')
    html.append(yahoo_palma['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_palma['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_palma['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_palma['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_palma['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_palma['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Lisboa</td>\n')
    html.append('<td>')
    html.append(yahoo_lisboa['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_lisboa['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_lisboa['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_lisboa['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_lisboa['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_lisboa['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Oporto</td>\n')
    html.append('<td>')
    html.append(yahoo_oporto['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_oporto['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_oporto['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_oporto['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_oporto['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_oporto['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Bruselas</td>\n')
    html.append('<td>')
    html.append(yahoo_bruselas['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_bruselas['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_bruselas['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_bruselas['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_bruselas['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_bruselas['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append(u'<tr>\n<td class="letraazul">Berlín</td>\n')
    html.append('<td>')
    html.append(yahoo_berlin['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_berlin['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_berlin['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_berlin['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_berlin['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_berlin['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Stuttgart</td>\n')
    html.append('<td>')
    html.append(yahoo_stuttgart['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_stuttgart['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_stuttgart['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_stuttgart['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_stuttgart['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_stuttgart['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('<tr>\n<td class="letraazul">Frankfurt</td>\n')
    html.append('<td>')
    html.append(yahoo_frankfurt['forecasts'][0]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_frankfurt['forecasts'][0]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_frankfurt['forecasts'][0]['code']])
    html.append('</td>\n<td>')
    html.append(yahoo_frankfurt['forecasts'][1]['high'])
    html.append('</td>\n<td>')
    html.append(yahoo_frankfurt['forecasts'][1]['low'])
    html.append('</td>\n<td>')
    html.append(codigos[yahoo_frankfurt['forecasts'][1]['code']])
    html.append('</td>\n</tr>\n')
    
    html.append('</tbody>\n</table>')
    html_string = ''.join(html)
    return html_string