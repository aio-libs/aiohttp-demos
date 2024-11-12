import aiohttp_jinja2
from aiohttp import web
from sqlalchemy import select

from . import db


@aiohttp_jinja2.template("index.html")
async def index(request):
    async with request.app["db"]() as sess:
        questions = await sess.scalars(select(db.Question))
        return {"questions": questions.all()}


@aiohttp_jinja2.template("detail.html")
async def poll(request):
    async with request.app["db"]() as sess:
        question_id = request.match_info["question_id"]
        try:
            question, choices = await db.get_question(sess, question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {"question": question, "choices": choices}


@aiohttp_jinja2.template("results.html")
async def results(request):
    async with request.app["db"]() as sess:
        question_id = int(request.match_info["question_id"])

        try:
            question, choices = await db.get_question(sess, question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return {"question": question, "choices": choices}


async def vote(request):
    question_id = int(request.match_info["question_id"])
    data = await request.post()
    try:
        choice_id = int(data["choice"])
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(text="You have not specified choice value") from e
    try:
        await db.vote(request.app, question_id, choice_id)
    except db.RecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))
    router = request.app.router
    url = router["results"].url_for(question_id=str(question_id))
    raise web.HTTPFound(location=url)
