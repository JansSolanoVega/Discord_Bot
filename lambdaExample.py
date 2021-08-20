class Empleado():
    def __init__(self,sueldo,sexo,nombre):
        self.sueldo=sueldo
        self.sexo=sexo
        self.nombre=nombre
    def __str__(self):
        return f"Su nombre es {self.nombre} y es del sexo {self.sexo} con un sueldo de {self.sueldo}"

EmpleadosTotales=[
    Empleado(2000,'Masculino','pepe'),
    Empleado(2400,'Masculino','papo'),
    Empleado(3300,'Femenino','dariam'),
    Empleado(1900,'Masculino','robert'),
    Empleado(3400,'Femenino','malena'),
    Empleado(1200,'Masculino','pipo'),
]

EmpleadosMasAdinerados=filter(lambda empleado:empleado.sueldo>3200,EmpleadosTotales)
for EmpleadoAdinerado in EmpleadosMasAdinerados:
    print(EmpleadoAdinerado)