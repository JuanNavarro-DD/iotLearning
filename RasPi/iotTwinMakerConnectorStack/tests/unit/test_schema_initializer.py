from schemaInitializerIoT.schemaInitializer import handler

def test_handler():
    assert handler() == {"properties": {
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