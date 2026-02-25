def test_map_service_to_json():
    from services.map_server import MapService
    from repositories.shelter_repository import ShelterRepository
    
    repo = ShelterRepository()
    service = MapService()
    
    shelters = repo.get_all_shelters()
    data = service.prepare_3d_data(shelters)
    
    assert isinstance(data, list)
    assert 'lat' in data[0]
    assert 'lon' in data[0]