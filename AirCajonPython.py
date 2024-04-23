import asyncio
from bleak import BleakClient
import pygame


DEVICE_ADDRESS_1 = "84:68:3E:12:31:66" #esquerda
DEVICE_ADDRESS_2 = "84:68:3E:05:B3:93"#direita
CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

pygame.mixer.init()
som1 = pygame.mixer.Sound('cajon_L.wav')
som2 = pygame.mixer.Sound('cajon_R.wav')

def play_sound(som):
    som.play()  
    
def notification_handler_1(sender, data): #notificacao 1
    if data[0] == 1:
        print("ESQUERDA: PLAY")
        play_sound(som1)

def notification_handler_2(sender, data): #notificacao 
    if data[0] == 1:
        print("DIREITA: PLAY")
        play_sound(som2)

async def connect_device(device_address, notification_handler):
    async with BleakClient(device_address) as client:
        if not await client.is_connected():
            print(f"ERRO {device_address}!")
            return

        print(f"Conectado ao dispositivo {device_address}!")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        print(f"Aguardando movimentos do dispositivo {device_address}...")
        await asyncio.sleep(30000)  

        await client.stop_notify(CHARACTERISTIC_UUID)
        print(f"Desconected {device_address}.")

async def main():
    await asyncio.gather(
        connect_device(DEVICE_ADDRESS_1, notification_handler_1),
        connect_device(DEVICE_ADDRESS_2, notification_handler_2)
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
