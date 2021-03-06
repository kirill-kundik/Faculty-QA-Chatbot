from flask import Blueprint, current_app, jsonify, request, abort

from app.search_wrapper import publish_question

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/healthCheck")
def health_check():
    return jsonify({"success": True})


@main_bp.route("/api/search")
def perform_direct_search():
    try:
        predictor = request.args.get("predictor")
        query = request.args.get("query")
    except KeyError:
        abort(400)
        return

    try:
        return jsonify(current_app.api_predictors_table[predictor](query))
    except KeyError:
        abort(404)
        return


@main_bp.route("/search")
def perform_search():
    try:
        predictor = request.args.get("predictor")
        query = request.args.get("query")
        msg_id = int(request.args.get("msg_id"))
        user_id = int(request.args.get("user_id"))
        chat_id = int(request.args.get("chat_id"))
    except (KeyError, ValueError):
        abort(400)  # will raise an error
        return

    question_id = publish_question(query, user_id, chat_id, msg_id)

    try:
        answer = current_app.predictors_table[predictor](query, question_id)
        if answer:
            return jsonify({"success": True, "answer": answer.serialize})
        else:
            return jsonify({"success": False})
    except KeyError:
        abort(404)  # will raise an error
        return
