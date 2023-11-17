import asyncio
import random
from asyncua import Server
import logging

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger()


async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://192.168.68.132:4840/opcua/')    
    server.set_server_name("OPC-UA Test Server")

    # setup our own namespace, not really necessary but should as spec
    idx = await server.register_namespace("floodDetectionOPC")


    objFloodDetect = await server.nodes.objects.add_object(idx, 'FloodDetection')
    varWaterLvl = await objFloodDetect.add_variable(idx, 'waterLevel', 0)
    varPressure = await objFloodDetect.add_variable(idx, 'pressure', 0)
    varPumpSetting = await objFloodDetect.add_variable(idx, 'pumpSetting', 0)
    _logger.info("starting server...")


    async with server:
        # run forever every 5 secs
        while True:
                # Writing Variables
                await varWaterLvl.write_value(random.randint(25,35))
                await varPressure.write_value(random.randint(55,75))
                await varPumpSetting.write_value(random.randint(0,1))
                await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())