class Shelter:
    def __init__(self,name:str,total_vessel:int,total_people:int,lon:float,lat:float):
        #初始化名稱 總人數 總容量 經度 緯度
        self.name =name
        self.total_vessel = total_vessel
        self.total_people = total_people
        self.lon = lon
        self.lat = lat

    @property
    #property轉函式為變數讀取
    #計算收容所負載率
    def load_percentage(self) -> float:
        if self.total_people <= 0:
            return 0.0
        #小於0報0.0 避免報error
        return (self.total_vessel / self.total_people) * 100
    