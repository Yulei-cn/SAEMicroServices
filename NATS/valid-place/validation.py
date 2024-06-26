import asyncio
import nats
import json
import pickle
import os

data_dir = "./data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
data_file = os.path.join(data_dir, "vol.pkl")

if os.path.exists(data_file):
    with open(data_file, "rb") as f:
        vol = pickle.load(f)
else:
    vol = {}


def save_vol():
    with open(data_file, "wb") as f:
        pickle.dump(vol, f)


async def handle_create_vol(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    try:
        name, place = data.split(":")
        place = int(place)
        if name not in vol:
            vol[name] = place
            response = f"vol crée {name} avec  {place} place."
            print(response)
            save_vol()
        elif vol[name] == place:
            response = f"Le vol {name} existe déjà."
            print(response)
        else:
            vol[name] = place
            response = f"vol crée {name} avec  {place} place."
            print(response)
            save_vol()
    except Exception as e:
        response = f"Erreur lors de la création du vol: {str(e)}"
        print(response)

    await nc.publish(reply, response.encode())

async def handle_delete_vol(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    try:
        name, place = data.split(":")
        place = int(place)
        if name in vol:
            vol[name].pop()
            response = f"vol supprimé."
            save_vol()
    except Exception as e:
        response = f"Erreur lors de la création du vol: {str(e)}"
        print(response)

    await nc.publish(reply, response.encode())

async def handle_place_validation(msg):
    subject = msg.subject
    reply = msg.reply
    vol_request = msg.data.decode
    try:
        name, place=vol_request.splt(":")
        if name in vol:
            if vol[name] >= place:
                print(f"les place du vol {name} sont reserver.")
                vol[name] -= place
                response_msg = f"True,Resever,Vol reservé. Les place restente sont de {vol[name]}"
                save_vol()
            
            else:
                print("Place insufisante")
                response_msg = "False,failed, nombre de place insufisante"
        else:
            print("Vol inconnu.")
            response_msg = "False,Failed,Vol inconnu."

        await nc.publish(reply, response_msg.encode())   
    except Exception as err:
        print(err)

async def handle_place_devalidation(msg):
    subject = msg.subject
    reply = msg.reply
    vol_request = msg.data.decode
    try:
        name, place=vol_request.splt(":")
        if name in vol:
            print(f"{place} place du vol {name} sont de nouveaux displonible.")
            vol[name] += place
            response_msg = f"True,Rembourse,Les place restente sont de {vol[name]}"
            
        else:
            print("Vol inconnu.")
            response_msg = "False,Failed,Vol inconnu."

        await nc.publish(reply, response_msg.encode())   
    except Exception as err:
        print(err)

async def vol_request():

    # Envoi de la requête et attente de la réponse
    reponse = await nc.request("vol.request",timeout=10)

    # Décodage de la réponse
    reponse_data = json.loads(reponse.data.decode())
    print("Received response:", reponse_data)
    
    for key, value in reponse_data.items():
        if key not in vol:
            vol[key] = value
    
    save_vol()

async def main():
    global nc
    env = os.getenv("DJANGO_ENVIRONMENT", "development")
    user = os.getenv("NATS_USER", '')
    password = os.getenv("NATS_PASSWORD", '')
    if env == "development":
        nc = await nats.connect("nats://localhost:4222", user=user, password=password)
    else:
        nc = await nats.connect("nats://nats:4222", user=user, password=password)
        
    vol_request
    try:
        await nc.subscribe("validation.reservation.place.client", cb=handle_place_validation)
        await nc.subscribe("validation.remboursement.place.client.*", cb=handle_place_devalidation)
        await nc.subscribe("vol.creation", cb=handle_create_vol)
        await nc.subscribe("vol.delete", cb=handle_delete_vol)
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


if __name__ == '__main__':
    asyncio.run(main())

