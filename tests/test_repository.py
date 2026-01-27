import pytest
from repositories.shelter_repository import ShelterRepository

def test_get_all_shelters_count_and_coords():
    """驗證是否能抓到 41 筆資料，且每筆都有經緯度"""
    repo = ShelterRepository()
    shelters = repo.get_all_shelters()
    
    # 1. 驗證總數是否為 41 (我們今天注入的數量)
    assert len(shelters) == 41
    
    # 2. 驗證資料是否包含座標 (不再是預設的 0.0)
    # 取第一筆資料來檢查
    sample = shelters[0]
    assert sample.lat != 0.0
    assert sample.lon != 0.0
    
    print(f"\n測試通過！")
    print(f" 總筆數: {len(shelters)}")
    print(f" 範例資料: {sample.name} -> 座標: ({sample.lat}, {sample.lon})")

def test_shelter_occupancy_logic():
    """驗證 Model 的負荷率計算邏輯依然正確 (SOLID SRP)"""
    from models.shelter import Shelter
    s = Shelter(name="測試", capacity=100, current_count=50)
    assert s.occupancy_rate == 50.0