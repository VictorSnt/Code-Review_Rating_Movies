from ninja import Schema

class PaginationSchema(Schema):
    paginated: bool = False
    page: int = 1
    page_size: int = 10