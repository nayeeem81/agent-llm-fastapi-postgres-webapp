from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapwebapp.data.model import Story


async def test_story_model_auto_rollback(db_session: AsyncSession) -> None:
    story = Story(story_name="Test Refactor Story", serial_number=1)
    db_session.add(story)
    await db_session.commit()

    result = await db_session.exec(select(Story).where(Story.story_name == "Test Refactor Story"))
    saved = result.first()

    assert saved is not None
    assert saved.story_name == "Test Refactor Story"