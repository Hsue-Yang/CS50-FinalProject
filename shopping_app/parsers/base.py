class BaseShoppingParser:
    def fetch_results(self, keyword):
        """
        統一的介面，每個網站的 Parser 都要實作這個方法。
        回傳的資料格式如下：
        [
            {
                "name": "商品名稱",
                "price": 999,
                "link": "https://example.com/item123",
                "source": "momo"
            },
            ...
        ]
        """
        raise NotImplementedError("子類別必須實作 fetch_results 方法")
