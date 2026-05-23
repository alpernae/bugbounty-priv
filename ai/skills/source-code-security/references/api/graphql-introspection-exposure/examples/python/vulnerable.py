import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def invoice(self, id: str) -> Invoice:
        return Invoice.get(id=id)

    @strawberry.field
    def users(self) -> list[User]:
        return User.all()
