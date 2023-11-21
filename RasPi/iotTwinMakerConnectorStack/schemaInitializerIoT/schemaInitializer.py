import json

def handler():
    return {"properties": {
                "distance": {
                    "definition":{
                        "dataType":{
                            "Type":"FLOAT"
                        }
                    },
                    "isTimeSeries":True
                        }
                    }
                }
    