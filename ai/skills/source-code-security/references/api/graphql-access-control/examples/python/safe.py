import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def invoice(self, info, id: str) -> Invoice:
        require_auth(info.context.user)
        return Invoice.get(id=id, organization_id=info.context.user.organization_id)

    @strawberry.field
    def users(self, info) -> list[User]:
        require_role(info.context.user, "admin")
        return User.find_by_org(info.context.user.organization_id)
