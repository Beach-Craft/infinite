import json
import time


from utils import tools

async def add_channel_data(channel):
    
    users = await get_channel_data()
    
    if str(channel.id) in users:
        return False

    else:
        users[str(channel.id)] = "True"
                                                                        
    with open(f"data/channels.json","w") as file:
        json.dump(users, file)

    return True

async def get_channel_data():

    with open(f"data/channels.json","r") as file:
        channels = json.load(file)
        
    return channels

async def create_data(user):
    
    users = await get_data()
    
    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["warnings"] = {}
        users[str(user.id)]["count"] = 0
                                                                        
    with open("data/warns.json","w") as f:
        json.dump(users, f)
    return True

async def get_data():

    with open("data/warns.json","r") as f:
        users = json.load(f)
    return users

async def update_data(user, reason, moderator):
    users = await get_data()
    id = tools.id_generator()
    users[str(user.id)]["count"] += 1
    count = users[str(user.id)]["count"]
    users[str(user.id)]["warnings"][count] = {}
    users[str(user.id)]["warnings"][count]["id"] = str(id)
    users[str(user.id)]["warnings"][count]["reason"] = reason
    users[str(user.id)]["warnings"][count]["time"] = int(time.time())
    users[str(user.id)]["warnings"][count]["moderator"] = moderator.id

    with open("data/warns.json","w") as f:
        json.dump(users, f)

    data = [users[str(user.id)]["warnings"], users[str(user.id)]["count"]]

    return data

async def staff_data(staff):
    
    staffs = await get_staff_data()
    
    if str(staff.id) in staffs:
        return False

    else:
        staffs[str(staff.id)] = {}
        staffs[str(staff.id)]["points"] = 0
                                                                        
    with open("data/staff_points.json","w") as f:
        json.dump(staffs, f)
    return True

async def update_staff(staff):

    staffs = await get_staff_data()

    staffs[str(staff.id)]["points"] += 1

    with open("data/staff_points.json","w") as f:
        json.dump(staffs, f)

    data = [staffs[str(staff.id)]["points"]]

    return data

async def get_staff_data():

    with open("data/staff_points.json","r") as f:
        staffs = json.load(f)
        
    return staffs