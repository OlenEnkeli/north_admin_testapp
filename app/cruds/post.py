from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreateSchema
from app.cruds.base import BaseCRUD


class PostCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=Post)

    @staticmethod
    def list_query() -> Select:
        return (
            select(Post)
            .filter(Post.is_published.is_(True))
            .order_by(Post.created_at.desc())
        )

    def list_by_tag_query(self, tags: str) -> Select:
        query = self.list_query()
        query = query.filter(Post.tags.contains([tags]))
        return query

    def list_by_author_query(self, author: User) -> Select:
        query = self.list_query()
        query.filter(Post.author_id == author.id)
        return query

    async def create(
        self,
        session: AsyncSession,
        origin: PostCreateSchema,
        author: User,
        is_published: bool = True,
    ) -> User | None:
        return await super().create(
            session=session,
            origin=origin,
            author_id=author.id,
            is_published=is_published,
        )


post_crud = PostCRUD()
