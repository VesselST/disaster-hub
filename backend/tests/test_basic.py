import pytest
from models.shelter import Shelter

def test_shelter_load_percentage_calculation():
    # 建立一個容量 100，目前 80 人的避難所
    shelter = Shelter(name="測試中心", capacity=100, current_ppl=80)
    
    # 我們預期負載應該是 0.8
    assert shelter.load_percentage == 0.8

def test_shelter_full_status():
    shelter = Shelter(name="測試中心", capacity=100, current_ppl=100)
    # 預期當滿載時，負載為 1.0
    assert shelter.load_percentage == 1.0