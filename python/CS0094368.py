import json
import struct

with open('./resources/here-stg-onemap-hdlm-native-global-1_topology-geometry_309106979.json') as f:
    data = json.load(f)

center_encoded = data['tile_center_here_2d_coordinate']
print(f'center location coordinates coded:\n{center_encoded}')
ref_encoded = data['nodes_in_tile'][0]["geometry"]["here_2d_coordinate"]
print(f'reference location coordinates coded:\n{ref_encoded}')

def decode_here_2d_coordinate_int(encoded):
    encoded_bin = bin(int(encoded))[2:].rjust(64, '0')
    lon_bin = encoded_bin[1::2]
    lat_bin = encoded_bin[2::2]
    lat_bin = lat_bin.rjust(32, lat_bin[0])
    lon_uint = int(lon_bin, base=2)
    lat_uint = int(lat_bin, base=2)
    lon_int = struct.unpack('i', struct.pack('I', lon_uint))[0]
    lat_int = struct.unpack('i', struct.pack('I', lat_uint))[0]
    return lat_int, lon_int

def decode_here_2d_coordinate(encoded):
    lat_int, lon_int = decode_here_2d_coordinate_int(encoded)
    lon_deg = lon_int * (360 / 2 ** 32)
    lat_deg = lat_int * (180 / 2 ** 31)
    print(lon_deg, lat_deg)
    return lat_deg, lon_deg

def decode_here_2d_coordinate_offset(encoded, encoded_reference):
    lat_int, lon_int = decode_here_2d_coordinate_int(encoded)
    ref_lat_int, ref_lon_int = decode_here_2d_coordinate_int(encoded_reference)
    lon_int ^= ref_lon_int
    lat_int ^= ref_lat_int
    lon_deg = lon_int * (360 / 2 ** 32)
    lat_deg = lat_int * (180 / 2 ** 31)
    print(lon_deg, lat_deg)
    return lat_deg, lon_deg

decode_here_2d_coordinate(center_encoded)
decode_here_2d_coordinate_offset(center_encoded, ref_encoded)