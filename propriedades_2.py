# Nome do arquivo: propriedades_2.py
# Autor: Maurício Fernandes de Oliveira Assis
# Versão do Python: 3.12.1

import CoolProp.CoolProp as CP

def allPropriedades(substancia, propriedade1, propriedade2, op1, op2):
    try:
        propriedades = ['P', 'T', 'V', 'U', 'H', 'S', 'Q']
        prop1_convertido = propriedade1
        prop2_convertido = propriedade2
        lista_resultado = []
        liquidos = []
        vapores = []
        for propriedade in propriedades:
            
            if propriedade == 'V':
                propriedade = 'D'

                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S':
                    prop1 = prop1_convertido * 1000
                elif op1 == 'T':
                    prop1 = prop1_convertido + 273.15

                elif op1 == 'Q':
                    prop1 = prop1_convertido

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    prop2 = prop2_convertido * 1000

                elif op2 == 'T':
                    prop2 = prop2_convertido + 273.15

                elif op2 == 'Q':
                    prop2 = prop2_convertido

                propriedadeEncontrada = 1/CP.PropsSI(propriedade, op1, prop1, op2, prop2, substancia)
                fase = CP.PhaseSI(op1, prop1, op2, prop2, substancia)
                lista_resultado.append(propriedadeEncontrada)

                

                if fase == 'twophase':
                    liquido = 1/CP.PropsSI(propriedade, op1, prop1, 'Q', 0, substancia)
                    liquidos.append(liquido)

                    vapor = 1/CP.PropsSI(propriedade, op1, prop1, 'Q', 1, substancia)
                    vapores.append(vapor)


            elif propriedade == 'Q':
                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S':
                    prop1 = prop1_convertido * 1000
                elif op1 == 'T':
                    prop1 = prop1_convertido + 273.15

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    prop2 = prop2_convertido * 1000
                elif op2 == 'T':
                    prop2 = prop2_convertido + 273.15

                propriedadeEncontrada = CP.PropsSI(propriedade, op1, prop1, op2, prop2, substancia)
                liquido = None
                vapor = None


            else:
                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S':
                    prop1 = prop1_convertido * 1000
                elif op1 == 'T':
                    prop1 = prop1_convertido + 273.15

                elif op1 == 'Q':
                    prop1 = prop1_convertido

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    prop2 = prop2_convertido * 1000

                elif op2 == 'T':
                    prop2 = prop2_convertido + 273.15

                elif op2 == 'Q':
                    prop2 = prop2_convertido

                propriedadeEncontrada = CP.PropsSI(propriedade, op1, prop1, op2, prop2, substancia)
                fase = CP.PhaseSI(op1, prop1, op2, prop2, substancia)

                if propriedade in ['P', 'U', 'H', 'S']:
                    propriedadeEncontrada = propriedadeEncontrada / 1000  # Convertendo para kJ/kg
                    lista_resultado.append(propriedadeEncontrada)

                elif propriedade == 'T':
                    propriedadeEncontrada = propriedadeEncontrada - 273.15  # convertendo para Celsius
                    lista_resultado.append(propriedadeEncontrada)

                
                print(fase)
                if fase == 'twophase':
                    if op1 == 'Q':
                        liquido = CP.PropsSI(propriedade, op2, prop2, 'Q', 0, substancia) / 1000
                        liquidos.append(liquido)

                        vapor = CP.PropsSI(propriedade, op2, prop2, 'Q', 1, substancia) / 1000
                        vapores.append(vapor)

                    elif op2 == 'Q':
                        liquido = CP.PropsSI(propriedade, op1, prop1, 'Q', 0, substancia) / 1000
                        liquidos.append(liquido)

                        vapor = CP.PropsSI(propriedade, op1, prop1, 'Q', 1, substancia) / 1000
                        vapores.append(vapor)

                    else: 
                        liquido = CP.PropsSI(propriedade, op1, prop1, 'Q', 0, substancia) / 1000
                        liquidos.append(liquido)

                        vapor = CP.PropsSI(propriedade, op1, prop1, 'Q', 1, substancia) / 1000
                        vapores.append(vapor)

                else:
                    liquidos = None
                    vapores = None

        print(liquidos)
        print (vapores)
        print (lista_resultado)
        return lista_resultado, liquidos, vapores, fase
    
    except ValueError:
        return 'Erro'
