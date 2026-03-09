import json
from typing import Union

from pydantic import BaseModel


class Asset(BaseModel):
    assetid: str
    templateid: Union[int, None] = None
    appid: Union[str, int, None] = "730"
    classid: Union[str, int, None] = None
    instanceid: Union[str, int, None] = None
    contextid: Union[int, str, None] = 2
    market_hash_name: Union[str, int, None] = None
    short_name: Union[str, None] = None
    orderNo: Union[str, int, None] = None
    price: float = float(0)


class LeaseAsset(Asset):
    price: Union[float, None] = None
    IsCanLease: bool = True
    IsCanSold: bool = False
    LeaseDeposit: float
    LeaseMaxDays: int
    LeaseUnitPrice: float
    LongLeaseUnitPrice: float = float(0)
    orderNo: Union[str, int, None] = None


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Asset, LeaseAsset)):
            return obj.model_dump(exclude_none=True)
        return json.JSONEncoder.default(self, obj)

class ECORentAsset(BaseModel):
    """
    StockId和AssetId二选一
    """

    SteamGameId: str = "730"
    StockId: Union[str, None] = None
    AssetId: Union[str, None] = None
    TradeTypes: list[int] = [2]
    RentMaxDay: int
    RentPrice: float
    LongRentPrice: Union[float, None] = None
    RentDeposits: float
    RentDescription: Union[str, None] = None

    @classmethod
    def fromLeaseAsset(cls, obj: LeaseAsset):
        return cls(
            SteamGameId=str(obj.appid),
            AssetId=obj.assetid,
            RentMaxDay=obj.LeaseMaxDays,
            RentPrice=obj.LeaseUnitPrice,
            LongRentPrice=obj.LongLeaseUnitPrice,
            RentDeposits=obj.LeaseDeposit,
        )


class GoodsNum(BaseModel):
    # GoodsNum和AssetId二选一
    GoodsNum: Union[str, None] = None
    AssetId: Union[str, None] = None
    SteamGameId: str = "730"


class ECOPublishStockAsset(BaseModel):
    AssetId: str
    SellPrice: float
    TradeTypes: list[int] = [1]
    Description: Union[str, None] = None
    SteamGameId: str = "730"

    @classmethod
    def fromAsset(cls, obj: Asset):
        return cls(AssetId=obj.assetid, SellPrice=float(obj.price), Description="", SteamGameId=str(obj.appid))  # type: ignore
