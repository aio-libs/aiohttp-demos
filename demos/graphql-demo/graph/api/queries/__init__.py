from graph.api.queries.user import UserQuery
from graph.api.queries.rooms import RoomsQuery


class Query(UserQuery, RoomsQuery):
    """Main GraphQL query point."""
