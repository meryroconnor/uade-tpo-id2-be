from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def json_response(data):
    json_compatible_item_data = jsonable_encoder(data)
    return JSONResponse(content=json_compatible_item_data)
