from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def inventario(request):
    vehiculos = [
        {
            'marca': 'Toyota',
            'modelo': 'Corolla',
            'anio': 2022,
            'placa': 'KLR582',
            'color': 'Blanco',
            'precio': 85000000,
            'estado': 'DISPONIBLE',
            'tiene_reserva': False,
            'imagen': 'https://tuyomotor.com/wp-content/uploads/2025/08/TUYO_COROLLA-26-2-scaled.jpg',
        },
        {
            'marca': 'Chevrolet',
            'modelo': 'Camaro',
            'anio': 2021,
            'placa': 'DFT219',
            'color': 'Azul',
            'precio': 120000000,
            'estado': 'RESERVADO',
            'tiene_reserva': True,
            'imagen': 'https://octane.rent/wp-content/uploads/2023/06/chevrolet-camaro-blue-41-600x400.webp',
        },
        {
            'marca': 'BMW',
            'modelo': 'X5',
            'anio': 2022,
            'placa': 'BMW001',
            'color': 'Gris',
            'precio': 210000000,
            'estado': 'DISPONIBLE',
            'tiene_reserva': False,
            'imagen': 'https://noticias.pro.pvt.coches.com/wp-content/uploads/2018/06/BMW-X5-2019-12.jpg?force_format=original&w=1280&h=720',
        },
        {
            'marca': 'Mercedes',
            'modelo': 'C300',
            'anio': 2023,
            'placa': 'MKP374',
            'color': 'Amarillo',
            'precio': 195000000,
            'estado': 'VENDIDO',
            'tiene_reserva': False,
            'imagen': 'https://objetos.estaticos-marca.com/assets/multimedia/imagenes/2019/02/20/15506779401989.jpg',
        },
        {
            'marca': 'Audi',
            'modelo': 'A4',
            'anio': 2022,
            'placa': 'NVS831',
            'color': 'Naranja',
            'precio': 175000000,
            'estado': 'RESERVADO',
            'tiene_reserva': True,
            'imagen': 'https://i.pinimg.com/736x/24/6b/78/246b78f4ad72bef384f7d509b3128124.jpg',
        },
    ]

    return render(request, 'inventario.html', {'vehiculos': vehiculos})