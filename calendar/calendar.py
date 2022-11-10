import json

room_list = [
    {
        "roomId": "roomId1",
    	"name": "room1"
    },
    {
        "roomId": "roomId2",
        "name": "room2"
    },
]

cal = {
    "roomId1":
        [
            {
                "bgn": 1668146400,  # 11/11 14:00
                "end": 1668153600   # 11/11 16:00
            }
        ],
    "roomId2":
        [
        ]
}

""" Get room info """
def get_room_list():
    return room_list

""" Get room status by roomId and datetime """
def get_room_status(roomId, datetime):
    for interval in cal[roomId]:
        if datetime >= interval["bgn"] and datetime <= interval["end"]:
            return 1   # occupied

    return 0   # free

""" Add new reservation to a room """
def reserve_room(roomId, bgn_datetime, end_datetime):
    if bgn_datetime >= end_datetime:
        raise ValueError("Invalid time range!")
    
    # check whether overlapped
    for interval in cal[roomId]:
        if (bgn_datetime >= interval["bgn"] and bgn_datetime < interval["end"]) or\
           (end_datetime > interval["bgn"] and end_datetime <= interval["end"]):
            return 1   # already exist

    cal[roomId].append({
        "bgn": bgn_datetime,
        "end": end_datetime,})

    return 0   # success

if __name__ == '__main__':
    print(get_room_list())
    reserve_room("roomId1", 1668146400, 1668146500)
    reserve_room("roomId1", 1668146000, 1668146200)
    queries = [{"roomId": "roomId1", "datetime": 1668146400, "expect_result": 1},
             {"roomId": "roomId1", "datetime": 1668146200, "expect_result": 1},
             {"roomId": "roomId1", "datetime": 1668153700, "expect_result": 0},
             {"roomId": "roomId2", "datetime": 1668146400, "expect_result": 0},]
    for query in queries:
        print(query)
        print(get_room_status(query["roomId"], query["datetime"]))
