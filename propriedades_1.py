# Nome do arquivo: propriedades_1.py
# Autor: Maurício Fernandes de Oliveira Assis
# Versão do Python: 3.12.1

import CoolProp.CoolProp as CP

def encontrarPropriedade (propriedade, substancia, propriedade1, propriedade2, op1, op2):
    try:
        if propriedade == op1:
            
            return 'op1'
        
        elif  propriedade == op2 :

            return 'op2'
        
        elif op1 == op2:

            return 'op'

        elif (op1 == 'P' and op2 == 'T') or (op1 == 'T' and op2 == 'P'):
            fase = CP.PhaseSI(op1, propriedade1, op2, propriedade2, substancia)

        else:
            
            if propriedade == 'V':
                propriedade = 'D'
                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S':
                    propriedade1 = propriedade1 * 1000

                elif op1 =='T':
                    propriedade1 = propriedade1 + 273.15

                elif op1 == 'Q':
                    propriedade1 = propriedade1

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    propriedade2 = propriedade2 * 1000

                elif op2 =='T':
                    propriedade2 = propriedade2 + 273.15
                
                elif op2 == 'Q':
                    propriedade2 = propriedade2

                fase = CP.PhaseSI(op1, propriedade1, op2, propriedade2, substancia)
                
                    
                propriedadeEncontrada = 1/CP.PropsSI(propriedade, op1, propriedade1, op2, propriedade2, substancia)   

                if propriedade== 'P' or propriedade == 'U' or propriedade == 'H' or propriedade == 'S':
                    propriedadeEncontrada = propriedadeEncontrada / 1000 # Convertendo para kJ/kg

                elif propriedade == 'T':
                    propriedadeEncontrada = propriedadeEncontrada - 273.15 #convertendo para Celsius

                if fase == 'twophase':
                    liquido = 1/CP.PropsSI(propriedade, op1, propriedade1, 'Q', 0, substancia)

                    vapor = 1/CP.PropsSI(propriedade, op1, propriedade1, 'Q', 1, substancia)

                    print (vapor)
                    print(liquido)
                      
            elif propriedade == 'Q':
                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S':
                    propriedade1 = propriedade1 * 1000

                elif op1 =='T':
                    propriedade1 = propriedade1 + 273.15

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    propriedade2 = propriedade2 * 1000

                elif op2 =='T':
                    propriedade2 = propriedade2 + 273.15

                fase = CP.PhaseSI(op1, propriedade1, op2, propriedade2, substancia)
                
                    
                propriedadeEncontrada = CP.PropsSI(propriedade, op1, propriedade1, op2, propriedade2, substancia)
                liquido = None
                vapor = None
                
            else:
                if op1 == 'P' or op1 == 'U' or op1 == 'H' or op1 == 'S' or op1 ==op2:
                    propriedade1 = propriedade1 * 1000

                elif op1 =='T':
                    propriedade1 = propriedade1 + 273.15

                elif op1 == 'Q':
                    propriedade1 = propriedade1

                if op2 == 'P' or op2 == 'U' or op2 == 'H' or op2 == 'S':
                    propriedade2 = propriedade2 * 1000

                elif op2 =='T':
                    propriedade2 = propriedade2 + 273.15
                
                elif op2 == 'Q':
                    propriedade2 = propriedade2

                fase = CP.PhaseSI(op1, propriedade1, op2, propriedade2, substancia)
                print (fase)
                propriedadeEncontrada = CP.PropsSI(propriedade, op1, propriedade1, op2, propriedade2, substancia)   

                if propriedade== 'P' or propriedade == 'U' or propriedade == 'H' or propriedade == 'S':
                    propriedadeEncontrada = propriedadeEncontrada / 1000 # Convertendo para kJ/kg

                elif propriedade == 'T':
                    propriedadeEncontrada = propriedadeEncontrada - 273.15 #convertendo para Celsius

                if fase == 'twophase':
                    if op1 == 'Q':
                        liquido = CP.PropsSI(propriedade, op2, propriedade2, 'Q', 0, substancia) / 1000
                        vapor = CP.PropsSI(propriedade, op2, propriedade2, 'Q', 1, substancia) / 1000

                    elif op2 == 'Q':
                        liquido = CP.PropsSI(propriedade, op1, propriedade1, 'Q', 0, substancia) / 1000
                        vapor = CP.PropsSI(propriedade, op1, propriedade1, 'Q', 1, substancia) / 1000
                        
                    else: 
                        liquido = CP.PropsSI(propriedade, op1, propriedade1, 'Q', 0, substancia) / 1000
                        vapor = CP.PropsSI(propriedade, op1, propriedade1, 'Q', 1, substancia) / 1000
                
                else:
                    liquido = None
                    vapor = None

            return {'propriedade':propriedadeEncontrada, 'fase': fase, 'liquido':liquido,  'vapor':vapor}
    
    except ValueError:
        return 'Erro'